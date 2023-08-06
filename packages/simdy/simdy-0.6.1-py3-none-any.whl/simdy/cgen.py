
import re
from collections import defaultdict, OrderedDict
from enum import Enum
from tdasm import cpu_features
from .holders import Name, CompileError, Const
from .asm_gen import AsmGen
from .util import generate_name
from .regs import Regs
from .loc_args import LocalArgs
from .args import ComplexArgument
from .ptr import PointerArg
from .strc_arg import StructArg
from .acum import Acums
from .opt import FunctionOptimizer
from .usr_typ import get_user_type_factory


class ISet(Enum):
    SSE = 1
    AVX = 2
    AVX2 = 3
    AVX512 = 4


_argument_facotries = {}


def register_arg_factory(arg_type, factory):
    _argument_facotries[arg_type] = factory


_built_ins = {}


def register_built_in(name, key, callback):
    def find_start_idx(key):
        for index, k in enumerate(key):
            if k is Name or k is Const:
                return index
        return -1

    def build_right_key(key):
        right_key = tuple()
        start_idx = find_start_idx(key)
        if start_idx != -1:
            right_key = tuple(key[start_idx:])
        return right_key

    if name in _built_ins:
        fns, right_keys = _built_ins[name]
        fns[key] = callback
        right_keys.add(build_right_key(key))
    else:
        right_keys = set([build_right_key(key)])
        _built_ins[name] = ({key: callback}, right_keys)


_global_funcs = {}


def register_function(name, key, source):
    fkey = []
    for k in key:
        if k:
            fkey.append(k.arg_class)
        else:
            fkey.append(None)
    fkey = tuple(fkey)
    if name in _global_funcs:
        fn = _global_funcs[name]
        fn[fkey] = source
    else:
        _global_funcs[name] = {fkey: source}


def get_global_function(name, key):
    fns = _global_funcs[name]
    key = tuple(key)
    none_key = tuple([None] * len(key))
    if key in fns:
        source = fns[key]
    elif none_key in fns:
        source = fns[none_key]
    else:
        raise ValueError("Function %s with specified parameters not found." % name, key)
    from .parser import parse
    stms = parse(source)
    if len(stms) != 1:
        raise ValueError("In source only function %s is expected." % name, key, source)
    fn_stm = stms[0]
    if not fn_stm.is_function():
        raise ValueError("In source only function %s is expected." % name, key, source)
    return fn_stm


_global_kernels = {}


def register_kernel(name, func_args, source, optimize=False):
    args = [val.arg_class(name, value=val) for name, val in func_args]
    fkey = tuple(arg.type_name() for arg in args)
    if name in _global_kernels:
        fn = _global_kernels[name]
        fn[fkey] = (source, func_args, optimize)
    else:
        _global_kernels[name] = {fkey: (source, func_args, optimize)}


_global_compiled_kernels = {}


def has_global_kernel(name, typs):
    if name not in _global_kernels:
        return False

    fkey = []
    for typ in typs:
        if typ.is_pointer():
            fkey.append(typ.arg.type_name())
        else:
            fkey.append(_argument_facotries[typ]().type_name())
    fkey = tuple(fkey)
    return fkey in _global_kernels[name]


def get_global_kernel(name, typs, iset, fma):
    fkey = []
    for typ in typs:
        if typ.is_pointer():
            fkey.append(typ.arg.type_name())
        else:
            fkey.append(_argument_facotries[typ]().type_name())
    fkey = tuple(fkey)

    fns = _global_kernels[name]
    if fkey not in fns:
        raise ValueError("Kernel %s with specified parameters not found." % name, typs)

    kkey = (fkey, iset, fma)
    if name in _global_compiled_kernels:
        kernels = _global_compiled_kernels[name]
        if kkey in kernels:
            return kernels[kkey]

    source, func_args, optimize = fns[fkey]
    from .kernel import Kernel
    kernel = Kernel(source, standalone=False, name=name, func_args=func_args, iset=iset, fma=fma, optimize=optimize)

    if name in _global_compiled_kernels:
        kernels = _global_compiled_kernels[name]
        kernels[kkey] = kernel
    else:
        _global_compiled_kernels[name] = {kkey: kernel}
    return kernel


