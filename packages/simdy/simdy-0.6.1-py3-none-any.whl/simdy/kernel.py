
import random
import ctypes
from inspect import getsource, signature
from collections import OrderedDict
from tdasm import Runtime, translate, cpu_features
from .parser import parse
from .cgen import generate, register_function, ISet
from .arr import ArrayArg
from .strc_arg import StructArg
from .int_vec_arg import int64x2
from .holders import CompileError


def arg_type_check(name, value):
    if not hasattr(value, 'arg_class'):
        msg = "Only simdy kernel types are allowed in kernel: Argument %s is of %s type." % (name, str(type(value)))
        raise ValueError(msg)


class Kernel:
    def __init__(self, source: str, args=[], standalone=True,
                 name: str=None, func_args=[], nthreads=-1,
                 kernels=[], iset=ISet.AVX2, fma=True, optimize=True):

        self._source = source
        self._nthreads = nthreads
        if name is None:
            self._name = 'kernel_%i' % id(self)
        else:
            self._name = name

        self._args_map = OrderedDict()
        # TODO if arg allready exist, raise error????
        for name, val in args:
            arg_type_check(name, val)
            self._args_map[name] = val.arg_class(value=val)

        self._standalone = standalone
        self._internal_name = 'kernel_%i' % id(self)
        self._func_args_map = OrderedDict()
        for name, val in func_args:
            # TODO beter error message
            self._func_args_map[name] = val.arg_class(value=val)
        self._arr_args = self._collect_cmplx_args(self._args_map)

        self._runtime = None
        self.compile(kernels=kernels, iset=iset, fma=fma, optimize=optimize)

    def _collect_cmplx_args(self, arg_map):
        def has_array(struc_arg):
            for a in struc_arg.args:
                if isinstance(a, ArrayArg):
                    return True
            return False

        cmplx_args = []
        for arg in arg_map.values():
            if isinstance(arg, ArrayArg):
                cmplx_args.append(arg)
            elif isinstance(arg, StructArg) and has_array(arg):
                cmplx_args.append(arg)
        return cmplx_args

    @property
    def func_args(self):
        return self._func_args_map.values()

    @property
    def name(self):
        return self._name

    @property
    def internal_name(self):
        return self._internal_name

    @property
    def code(self):
        return self._code

    @property
    def ret_type(self):
        return self._ret_type

    @property
    def asm(self):
        return self._asm

    def compile(self, kernels=[], iset=ISet.AVX512, fma=True, optimize=True):
        self._kernels = kernels
        stms = parse(self._source)
        nthreads = self._nthreads if self._nthreads != -1 else 1
        try:
            asm, ret_type, global_kernels, rng, t_arg = generate(stms,
                                                                 args=self._args_map,
                                                                 standalone=self._standalone,
                                                                 name=self._name,
                                                                 func_args=self._func_args_map,
                                                                 kernels=kernels,
                                                                 optimize=optimize,
                                                                 iset=iset,
                                                                 fma=fma,
                                                                 nthreads=nthreads)
        except CompileError as e:
            e.source = self._source
            raise e

        self._ret_type = ret_type
        self._global_kernels = global_kernels
        self._asm = asm
        self._rng = rng
        self._thread_idx_arg = t_arg

        force_avx512 = False
        cpu = cpu_features()
        if iset == ISet.AVX512 and cpu.AVX512F:
            force_avx512 = True
        self._code = translate(asm, standalone=self._standalone, force_avx512=force_avx512)
        if self._standalone:
            self.load()

    def _check_multithreading(self):
        if self._nthreads != -1:
            all_kernels = self._kernels + list(self._global_kernels)
            for kernel in all_kernels:
                if self._nthreads != kernel._nthreads:
                    # NOTE multi-threaded kernels can also call kernels that doesn't have internal state
                    if len(kernel._args_map) == 0:
                        continue
                    raise ValueError("Threading number mismatch kernel %s with kernel %s" % (self.name, kernel.name))

    def _lbl_to_resolve(self, thread_idx):
        all_kernels = self._kernels + list(self._global_kernels)
        lbls = {}
        for kernel in all_kernels:
            if kernel._nthreads != -1:
                name = "%s_%i" % (kernel._internal_name, thread_idx)
                lbls[kernel._internal_name] = name
        return lbls

    def _pcg_state(self, initstate, initseq):

        def uint32(n):
            return n & 0xffffffff

        def uint64(n):
            return n & 0xffffffffffffffff

        def random_r(rng):
            oldstate = rng['state']
            rng['state'] = uint64(oldstate * 6364136223846793005 + rng['inc'])
            xorshifted = uint32(((oldstate >> 18) ^ oldstate) >> 27)
            rot = uint32(oldstate >> 59)
            return uint32((xorshifted >> rot) | (xorshifted << ((-rot) & 31)))

        rng = {'state': uint64(initstate), 'inc': uint64(initseq)}
        rng['state'] = 0
        rng['inc'] = uint64(initseq << 1) | 1
        random_r(rng)
        rng['state'] = uint64(rng['state'] + initstate)
        random_r(rng)
        return ctypes.c_longlong(rng['state']).value, ctypes.c_longlong(rng['inc']).value

    def _load(self, runtime):
        if self._runtime is runtime:  # Kernel allready loaded
            return

        self._check_multithreading()
        if self._nthreads != -1:
            self._kernel_names = []
            self._ds = []
            for i in range(self._nthreads):
                name = "%s_%i" % (self._internal_name, i)
                lbls = self._lbl_to_resolve(i)
                self._ds.append(runtime.load(name, self._code, lbls))
                self._kernel_names.append(name)
            self._kernel_names = tuple(self._kernel_names)
        else:
            self._ds = [runtime.load(self.internal_name, self._code)]
        self._runtime = runtime
        # NOTE After we load kernel to memory we initialize paramters(args) with default values

        for name, arg in self._args_map.items():
            self.set_value(name, arg.value)

        if self._rng is not None:
            for ds in self._ds:
                initstate = random.randint(0, (1 << 64) - 1)
                initseq = random.randint(0, (1 << 64) - 1)
                state, seq = self._pcg_state(initstate, initseq)
                self._rng.set_ds_value(ds, int64x2(state, seq))

        if self._thread_idx_arg is not None:
            for index, ds in enumerate(self._ds):
                self._thread_idx_arg.set_ds_value(ds, index)

    def load(self):

        def sum_kernels(root_kernel, csize, dsize):
            all_kernels = root_kernel._kernels + list(root_kernel._global_kernels)
            for kernel in all_kernels:
                sum_kernels(kernel, csize + kernel._code.code_section_size(), dsize + kernel._code.data_section_size())
            return csize, dsize

        csize, dsize = sum_kernels(self, self._code.code_section_size(), self._code.data_section_size())
        csize = csize * max(1, self._nthreads)
        ncode_pages = csize // 64000 + 1
        dsize = dsize * max(1, self._nthreads)
        ndata_pages = dsize // 64000 + 1
        runtime = Runtime(ncode_pages=ncode_pages, ndata_pages=ndata_pages)

        def iter_kernels(root_kernel):
            all_kernels = root_kernel._kernels + list(root_kernel._global_kernels)
            for kernel in all_kernels:
                iter_kernels(kernel)
            root_kernel._load(runtime)

        iter_kernels(self)

    def _refresh_arrays(self, root_kernel):
        for k in root_kernel._kernels:
            self._refresh_arrays(k)

        for arg in root_kernel._arr_args:
            for ds in root_kernel._ds:
                # TODO - only arrays needs to be refreshed, rename to refresh_arrays!
                arg.refresh_ds(ds)

    def run(self, args={}):
        if not self._standalone:
            raise ValueError("Function kernel cannot be directly executed.")

        # NOTE -- Array can be realocated when its size is changed so we must refresh address of arrays
        self._refresh_arrays(self)

        for name, value in args.items():
            self.set_value(name, value)

        if self._nthreads != -1:
            self._runtime.run_multiple(self._kernel_names)
        else:
            self._runtime.run(self.internal_name)

    def get_value(self, name, thread_idx=-1):
        index = thread_idx if thread_idx != -1 else 0
        return self._args_map[name].get_ds_value(self._ds[index])

    def set_value(self, name, value, thread_idx=-1):
        if thread_idx == -1:
            for ds in self._ds:
                self._args_map[name].set_ds_value(ds, value)
        else:
            self._args_map[name].set_ds_value(self._ds[thread_idx], value)


class SimdyCallable:
    kernels = {}

    def __init__(self, name, source, arg_types, ret_name, ret_type, nthreads=-1, iset=ISet.AVX, fma=True):
        self._name = name
        self._source = source
        self._arg_types = arg_types
        self._ret_name = ret_name
        self._ret_type = ret_type
        self.__name__ = name
        self.nthreads = nthreads
        self.iset = iset
        self.fma = fma

    def __call__(self, *func_args):
        if len(self._arg_types) != len(func_args):
            raise ValueError("Wrong number of arguments.", func_args)
        args = []
        arg_types = []
        for (name, typ), val in zip(self._arg_types, func_args):
            arg_type_check(name, val)
            args.append((name, val))
            arg_type = val.arg_class(value=val).type_name()
            if typ and not isinstance(val, typ):
                raise ValueError("Function %s, argument %s type mismatch %s != %s" % (self._name, name, type(val), typ))
            arg_types.append(arg_type)

        key = (self._name, tuple(arg_types))
        if key in self.kernels:
            k = self.kernels[key]
        else:
            if self._ret_type is not None:
                args.append((self._ret_name, self._ret_type()))
            k = Kernel(self._source, args=args, nthreads=self.nthreads, fma=self.fma, iset=self.iset)
            self.kernels[key] = k
        for (name, typ), val in zip(self._arg_types, func_args):
            k.set_value(name, val)
        k.run()
        if self._ret_type is not None:
            if self.nthreads != -1:
                result = [k.get_value(self._ret_name, i) for i in range(self.nthreads)]
                return tuple(result)
            else:
                return k.get_value(self._ret_name)