class CodeGenerator:
    def __init__(self):
        self.regs = Regs()

    def generate_asm(self, statements,
                     args={},
                     standalone=True,
                     name=None,
                     func_args={},
                     kernels=[],
                     optimize=False,
                     iset=ISet.AVX2,
                     fma=True,
                     nthreads=1):

        self._kernels = kernels
        self._args = args.values()
        self._args_map = args
        self._locals_stack = [LocalArgs()]
        self._local_funcs = {}
        self._reg_cache = {}
        self._cached_regs = set()
        self._constants = {}
        self._return_labels = ['_end_kernel_label_%s' % id(self)]
        self._ret_types = [None]
        self.cpu = self._configure_cpu_features(iset, fma)
        self.gen = AsmGen(self.cpu)
        self._iset = iset
        self._fma = fma
        self._optimize = optimize
        self._used_tmp_args = defaultdict(set)
        self._free_tmp_args = defaultdict(set)
        self._global_kernels = set()
        self._loc_arr_structs = {}
        self._loc_vars = [(defaultdict(list), defaultdict(list))]
        self.rng_state = None
        self.thread_idx = None
        self.nthreads = nthreads

        self._store_records = [defaultdict(int)]

        self._analyze_stms(statements)

        kernel_asm = self._store_func_args(func_args)
        if not standalone:
            # TODO Argument checking, func_args with args in fn_stm
            if len(statements) != 1:
                raise ValueError("Only function statement is expected!", statements)
            fn_stm = statements[0]
            if not fn_stm.is_function():
                raise ValueError("Only function statement is expected!", statements)
            if len(fn_stm.args) != len(func_args):
                raise ValueError("Wrong number of arguments in %s function!" % fn_stm.name)

            self._set_last_stm(fn_stm)
            kernel_asm += ''.join(self.stm_code(s) for s in fn_stm.body)
            # TODO if ... return 4 else return 5 .. if statement is last staement and this is legal
            if self.get_return_type():
                if not fn_stm.body[-1].is_return():
                    raise TypeError("Expected return as last statemnt in %s." % fn_stm.name)
            # TODO Type checking for return types
        else:
            kernel_asm += ''.join(self.stm_code(s) for s in statements)
        struct_descs = self._generate_struct_descs()
        offsets, stack_size, map_name_to_typ = self._calculate_stack_offsets()

        data_section = self._generate_data_section() + '\n'
        data_section = struct_descs + '\n' + data_section
        data_section = "\n#DATA \n" + data_section + "#CODE \n"

        code = self.stack_setup(stack_size)
        for loc_arr_arg, name in self._loc_arr_structs.items():
            code += 'lea rax, byte[%s]\n' % loc_arr_arg.name
            code += 'mov qword [%s + Array.size], %i\n' % (name, len(loc_arr_arg.value))
            code += 'mov qword [%s + Array.address], rax\n' % name
        code += kernel_asm
        code += self.stack_cleanup()

        code = self._recode_asm(code, offsets, 'rsp', map_name_to_typ) + '\n'
        code = data_section + code
        if not standalone:
            code += 'ret\n'

        return code, self.get_return_type(), self._global_kernels, self.rng_state, self.thread_idx

    def _configure_cpu_features(self, iset, fma):
        cpu = cpu_features()
        if iset == ISet.SSE:
            cpu.AVX = False
            cpu.AVX2 = False
            cpu.FMA = False
            cpu.AVX512F = cpu.AVX512ER = cpu.AVX512PF = cpu.AVX512CD = cpu.AVX512DQ = cpu.AVX512BW = cpu.AVX512VL = False
        elif iset == ISet.AVX:
            cpu.AVX2 = False
            cpu.FMA = False
            cpu.AVX512F = cpu.AVX512ER = cpu.AVX512PF = cpu.AVX512CD = cpu.AVX512DQ = cpu.AVX512BW = cpu.AVX512VL = False
        elif iset == ISet.AVX2:
            if fma is False:
                cpu.FMA = False
            cpu.AVX512F = cpu.AVX512ER = cpu.AVX512PF = cpu.AVX512CD = cpu.AVX512DQ = cpu.AVX512BW = cpu.AVX512VL = False
        else: # AVX512
            if fma is False:
                cpu.FMA = False
        return cpu

    def _store_func_args(self, func_args_map):
        self.clear_regs()
        acums = Acums()
        code = ''
        regs = [acums.pop_type(self, arg) for arg in func_args_map.values()]
        self.allocate_regs(regs)
        for (name, arg), reg in zip(func_args_map.items(), regs):
            if isinstance(arg, ComplexArgument) and not arg.is_pointer():
                arg = PointerArg(arg)
            if arg.is_multi_part(self):
                co, regs, new_typ = arg.load_cmd(self, ptr_reg=reg)
                code += co
                code += arg.store_cmd(self, regs)
            else:
                code += arg.store_cmd(self, reg)
            self._locals_stack[-1].add(name, arg)
            stores = self._store_records[-1]
            stores[arg] = name
        self.clear_regs()
        return code

    def struct_for_loc_array(self, arg):
        if arg not in self._loc_arr_structs:
            self._loc_arr_structs[arg] = generate_name('loc_arr')
        return self._loc_arr_structs[arg]

    def _recode_asm(self, code, offsets, reg, map_name_to_typ):
        new_code = []

        if self._optimize:
            fun_opt = FunctionOptimizer(self, code, self._store_records[-1])
            code = fun_opt.optimize()

        for line in code.splitlines():
            for key, value in offsets.items():
                if key in line:
                    tokens = re.split(' |,|\[|\]|;|\.', line)
                    if key in tokens:
                        start = line.index('[')
                        end = line.index(']', start)
                        if key + '.' in line:
                            substr = line[start:end + 1].replace(key, '%s + %i' % (reg, value))
                            start_p = substr.index('.')
                            substr = substr[:start_p] + '+' + map_name_to_typ[key] + substr[start_p:]
                        else:
                            substr = line[start:end + 1].replace(key, '%s + %i' % (reg, value))
                        line = line[0:start] + substr + line[end + 1:]
            new_code.append(line)

        return '\n'.join(new_code)

    def stack_setup(self, stack_size):
        # dynamic stack alignment on 64-byte boundary
        code = 'push r13 \n'
        code += 'mov r13, rsp \n'
        code += 'and rsp, -64 \n'
        code += 'sub rsp, %i \n' % stack_size
        return code

    def stack_cleanup(self):
        code = self.return_label() + ':\n'
        code += 'mov rsp, r13 \n'
        code += 'pop r13 \n'
        return code

    def stm_code(self, stm):
        self.clear_regs()
        try:
            asm = stm.asm_code(self)
        except CompileError as e:
            e.lineno = stm.lineno
            raise e
        return asm

    def _generate_data_section(self):
        data_sec_repr = ''

        if self.rng_state is not None:
            data_sec_repr += self.rng_state.data_sec_repr()

        if self.thread_idx is not None:
            data_sec_repr += self.thread_idx.data_sec_repr()

        for arg in self._args:
            data_sec_repr += arg.data_sec_repr()

        for arg in self._constants.values():
            data_sec_repr += arg.data_sec_repr()

        return data_sec_repr

    def _generate_struct_descs(self):
        od = OrderedDict()
        args = list(self._args)
        for _locals in self._locals_stack:
            args.extend(arg for arg in iter(_locals))
        for arg_type, tmp_args in self._used_tmp_args.items():
            args.extend(tmp_args)
        for arg_type, tmp_args in self._free_tmp_args.items():
            args.extend(tmp_args)
        for arg in args:
            if arg.is_pointer():
                arg = arg.arg
            if isinstance(arg, ComplexArgument):
                if isinstance(arg, StructArg):
                    for a in arg.args:
                        if isinstance(a, ComplexArgument):
                            desc = a.struct_desc()
                            od[desc] = desc

                desc = arg.struct_desc()
                od[desc] = desc
                if arg.is_subscriptable():
                    arg = arg.value.arg
                    if isinstance(arg, ComplexArgument):
                        desc = arg.struct_desc()
                        od[desc] = desc
        struct_descs = '\n'.join(val for val in od.values())
        return struct_descs

    def _calculate_stack_offsets(self):
        # on stack goes local arguments , func_args and temp args
        offsets = {}
        cur_offset = 4

        args = []
        for _locals in self._locals_stack:
            args.extend(arg for arg in iter(_locals))
        for arg_type, tmp_args in self._used_tmp_args.items():
            args.extend(tmp_args)
        for arg_type, tmp_args in self._free_tmp_args.items():
            args.extend(tmp_args)

        # TODO investigate this, maybe is better without sort!!!
        args = sorted(args, key=lambda obj: obj.stack_size(self.cpu))
        map_name_to_typ = {}

        for loc_arr_arg, name in self._loc_arr_structs.items():
            map_name_to_typ[name] = 'Array'
            cur_offset = (cur_offset + 64 - 1) & ~(64 - 1)
            offsets[name] = cur_offset
            cur_offset += loc_arr_arg.array_desc.size()

        for arg in args:
            if isinstance(arg, StructArg):
                map_name_to_typ[arg.name] = arg.type_name()
            cur_offset = (cur_offset + arg.stack_align(self.cpu) - 1) & ~(arg.stack_align(self.cpu) - 1)
            offsets[arg.name] = cur_offset
            cur_offset += arg.stack_size(self.cpu)

        align = 128  # align stack boundary (stack aligement is 64)
        cur_offset = (cur_offset + align - 1) & ~(align - 1)
        # NOTE if align = 64 - AVX512 craches -- this must be investigated Hint: sub rsp, stack_size
        # Maybe stack_size = align64(cur_offset) + 64 is correct value
        return offsets, cur_offset, map_name_to_typ

    def create_arg(self, dest, arg_type):
        arg = self.get_arg(dest)
        if arg is not None:
            self.type_arg_check(arg, arg_type)
            return arg

        if not isinstance(dest, Name):
            raise CompileError("Attr and Subscript arg. cannot be created!")
        arg = self._locals_stack[-1].add(dest.name, self.arg_factory(arg_type))
        stores = self._store_records[-1]
        stores[arg] = dest.name
        return arg

    def type_arg_check(self, arg, arg_type):
        if self._tname(arg) != self._tname(arg_type):
            raise CompileError("Type mismatch! %s != %s" % (self._tname(arg), self._tname(arg_type)))

    def _tname(self, arg):
        if arg.is_pointer():
            return arg.type_name() + arg.arg.type_name()
        return arg.type_name()

    def add_local_array(self, arg):
        arg = self._locals_stack[-1].add(arg.name, arg)
        return arg

    def create_user_arg(self, type_name):
        factory = get_user_type_factory(type_name)
        if factory is None:
            return None
        value = factory()
        arg = value.arg_class(value=value)
        arg = self._locals_stack[-1].add(arg.name, arg)
        return arg

    def arg_factory(self, arg_type):
        if arg_type.is_pointer():
            return PointerArg(arg_type.arg)
        return _argument_facotries[arg_type]()

    def create_tmp_arg(self, arg_type):
        if arg_type in self._free_tmp_args:
            if len(self._free_tmp_args[arg_type]) > 0:
                arg = self._free_tmp_args[arg_type].pop()
                self._used_tmp_args[arg_type].add(arg)
                return arg
        arg = self.arg_factory(arg_type)
        self._used_tmp_args[arg_type].add(arg)
        return arg

    def release_tmp_arg(self, arg):
        self._free_tmp_args[type(arg)].add(arg)
        self._used_tmp_args[type(arg)].remove(arg)

    def get_arg(self, source):
        # NOTE search priorities locals, args
        name = source.name

        if len(self._locals_stack) > 1:  # local funcs only sees local variables
            return self._locals_stack[-1].get_arg(name)

        for _locals in reversed(self._locals_stack):
            arg = _locals.get_arg(name)
            if arg is not None:
                return arg

        if name in self._args_map:
            return self._args_map[name]

        return None

    def is_user_arg(self, source):
        return source.name in self._args_map

    def clear_regs(self):
        """Free all registers."""
        if self.cpu.AVX512F:
            self._k = ['k7', 'k6', 'k5', 'k4', 'k3', 'k2', 'k1']
            self._zmm = ['zmm31', 'zmm30', 'zmm29', 'zmm28', 'zmm27', 'zmm26', 'zmm25', 'zmm24',
                         'zmm23', 'zmm22', 'zmm21', 'zmm20', 'zmm19', 'zmm18', 'zmm17', 'zmm16',
                         'zmm15', 'zmm14', 'zmm13', 'zmm12', 'zmm11', 'zmm10', 'zmm9', 'zmm8',
                         'zmm7', 'zmm6', 'zmm5', 'zmm4', 'zmm3', 'zmm2', 'zmm1', 'zmm0']
            self._ymm = ['ymm31', 'ymm30', 'ymm29', 'ymm28', 'ymm27', 'ymm26', 'ymm25', 'ymm24',
                         'ymm23', 'ymm22', 'ymm21', 'ymm20', 'ymm19', 'ymm18', 'ymm17', 'ymm16',
                         'ymm15', 'ymm14', 'ymm13', 'ymm12', 'ymm11', 'ymm10', 'ymm9', 'ymm8',
                         'ymm7', 'ymm6', 'ymm5', 'ymm4', 'ymm3', 'ymm2', 'ymm1', 'ymm0']
            self._xmm = ['xmm31', 'xmm30', 'xmm29', 'xmm28', 'xmm27', 'xmm26', 'xmm25', 'xmm24',
                         'xmm23', 'xmm22', 'xmm21', 'xmm20', 'xmm19', 'xmm18', 'xmm17', 'xmm16',
                         'xmm15', 'xmm14', 'xmm13', 'xmm12', 'xmm11', 'xmm10', 'xmm9', 'xmm8',
                         'xmm7', 'xmm6', 'xmm5', 'xmm4', 'xmm3', 'xmm2', 'xmm1', 'xmm0']
        else:
            self._ymm = ['ymm15', 'ymm14', 'ymm13', 'ymm12', 'ymm11', 'ymm10', 'ymm9', 'ymm8',
                         'ymm7', 'ymm6', 'ymm5', 'ymm4', 'ymm3', 'ymm2', 'ymm1', 'ymm0']
            self._xmm = ['xmm15', 'xmm14', 'xmm13', 'xmm12', 'xmm11', 'xmm10', 'xmm9', 'xmm8',
                         'xmm7', 'xmm6', 'xmm5', 'xmm4', 'xmm3', 'xmm2', 'xmm1', 'xmm0']
        self._general = ['r15d', 'r14d', 'r12d', 'r11d', 'r10d', 'r9d', 'r8d',
                         'ebp', 'edi', 'esi', 'edx', 'ecx', 'ebx', 'eax']
        self._general64 = ['r15', 'r14', 'r12', 'r11', 'r10', 'r9', 'r8',
                           'rbp', 'rdi', 'rsi', 'rdx', 'rcx', 'rbx', 'rax']
        self._reg_cache = {}
        self._cached_regs = set()

    def used_regs(self):
        used_k = set()
        if self.cpu.AVX512F:
            zmm = ['zmm31', 'zmm30', 'zmm29', 'zmm28', 'zmm27', 'zmm26', 'zmm25', 'zmm24',
                   'zmm23', 'zmm22', 'zmm21', 'zmm20', 'zmm19', 'zmm18', 'zmm17', 'zmm16',
                   'zmm15', 'zmm14', 'zmm13', 'zmm12', 'zmm11', 'zmm10', 'zmm9', 'zmm8',
                   'zmm7', 'zmm6', 'zmm5', 'zmm4', 'zmm3', 'zmm2', 'zmm1', 'zmm0']
            used_xmms = set(zmm) - set(self._zmm)
            used_k = set(['k7', 'k6', 'k5', 'k4', 'k3', 'k2', 'k1']) - set(self._k)
        elif self.cpu.AVX:
            ymm = ['ymm15', 'ymm14', 'ymm13', 'ymm12', 'ymm11', 'ymm10', 'ymm9', 'ymm8',
                   'ymm7', 'ymm6', 'ymm5', 'ymm4', 'ymm3', 'ymm2', 'ymm1', 'ymm0']
            used_xmms = set(ymm) - set(self._ymm)
        else:
            xmm = ['xmm15', 'xmm14', 'xmm13', 'xmm12', 'xmm11', 'xmm10', 'xmm9', 'xmm8',
                   'xmm7', 'xmm6', 'xmm5', 'xmm4', 'xmm3', 'xmm2', 'xmm1', 'xmm0']
            used_xmms = set(xmm) - set(self._xmm)

        general64 = ['r15', 'r14', 'r12', 'r11', 'r10', 'r9', 'r8',
                     'rbp', 'rdi', 'rsi', 'rdx', 'rcx', 'rbx', 'rax']
        regs = set(general64) - set(self._general64)
        return list(used_xmms) + list(regs) + list(used_k)

    def register(self, typ):
        """
        Allocate currently unused register for temporally usage.

        @param typ - reigster type(general, general64, pointer, xmm, ymm, zmm, mask)
        """
        if typ == 'pointer':
            self._general.pop()
            return self._general64.pop()
        elif typ == 'general':
            self._general64.pop()
            return self._general.pop()
        elif typ == 'general64':
            self._general.pop()
            return self._general64.pop()
        elif typ == 'xmm':
            self._ymm.pop()
            if self.cpu.AVX512F:
                self._zmm.pop()
            return self._xmm.pop()
        elif typ == 'ymm':
            self._xmm.pop()
            if self.cpu.AVX512F:
                self._zmm.pop()
            return self._ymm.pop()
        elif typ == 'zmm':
            self._xmm.pop()
            self._ymm.pop()
            return self._zmm.pop()
        elif typ == 'mask':
            return self._k.pop()
        else:
            raise CompileError("Unknown type(%s) of register" % typ)

    def release_reg(self, reg):
        """
        Free currently used register.

        @param reg - Register that must be freed
        """
        if reg in self._cached_regs:
            return
        if isinstance(reg, tuple):
            for r in reg:
                self._release_reg(r)
        else:
            self._release_reg(reg)

    def _release_reg(self, reg):
        if self.regs.is_xmm(reg) and reg not in self._xmm:
            self._xmm.append(reg)
            self._ymm.append('y' + reg[1:])
            if self.cpu.AVX512F:
                self._zmm.append('z' + reg[1:])
        elif self.regs.is_ymm(reg) and reg not in self._ymm:
            self._ymm.append(reg)
            self._xmm.append('x' + reg[1:])
            if self.cpu.AVX512F:
                self._zmm.append('z' + reg[1:])
        elif self.regs.is_zmm(reg) and reg not in self._zmm:
            self._zmm.append(reg)
            self._xmm.append('x' + reg[1:])
            self._ymm.append('y' + reg[1:])
        elif self.regs.is_mask(reg) and reg not in self._k:
            self._k.append(reg)
        elif self.regs.is_reg32(reg) and reg not in self._general:
            self._general.append(reg)
            self._general64.append(self.regs.t_32_to_64(reg))
        elif self.regs.is_reg64(reg) and reg not in self._general64:
            self._general64.append(reg)
            self._general.append(self.regs.t_64_to_32(reg))
        else:
            raise CompileError("Register %s was allready unused!!!" % reg)

    def create_const(self, arg):
        key = (type(arg), repr(arg.value))
        if key in self._constants:
            return self._constants[key]
        self._constants[key] = arg
        return arg

    def put_in_cache(self, key, reg, typ):
        self._reg_cache[key] = (reg, typ)
        self._cached_regs.add(reg)

    def get_from_cache(self, key):
        return self._reg_cache.get(key, None)

    def in_cache(self, key):
        return key in self._reg_cache

    def remove_from_cache(self, key):
        if key in self._reg_cache:
            reg, typ = self._reg_cache[key]
            del self._reg_cache[key]
            self._cached_regs.remove(reg)

    def can_destruct(self, reg):
        if reg in self._cached_regs:
            return False
        return True

    def has_local_fn(self, name):
        return name in self._local_funcs or name in _global_funcs

    def get_local_fn(self, name, typs=[]):
        if name in self._local_funcs:
            fns = self._local_funcs[name]
        else:
            if name in _global_funcs:
                key = []
                for typ in typs:
                    if typ.is_pointer():
                        key.append(type(typ.arg))
                    else:
                        key.append(typ)
                fn_stm = get_global_function(name, key)
                self.register_local_func(fn_stm)
                fns = self._local_funcs[name]
            else:
                raise CompileError("Function %s doesnt exist." % name)

        loc_key = []
        for k in typs:
            if k.is_pointer():
                loc_key.append(k.arg.type_name())
            else:
                loc_key.append(k.type_name())

        loc_key = tuple(loc_key)
        if loc_key in fns:
            return fns[loc_key]
        loc_key = tuple([None] * len(typs))
        if loc_key in fns:
            return fns[loc_key]

        raise CompileError("Local function %s not found." % name)

    def has_kernel(self, name):
        if name in _global_kernels:
            return True
        for k in self._kernels:
            if k.name == name:
                return True
        return False

    def get_kernel(self, name, key):
        if has_global_kernel(name, key):
            global_kernel = get_global_kernel(name, key, self._iset, self._fma)
            self._global_kernels.add(global_kernel)
            return global_kernel

        for k in self._kernels:
            if k.name == name and len(key) == len(k.func_args):
                for arg_val, arg_class in zip(k.func_args, key):
                    if isinstance(arg_val, ComplexArgument) and not arg_val.is_pointer():
                        arg_val = PointerArg(arg_val)
                    if self._tname(arg_val) != self._tname(arg_class):
                        break
                else:
                    return k

    def has_built_in(self, name):
        return name in _built_ins

    def get_built_in(self, name, key):
        if name in _built_ins:
            fns, right_keys = _built_ins[name]
            if key in fns:
                return fns[key]
        return None

    def has_right_key_builtin(self, name, key):
        fns, right_keys = _built_ins[name]
        return key in right_keys

    def has_struct(self, name):
        return get_user_type_factory(name) is not None

    def register_local_func(self, func_stm):
        key = tuple(arg.type_name for arg in func_stm.args)
        self._set_last_stm(func_stm)
        if func_stm.name in self._local_funcs:
            fun = self._local_funcs[func_stm.name]
            fun[key] = func_stm
        else:
            self._local_funcs[func_stm.name] = {key: func_stm}

    def _set_last_stm(self, func_stm):
        if len(func_stm.body) > 0:
            if func_stm.body[-1].is_return():
                func_stm.body[-1].last_stm = True

    def create_local_scope(self, fname, body_stms):
        locs = LocalArgs()
        locs.add_free_args(self._locals_stack[-1].grab_free_args())
        self._locals_stack.append(locs)
        label = generate_name('%s_end_label' % fname)
        self._return_labels.append(label)
        self._ret_types.append(None)
        self._loc_vars.append((defaultdict(list), defaultdict(list)))
        self._analyze_stms(body_stms)
        self._store_records.append(defaultdict(int))

    def destroy_local_scope(self):
        self._return_labels.pop()
        self._ret_types.pop()
        locs = self._locals_stack.pop()
        self._locals_stack[-1].add_free_args(iter(locs))
        self._loc_vars.pop()
        stores = self._store_records.pop()
        return stores

    def get_return_type(self):
        return self._ret_types[-1]

    def return_label(self):
        return self._return_labels[-1]

    def register_ret_type(self, ret_types):
        rets = self._ret_types[-1]
        if rets is None:
            self._ret_types[-1] = ret_types
        else:
            if len(rets) != len(ret_types):
                raise CompileError("Expected %i return values got %i." % (len(rets), len(ret_types)))
            for r, e in zip(rets, ret_types):
                if r.type_name() != e.type_name():
                    raise CompileError("Wrong return type got %s expected %s." %
                                       (e.type_name(), r.type_name()))

    def allocate_regs(self, regs):
        for reg in regs:
            if isinstance(reg, tuple):
                self._allocate_regs(reg)
            else:
                self._allocate_regs((reg,))

    def _allocate_regs(self, regs):
        for reg in regs:
            if self.regs.is_xmm(reg):
                self._xmm.remove(reg)
                self._ymm.remove('y' + reg[1:])
                if self.cpu.AVX512F:
                    self._zmm.remove('z' + reg[1:])
            elif self.regs.is_ymm(reg):
                self._ymm.remove(reg)
                self._xmm.remove('x' + reg[1:])
                if self.cpu.AVX512F:
                    self._zmm.remove('z' + reg[1:])
            elif self.regs.is_zmm(reg):
                self._zmm.remove(reg)
                self._xmm.remove('x' + reg[1:])
                self._ymm.remove('y' + reg[1:])
            elif self.regs.is_mask(reg):
                self._k.remove(reg)
            elif self.regs.is_reg32(reg):
                self._general.remove(reg)
                self._general64.remove(self.regs.t_32_to_64(reg))
            elif self.regs.is_reg64(reg):
                self._general64.remove(reg)
                self._general.remove(self.regs.t_64_to_32(reg))
            else:
                raise CompileError("Unknown reg(%s) to allocate!" % reg)

    def _analyze_stms(self, stms):
        read_vars, store_vars = self._loc_vars[-1]
        for index, stm in enumerate(stms):
            stm.analyze_vars(self, index, read_vars, store_vars)


def generate(statements, args=[], standalone=True, name=None, func_args=[],
             kernels=[], optimize=False, iset=ISet.AVX2, fma=True, nthreads=1):

    cgen = CodeGenerator()
    return cgen.generate_asm(statements,
                             args=args,
                             standalone=standalone,
                             name=name,
                             func_args=func_args,
                             kernels=kernels,
                             optimize=optimize,
                             iset=iset,
                             fma=fma,
                             nthreads=nthreads)