def create_simdy_callable(fun, nthreads=-1, iset=ISet.AVX2, fma=True):
    name = fun.__name__
    sig = signature(fun)
    args = []
    fun_key = []
    for p in sig.parameters:
        if hasattr(sig.parameters[p].annotation, 'arg_class'):
            args.append((p, sig.parameters[p].annotation))
            fun_key.append(sig.parameters[p].annotation)
        else:
            args.append((p, None))
            fun_key.append(None)
    args = tuple(args)
    source = getsource(fun)

    if hasattr(sig.return_annotation, 'arg_class'):
        ret_name = 'ret_value_%i' % id(sig)
        ret_type = sig.return_annotation
        arg_names = ','.join(p for p in sig.parameters)
        func_call = '\n%s = %s(%s)\n' % (ret_name, name, arg_names)
        full_source = source + func_call
    else:
        ret_name, ret_type = None, None
        arg_names = ','.join(p for p in sig.parameters)
        func_call = '\n%s(%s)\n' % (name, arg_names)
        full_source = source + func_call

    # TODO module = fun.__module__  # can be __main__ or module name
    # TODO register global_inline_function(name, source, arg_types, module)
    register_function(name, tuple(fun_key), source)

    return SimdyCallable(name, full_source, args, ret_name, ret_type, nthreads=nthreads, iset=iset, fma=fma)


def simdy_kernel(*args, **kwargs):
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # called as @decorator
        function = args[0]
        return create_simdy_callable(function)
    else:
        # called as @decorator(*args, **kwargs)
        fma = kwargs.get('fma', True)
        iset = kwargs.get('iset', ISet.AVX512)
        nthreads = kwargs.get('nthreads', -1)

        def real_decorator(function):
            return create_simdy_callable(function, iset=iset, fma=fma, nthreads=nthreads)
        return real_decorator
