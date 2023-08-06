
import x86
from .cgen import register_arg_factory
from .args import Argument
from .dbl_arg import Float64Arg, float64
from .mask import MaskF64x2Arg, MaskF64x3Arg, MaskF64x4Arg, MaskF64x8Arg
from .holders import CompileError


class float64x2:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (float64(), float64())
        elif len(args) == 1:
            self.values = (float64(args[0]), float64(args[0]))
        else:
            self.values = (float64(args[0]), float64(args[1]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = float64(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s" % (repr(v[0]), repr(v[1]))


class float64x3:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (float64(), float64(), float64())
        elif len(args) == 1:
            self.values = (float64(args[0]), float64(args[0]), float64(args[0]))
        else:
            self.values = (float64(args[0]), float64(args[1]), float64(args[2]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = float64(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s %s" % (repr(v[0]), repr(v[1]), repr(v[2]))


class float64x4:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (float64(), float64(), float64(), float64())
        elif len(args) == 1:
            self.values = (float64(args[0]), float64(args[0]), float64(args[0]), float64(args[0]))
        else:
            self.values = (float64(args[0]), float64(args[1]), float64(args[2]), float64(args[3]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = float64(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s %s %s" % (repr(v[0]), repr(v[1]), repr(v[2]), repr(v[3]))


class float64x8:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = tuple([float64()] * 8)
        elif len(args) == 1:
            self.values = tuple([float64(args[0])] * 8)
        elif len(args) == 8:
            self.values = tuple(float64(a) for a in args)
        else:
            raise ValueError("Constructor for type float64x8 only accept 0, 1 or 8 arguments.", args)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = float64(value)
        self.values = tuple(v)

    def __repr__(self):
        vals = ' '.join(repr(v) for v in self.values)
        return "%s" % vals


class Float64VecBase(Argument):

    def data_sec_repr(self):
        vals = ', '.join(repr(v) for v in self._value.values)
        align = 2
        length = (len(self) + align - 1) & ~(align - 1)
        return 'double %s[%i] = %s\n' % (self._name, length, vals)

    def set_ds_value(self, ds, val, name=None):
        if not isinstance(val, type(self._value)):
            raise TypeError("%s argument expected, got %s" % (type(self._value), type(val)))
        name = self._name if name is None else name
        ds[name] = val.values

    def get_ds_value(self, ds, name=None):
        name = self._name if name is None else name
        return type(self._value)(*ds[name])

    @property
    def value(self):
        return self._value

    def load_cmd(self, cgen, name=None, ptr_reg=None):
        name = self.name if name is None else name

        if len(self) == 2:
            xmms = cgen.register('xmm')
            code = cgen.gen.load_f64x2(xmms, name=name, ptr_reg=ptr_reg)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX or cgen.cpu.AVX512F:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_f64x4(xmms, name=name, ptr_reg=ptr_reg)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_f64x2(xmm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_f64x2(xmm2, name=name, ptr_reg=ptr_reg, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                xmms = cgen.register('zmm')
                code = cgen.gen.load_f64x8(xmms, name=name, ptr_reg=ptr_reg)
            elif cgen.cpu.AVX:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_f64x4(ymm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_f64x4(ymm2, name=name, ptr_reg=ptr_reg, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_f64x2(xmm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_f64x2(xmm2, name=name, ptr_reg=ptr_reg, offset=16)
                code += cgen.gen.load_f64x2(xmm3, name=name, ptr_reg=ptr_reg, offset=32)
                code += cgen.gen.load_f64x2(xmm4, name=name, ptr_reg=ptr_reg, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms, name=None):
        name = self.name if name is None else name

        if len(self) == 2:
            code = cgen.gen.store_f64x2(xmms, name=name)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX or cgen.cpu.AVX512F:
                code = cgen.gen.store_f64x4(xmms, name=name)
            else:
                code = cgen.gen.store_f64x2(xmms[0], name=name)
                code += cgen.gen.store_f64x2(xmms[1], name=name, offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                code = cgen.gen.store_f64x8(xmms, name=name)
            elif cgen.cpu.AVX:
                code = cgen.gen.store_f64x4(xmms[0], name=name)
                code += cgen.gen.store_f64x4(xmms[1], name=name, offset=32)
            else:
                code = cgen.gen.store_f64x2(xmms[0], name=name)
                code += cgen.gen.store_f64x2(xmms[1], name=name, offset=16)
                code += cgen.gen.store_f64x2(xmms[2], name=name, offset=32)
                code += cgen.gen.store_f64x2(xmms[3], name=name, offset=48)

        return code

    def fma_supported(self, cgen):
        if len(self) > 4 and not (cgen.cpu.AVX or cgen.cpu.AVX512F):
            return False
        return True

    def can_operate_with_const(self, cgen, op, value):
        return isinstance(value, (int, float)) and op == '*'

    def can_operate_with_memory(self, cgen, arg, op):
        if isinstance(arg, Float64Arg) and op == '*':
            return True
        return isinstance(arg, type(self)) and op in ('+', '-', '/', '*', '>', '<', '==', '<=', '>=', '!=')

    def can_operate_with_arg(self, cgen, arg, op):
        if isinstance(arg, Float64Arg) and op == '*':
            return True
        return isinstance(arg, type(self)) and op in ('+', '-', '/', '*', '>', '<', '==', '<=', '>=', '!=')

    def arith_with_const(self, cgen, reg, op, value):
        arg = type(self)(value=type(self._value)(value))
        const_arg = cgen.create_const(arg)
        return self.arith_with_memory(cgen, reg, op, const_arg)

    def arith_with_memory(self, cgen, xmms, op, arg):
        if len(self) == 2:
            if cgen.cpu.AVX512F and op in ('>', '<', '==', '<=', '>=', '!='):
                dst_xmms = cgen.register('mask')
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_f64x2(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX512F and op in ('>', '<', '==', '<=', '>=', '!='):
                dst_xmms = cgen.register('mask')
                code = cgen.gen.arith_f64x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
            elif cgen.cpu.AVX or cgen.cpu.AVX512F:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_f64x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_f64x2(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x2(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                if op in ('>', '<', '==', '<=', '>=', '!='):
                    dst_xmms = cgen.register('mask')
                else:
                    dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('zmm')
                code = cgen.gen.arith_f64x8(xmms, op, name=arg.name, dst_reg=dst_xmms)
            elif cgen.cpu.AVX:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_f64x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=32)
            else:
                if cgen.can_destruct(xmms):
                    dst_xmms = xmms
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_f64x2(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x2(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
                code += cgen.gen.arith_f64x2(xmms[2], op, name=arg.name, dst_reg=dst_xmms[2], offset=32)
                code += cgen.gen.arith_f64x2(xmms[3], op, name=arg.name, dst_reg=dst_xmms[3], offset=48)

        if op in ('>', '<', '==', '<=', '>=', '!='):
            int_type = {2: MaskF64x2Arg, 3: MaskF64x3Arg, 4: MaskF64x4Arg, 8: MaskF64x8Arg}
            return code, dst_xmms, int_type[len(self)]
        else:
            return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):
        if len(self) == 2:
            if cgen.cpu.AVX512F and op in ('>', '<', '==', '<=', '>=', '!='):
                dst_xmms = cgen.register('mask')
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_f64x2(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX512F and op in ('>', '<', '==', '<=', '>=', '!='):
                dst_xmms = cgen.register('mask')
                code = cgen.gen.arith_f64x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            elif cgen.cpu.AVX or cgen.cpu.AVX512F:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_f64x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_f64x2(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x2(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                if op in ('>', '<', '==', '<=', '>=', '!='):
                    dst_xmms = cgen.register('mask')
                else:
                    dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('zmm')
                code = cgen.gen.arith_f64x8(xmms1, op, zmm2=xmms2, dst_reg=dst_xmms)
            elif cgen.cpu.AVX:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_f64x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
            else:
                if cgen.can_destruct(xmms1):
                    dst_xmms = xmms1
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_f64x2(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x2(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
                code += cgen.gen.arith_f64x2(xmms1[2], op, xmm2=xmms2[2], dst_reg=dst_xmms[2])
                code += cgen.gen.arith_f64x2(xmms1[3], op, xmm2=xmms2[3], dst_reg=dst_xmms[3])

        if op in ('>', '<', '==', '<=', '>=', '!='):
            int_type = {2: MaskF64x2Arg, 3: MaskF64x3Arg, 4: MaskF64x4Arg, 8: MaskF64x8Arg}
            return code, dst_xmms, int_type[len(self)]
        else:
            return code, dst_xmms, type(self)

    def _mem_broadcast(self, cgen, arg2):
        if len(self) == 2:
            code, dst_xmms, arg_typ = arg2.load_cmd(cgen)
            code += cgen.gen.broadcast_f64(dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX:
                dst_xmms = cgen.register('ymm')
                code = 'vbroadcastsd %s, qword[%s]\n' % (dst_xmms, arg2.name)
            else:
                xmm1 = cgen.register('xmm')
                code, xmm, arg_typ = arg2.load_cmd(cgen)
                code += cgen.gen.broadcast_f64(xmm)
                code += cgen.gen.move_reg(xmm1, xmm)
                dst_xmms = (xmm, xmm1)
        else:
            if cgen.cpu.AVX:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = 'vbroadcastsd %s, qword[%s]\n' % (ymm1, arg2.name)
                code += cgen.gen.move_reg(ymm2, ymm1)
                dst_xmms = (ymm1, ymm2)
            else:
                xmm2, xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code, xmm1, arg_typ = arg2.load_cmd(cgen)
                code += cgen.gen.broadcast_f64(xmm1)
                code += cgen.gen.move_reg(xmm2, xmm1)
                code += cgen.gen.move_reg(xmm3, xmm1)
                code += cgen.gen.move_reg(xmm4, xmm1)
                dst_xmms = (xmm1, xmm2, xmm3, xmm4)
        return code, dst_xmms

    def _reg_broadcast(self, cgen, arg2, xmm2):
        if len(self) == 2:
            dst_xmms = cgen.register('xmm')
            if cgen.cpu.AVX or cgen.cpu.AVX512F:
                code = "vshufpd %s, %s, %s, 0\n" % (dst_xmms, xmm2, xmm2)
            else:
                code = "movaps %s, %s\n" % (dst_xmms, xmm2)
                code += "shufpd %s, %s, 0\n" % (dst_xmms, dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = cgen.register('ymm')
                code = 'vbroadcastsd %s, %s\n' % (dst_xmms, xmm2)
            elif cgen.cpu.AVX:
                dst_xmms = cgen.register('ymm')
                code = cgen.gen.broadcast_f64(xmm2)
                code += 'vperm2f128 %s, %s, %s, 0\n' % (dst_xmms, 'y' + xmm2[1:], 'y' + xmm2[1:])
            else:
                dst_xmms = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.broadcast_f64(xmm2)
                code += cgen.gen.move_reg(dst_xmms[0], xmm2)
                code += cgen.gen.move_reg(dst_xmms[1], xmm2)
        else:
            if cgen.cpu.AVX512F:
                dst_xmms = cgen.register('zmm')
                code = 'vbroadcastsd %s, %s\n' % (dst_xmms, xmm2)
            elif cgen.cpu.AVX2:
                dst_xmms = cgen.register('ymm'), cgen.register('ymm')
                code = 'vbroadcastsd %s, %s\n' % (dst_xmms[0], xmm2)
                code += cgen.gen.move_reg(dst_xmms[1], dst_xmms[0])
            elif cgen.cpu.AVX:
                dst_xmms = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.broadcast_f64(xmm2)
                code += 'vperm2f128 %s, %s, %s, 0\n' % (dst_xmms[0], 'y' + xmm2[1:], 'y' + xmm2[1:])
                code += cgen.gen.move_reg(dst_xmms[1], dst_xmms[0])
            else:
                dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.broadcast_f64(xmm2)
                code += cgen.gen.move_reg(dst_xmms[0], xmm2)
                code += cgen.gen.move_reg(dst_xmms[1], xmm2)
                code += cgen.gen.move_reg(dst_xmms[2], xmm2)
                code += cgen.gen.move_reg(dst_xmms[3], xmm2)
        return code, dst_xmms

    def _avx512_vec_scalar_mul(self, cgen, reg1, arg2):
        if len(self) == 2:
            dst_reg = reg1 if cgen.can_destruct(reg1) else cgen.register('xmm')
        elif len(self) in (3, 4):
            dst_reg = reg1 if cgen.can_destruct(reg1) else cgen.register('ymm')
        elif len(self) == 8:
            dst_reg = reg1 if cgen.can_destruct(reg1) else cgen.register('zmm')
        else:
            raise ValueError("AVX512 vector scalar multiplication!", self)
        code = 'vmulpd %s, %s, qword[%s]\n' % (dst_reg, reg1, arg2.name)
        return code, dst_reg, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if isinstance(arg2, Float64Arg):  # scalar vector multiplication
            if reg2 is None:
                if cgen.cpu.AVX512F:
                    return self._avx512_vec_scalar_mul(cgen, reg1, arg2)
                brd_code, reg2 = self._mem_broadcast(cgen, arg2)
            else:
                brd_code, reg2 = self._reg_broadcast(cgen, arg2, reg2)
            code, dst_xmms, arg_type = self.arith_with_arg(cgen, reg1, arg2, reg2, op)
            if dst_xmms != reg2:
                cgen.release_reg(reg2)
            return brd_code + code, dst_xmms, arg_type

        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def do_unary_op(self, cgen, xmms, op):
        if op not in ('+', '-'):
            raise CompileError("Unsupported unary operation %s for %s type!" % (str(op), str(self)))

        if op == '+':
            return '', xmms, type(self)

        def un_op(reg1, reg2):
            if cgen.cpu.AVX or cgen.cpu.AVX512F:
                code = 'vxorpd %s, %s, %s\n' % (reg1, reg1, reg1)
                code += 'vsubpd %s, %s, %s\n' % (reg1, reg1, reg2)
            else:
                code = 'xorpd %s, %s\n' % (reg1, reg1)
                code += 'subpd %s, %s\n' % (reg1, reg2)
            return code

        if len(self) == 2:
            xmms1 = cgen.register('xmm')
            code = un_op(xmms1, xmms)
        elif len(self) in (3, 4):
            if cgen.cpu.AVX or cgen.cpu.AVX512F:
                xmms1 = cgen.register('ymm')
                code = un_op(xmms1, xmms)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = un_op(xmm1, xmms[0])
                code += un_op(xmm2, xmms[1])
                xmms1 = (xmm1, xmm2)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                xmms1 = cgen.register('zmm')
                code = un_op(xmms1, xmms)
            elif cgen.cpu.AVX:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = un_op(ymm1, xmms[0])
                code += un_op(ymm2, xmms[1])
                xmms1 = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = un_op(xmm1, xmms[0])
                code += un_op(xmm2, xmms[1])
                code += un_op(xmm3, xmms[2])
                code += un_op(xmm4, xmms[3])
                xmms1 = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms1, type(self)

    def _cpu_fma(self, cgen, arg2, op, reverse, arg3, reg1, reg2, reg3=None):
        negate = reverse and op == '-'
        if negate:
            op = '+'
        if cgen.can_destruct(reg1) or cgen.can_destruct(reg2):
            if not cgen.can_destruct(reg1) and cgen.can_destruct(reg2):
                reg1, reg2 = reg2, reg1
            if len(self) == 2:
                code = cgen.gen.fma_f64x2_213(reg1, reg2, op, negate, xmm3=reg3, name=arg3.name)
            elif len(self) in (3, 4):
                code = cgen.gen.fma_f64x4_213(reg1, reg2, op, negate, ymm3=reg3, name=arg3.name)
            elif len(self) == 8:
                if cgen.cpu.AVX512F:
                    code = cgen.gen.fma_f64x8_213(reg1, reg2, op, negate, zmm3=reg3, name=arg3.name)
                else:
                    if reg3 is not None:
                        code = cgen.gen.fma_f64x4_213(reg1[0], reg2[0], op, negate, ymm3=reg3[0])
                        code += cgen.gen.fma_f64x4_213(reg1[1], reg2[1], op, negate, ymm3=reg3[1])
                    else:
                        code = cgen.gen.fma_f64x4_213(reg1[0], reg2[0], op, negate, name=arg3.name)
                        code += cgen.gen.fma_f64x4_213(reg1[1], reg2[1], op, negate, name=arg3.name, offset=32)
            dest_reg = reg1
        elif reg3 is not None and cgen.can_destruct(reg3):
            if len(self) == 2:
                code = cgen.gen.fma_f64x2_231(reg3, reg1, op, negate, xmm3=reg2)
            elif len(self) in (3, 4):
                code = cgen.gen.fma_f64x4_231(reg3, reg1, op, negate, ymm3=reg2)
            elif len(self) == 8:
                if cgen.cpu.AVX512F:
                    code = cgen.gen.fma_f64x8_231(reg3, reg1, op, negate, zmm3=reg2)
                else:
                    code = cgen.gen.fma_f64x4_231(reg3[0], reg1[0], op, negate, ymm3=reg2[0])
                    code += cgen.gen.fma_f64x4_231(reg3[1], reg1[1], op, negate, ymm3=reg2[1])
            dest_reg = reg3
        else:
            if len(self) == 2:
                xmm4 = cgen.register('xmm')
                code = cgen.gen.move_reg(xmm4, reg1)
                code += cgen.gen.fma_f64x2_213(xmm4, reg2, op, negate, xmm3=reg3, name=arg3.name)
                dest_reg = xmm4
            elif len(self) in (3, 4):
                xmm4 = cgen.register('ymm')
                code = cgen.gen.move_reg(xmm4, reg1)
                code += cgen.gen.fma_f64x4_213(xmm4, reg2, op, negate, ymm3=reg3, name=arg3.name)
                dest_reg = xmm4
            elif len(self) == 8:
                if cgen.cpu.AVX512F:
                    xmm4 = cgen.register('zmm')
                    code = cgen.gen.move_reg(xmm4, reg1)
                    code += cgen.gen.fma_f64x8_213(xmm4, reg2, op, negate, zmm3=reg3, name=arg3.name)
                    dest_reg = xmm4
                else:
                    xmms = (cgen.register('ymm'), cgen.register('ymm'))
                    code = cgen.gen.move_reg(xmms[0], reg1[0])
                    code += cgen.gen.move_reg(xmms[1], reg1[1])
                    if reg3 is not None:
                        code += cgen.gen.fma_f64x4_213(xmms[0], reg2[0], op, negate, ymm3=reg3)
                        code += cgen.gen.fma_f64x4_213(xmms[1], reg2[1], op, negate, ymm3=reg3)
                    else:
                        code += cgen.gen.fma_f64x4_213(xmms[0], reg2[0], op, negate, name=arg3.name)
                        code += cgen.gen.fma_f64x4_213(xmms[1], reg2[1], op, negate, name=arg3.name, offset=32)
                    dest_reg = xmms

        return code, dest_reg, type(self)

    def _no_cpu_fma_2(self, cgen, arg2, op, reverse, arg3, reg1, reg2, dst_xmm, reg3=None, offset=None):
        code = cgen.gen.arith_f64x2(reg1, '*', xmm2=reg2, dst_reg=dst_xmm)
        if reverse and op == '-':
            xmm5 = cgen.register('xmm')
            if reg3 is not None:
                code += cgen.gen.arith_f64x2(reg3, op, xmm2=dst_xmm, dst_reg=xmm5)
            else:
                code += cgen.gen.load_f64x2(xmm5, name=arg3.name, offset=offset)
                code += cgen.gen.arith_f64x2(xmm5, op, xmm2=dst_xmm)
            if dst_xmm != reg1:
                cgen.release_reg(dst_xmm)
            dst_xmm = xmm5
        else:
            code += cgen.gen.arith_f64x2(dst_xmm, op, xmm2=reg3, name=arg3.name, offset=offset)
        return code, dst_xmm, type(self)

    def _no_cpu_fma_4(self, cgen, arg2, op, reverse, arg3, reg1, reg2, dst_ymm, reg3=None, offset=None):
        code = cgen.gen.arith_f64x4(reg1, '*', xmm2=reg2, dst_reg=dst_ymm)
        if reverse and op == '-':
            ymm5 = cgen.register('ymm')
            if reg3 is not None:
                code += cgen.gen.arith_f64x4(reg3, op, xmm2=dst_ymm, dst_reg=ymm5)
            else:
                code += cgen.gen.load_f64x4(ymm5, name=arg3.name, offset=offset)
                code += cgen.gen.arith_f64x4(ymm5, op, xmm2=dst_ymm)
            if dst_ymm != reg1:
                cgen.release_reg(dst_ymm)
            dst_ymm = ymm5
        else:
            code += cgen.gen.arith_f64x4(dst_ymm, op, xmm2=reg3, name=arg3.name, offset=offset)
        return code, dst_ymm, type(self)

    def _no_cpu_fma_8(self, cgen, arg2, op, reverse, arg3, reg1, reg2, dst_zmm, reg3=None, offset=None):
        code = cgen.gen.arith_f64x8(reg1, '*', zmm2=reg2, dst_reg=dst_zmm)
        if reverse and op == '-':
            zmm5 = cgen.register('zmm')
            if reg3 is not None:
                code += cgen.gen.arith_f64x8(reg3, op, zmm2=dst_zmm, dst_reg=zmm5)
            else:
                code += cgen.gen.load_f64x8(zmm5, name=arg3.name, offset=offset)
                code += cgen.gen.arith_f64x8(zmm5, op, zmm2=dst_zmm)
            if dst_zmm != reg1:
                cgen.release_reg(dst_zmm)
            dst_zmm = zmm5
        else:
            code += cgen.gen.arith_f64x8(dst_zmm, op, zmm2=reg3, name=arg3.name, offset=offset)
        return code, dst_zmm, type(self)

    def _no_cpu_fma(self, cgen, arg2, op, reverse, arg3, reg1, reg2, reg3=None):
        if len(self) == 2:
            dst_xmm = reg1 if cgen.can_destruct(reg1) else cgen.register('xmm')
            return self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1, reg2, dst_xmm, reg3=reg3)
        elif len(self) in (3, 4):
            if cgen.cpu.AVX or cgen.cpu.AVX512F:
                dst_xmm = reg1 if cgen.can_destruct(reg1) else cgen.register('ymm')
                code, xmms, typ = self._no_cpu_fma_4(cgen, arg2, op, reverse, arg3, reg1, reg2, dst_xmm, reg3=reg3)
                return code, xmms, typ
            else:
                dst_xmms = reg1 if cgen.can_destruct(reg1) else (cgen.register('xmm'), cgen.register('xmm'))
                if reg3 is not None:
                    code4, reg4, typ4 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[0], reg2[0], dst_xmms[0], reg3=reg3[0])
                    code5, reg5, typ5 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[1], reg2[1], dst_xmms[1], reg3=reg3[1])
                else:
                    code4, reg4, typ4 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[0], reg2[0], dst_xmms[0])
                    code5, reg5, typ5 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[1], reg2[1], dst_xmms[1], offset=16)
                return code4 + code5, (reg4, reg5), type(self)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                dst_zmm = reg1 if cgen.can_destruct(reg1) else cgen.register('zmm')
                code, xmms, typ = self._no_cpu_fma_8(cgen, arg2, op, reverse, arg3, reg1, reg2, dst_zmm, reg3=reg3)
                return code, xmms, typ
            elif cgen.cpu.AVX:
                dst_xmms = reg1 if cgen.can_destruct(reg1) else (cgen.register('ymm'), cgen.register('ymm'))
                if reg3 is not None:
                    code4, reg4, typ4 = self._no_cpu_fma_4(cgen, arg2, op, reverse, arg3, reg1[0], reg2[0], dst_xmms[0], reg3=reg3[0])
                    code5, reg5, typ5 = self._no_cpu_fma_4(cgen, arg2, op, reverse, arg3, reg1[1], reg2[1], dst_xmms[1], reg3=reg3[1])
                else:
                    code4, reg4, typ4 = self._no_cpu_fma_4(cgen, arg2, op, reverse, arg3, reg1[0], reg2[0], dst_xmms[0])
                    code5, reg5, typ5 = self._no_cpu_fma_4(cgen, arg2, op, reverse, arg3, reg1[1], reg2[1], dst_xmms[1], offset=32)
                return code4 + code5, (reg4, reg5), type(self)
            else:
                if cgen.can_destruct(reg1):
                    dst_xmms = reg1
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                if reg3 is not None:
                    code4, reg4, typ4 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[0], reg2[0], dst_xmms[0], reg3=reg3[0])
                    code5, reg5, typ5 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[1], reg2[1], dst_xmms[1], reg3=reg3[1])
                    code6, reg6, typ6 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[2], reg2[2], dst_xmms[2], reg3=reg3[2])
                    code7, reg7, typ7 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[3], reg2[3], dst_xmms[3], reg3=reg3[3])
                else:
                    code4, reg4, typ4 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[0], reg2[0], dst_xmms[0])
                    code5, reg5, typ5 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[1], reg2[1], dst_xmms[1], offset=16)
                    code6, reg6, typ6 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[2], reg2[2], dst_xmms[2], offset=32)
                    code7, reg7, typ7 = self._no_cpu_fma_2(cgen, arg2, op, reverse, arg3, reg1[3], reg2[3], dst_xmms[3], offset=48)
                return code4 + code5 + code6 + code7, (reg4, reg5, reg6, reg7), type(self)

    def fma_cmd(self, cgen, arg2, op, reverse, arg3, reg1, reg2, reg3=None):
        # arg1 * arg2 +/- arg3
        # arg3 +/- arg1 * arg2
        brd_code = ''
        if isinstance(arg2, Float64Arg):
            brd_code, reg2 = self._reg_broadcast(cgen, arg2, reg2)
        if cgen.cpu.FMA:
            code, dst_regs, arg_typ = self._cpu_fma(cgen, arg2, op, reverse, arg3, reg1, reg2, reg3=reg3)
        else:
            code, dst_regs, arg_typ = self._no_cpu_fma(cgen, arg2, op, reverse, arg3, reg1, reg2, reg3=reg3)
        if isinstance(arg2, Float64Arg):
            if dst_regs != reg2:
                cgen.release_reg(reg2)
        return brd_code + code, dst_regs, arg_typ

    def is_subscriptable(self):
        return True

    def load_item_cmd(self, cgen, index=None, reg=None, ptr_reg=None):
        if index is not None:
            if index < 0 or index > len(self) - 1:
                raise IndexError("Index is out of bounds! ", index, type(self), self.name)

        def load_item(xmm, ptr, reg):
            inst = 'vmovsd' if cgen.cpu.AVX or cgen.cpu.AVX512F else 'movsd'
            if cgen.regs.is_reg32(reg):
                reg = cgen.regs.t_32_to_64(reg)
            code = '%s %s, qword[%s + %s * 8]\n' % (inst, xmm, ptr, reg)
            return code

        xmm = cgen.register('xmm')

        if ptr_reg is None:
            if index is None:
                ptr = cgen.register('pointer')
                code = cgen.gen.load_addr(ptr, self.name)
                code += load_item(xmm, ptr, reg)
                cgen.release_reg(ptr)
            else:
                code = cgen.gen.load_f64(xmm, name=self.name, offset=index * 8)
        else:
            if index is None:
                code = load_item(xmm, ptr_reg, reg)
            else:
                code = cgen.gen.load_f64(xmm, ptr_reg=ptr_reg, offset=index * 8)
        return code, xmm, Float64Arg

    def store_item_cmd(self, cgen, arg_type, xmm, index=None, reg=None, ptr_reg=None):

        if arg_type is not Float64Arg:
            raise ValueError("float64 item argument expected!", self, arg_type)

        if index is not None:
            if index < 0 or index > len(self) - 1:
                raise IndexError("Index is out of bounds! ", index, type(self), self.name)

        def store_item(xmm, ptr, reg):
            inst = 'vmovsd' if cgen.cpu.AVX or cgen.cpu.AVX512F else 'movsd'
            if cgen.regs.is_reg32(reg):
                reg = cgen.regs.t_32_to_64(reg)
            code = '%s qword[%s + %s * 8], %s\n' % (inst, ptr, reg, xmm)
            return code

        if ptr_reg is None:
            if index is None:
                ptr = cgen.register('pointer')
                code = cgen.gen.load_addr(ptr, self.name)
                code += store_item(xmm, ptr, reg)
                cgen.release_reg(ptr)
            else:
                code = cgen.gen.store_f64(xmm, name=self.name, offset=index * 8)
        else:
            if index is None:
                code = store_item(xmm, ptr_reg, reg)
            else:
                code = cgen.gen.store_f64(xmm, ptr_reg=ptr_reg, offset=index * 8)
        return code

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F and len(self) == 8:
            return 'zmm'
        elif (cgen.cpu.AVX or cgen.cpu.AVX512F) and len(self) in (3, 4):
            return 'ymm'
        else:
            return 'xmm'

    def is_multi_part(self, cgen):
        if cgen.cpu.AVX512F:
            return False
        elif cgen.cpu.AVX:
            return len(self) > 4
        else:
            return len(self) > 2

    def set_array_item(self, addr, value):
        if not isinstance(value, type(self._value)):
            raise TypeError("Expected %s got %s" % (type(self._value), type(value)))
        x86.SetDouble(addr, value.values, 0)

    def get_array_item(self, addr):
        return type(self._value)(*x86.GetDouble(addr, 0, len(self)))

    @property
    def itemsize(self):
        return 8 * len(self)


class Float64x2Arg(Float64VecBase):
    def __init__(self, name=None, value=float64x2()):
        super(Float64x2Arg, self).__init__(name)
        if not isinstance(value, float64x2):
            raise TypeError("float64x2 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 16

    def stack_size(self, cpu):
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'float64x2'

    def load_item_from_array(self, cgen, ptr_reg):
        xmm = cgen.register('xmm')
        code = cgen.gen.load_f64x2(xmm, ptr_reg=ptr_reg)
        return code, xmm, Float64x2Arg

    def store_item_to_array(self, cgen, ptr_reg, xmm):
        return cgen.gen.store_f64x2(xmm, ptr_reg=ptr_reg)


class Float64x3Arg(Float64VecBase):
    def __init__(self, name=None, value=float64x3()):
        super(Float64x3Arg, self).__init__(name)
        if not isinstance(value, float64x3):
            raise TypeError("float64x3 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 32

    def stack_size(self, cpu):
        return 32

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'float64x3'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            xmms = cgen.register('ymm')
            code = cgen.gen.load_f64x4(xmms, ptr_reg=ptr_reg, align=False)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_f64x2(xmm1, ptr_reg=ptr_reg, align=False)
            code += cgen.gen.load_f64x2(xmm2, ptr_reg=ptr_reg, offset=16, align=False)
            xmms = (xmm1, xmm2)
        return code, xmms, Float64x3Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = cgen.gen.store_f64x2('x' + xmms[1:], ptr_reg=ptr_reg, align=False)
            if cgen.cpu.AVX512F:
                code += 'vextractf64x2 %s, %s, 1\n' % ('x' + xmms[1:], xmms)
            else:
                code += 'vextractf128 %s, %s, 1\n' % ('x' + xmms[1:], xmms)
            code += cgen.gen.store_f64('x' + xmms[1:], ptr_reg=ptr_reg, offset=16)
        else:
            code = cgen.gen.store_f64x2(xmms[0], ptr_reg=ptr_reg, align=False)
            code += cgen.gen.store_f64(xmms[1], ptr_reg=ptr_reg, offset=16)
        return code


class Float64x4Arg(Float64VecBase):
    def __init__(self, name=None, value=float64x4()):
        super(Float64x4Arg, self).__init__(name)
        if not isinstance(value, float64x4):
            raise TypeError("float64x4 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 32

    def stack_size(self, cpu):
        return 32

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'float64x4'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            xmms = cgen.register('ymm')
            code = cgen.gen.load_f64x4(xmms, ptr_reg=ptr_reg, align=True)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_f64x2(xmm1, ptr_reg=ptr_reg)
            code += cgen.gen.load_f64x2(xmm2, ptr_reg=ptr_reg, offset=16)
            xmms = (xmm1, xmm2)
        return code, xmms, Float64x4Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = cgen.gen.store_f64x4(xmms, ptr_reg=ptr_reg, align=True)
        else:
            code = cgen.gen.store_f64x2(xmms[0], ptr_reg=ptr_reg)
            code += cgen.gen.store_f64x2(xmms[1], ptr_reg=ptr_reg, offset=16)
        return code


class Float64x8Arg(Float64VecBase):
    def __init__(self, name=None, value=float64x8()):
        super(Float64x8Arg, self).__init__(name)
        if not isinstance(value, float64x8):
            raise TypeError("float64x8 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 64

    def stack_size(self, cpu):
        return 64

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'float64x8'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX512F:
            xmms = cgen.register('zmm')
            code = cgen.gen.load_f64x8(xmms, ptr_reg=ptr_reg, align=True)
        elif cgen.cpu.AVX:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = cgen.gen.load_f64x4(ymm1, ptr_reg=ptr_reg, align=True)
            code += cgen.gen.load_f64x4(ymm2, ptr_reg=ptr_reg, offset=32, align=True)
            xmms = (ymm1, ymm2)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_f64x2(xmm1, ptr_reg=ptr_reg)
            code += cgen.gen.load_f64x2(xmm2, ptr_reg=ptr_reg, offset=16)
            code += cgen.gen.load_f64x2(xmm3, ptr_reg=ptr_reg, offset=32)
            code += cgen.gen.load_f64x2(xmm4, ptr_reg=ptr_reg, offset=48)
            xmms = (xmm1, xmm2, xmm3, xmm4)
        return code, xmms, Float64x8Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX512F:
            code = cgen.gen.store_f64x8(xmms, ptr_reg=ptr_reg, align=True)
        elif cgen.cpu.AVX:
            code = cgen.gen.store_f64x4(xmms[0], ptr_reg=ptr_reg, align=True)
            code += cgen.gen.store_f64x4(xmms[1], ptr_reg=ptr_reg, offset=32, align=True)
        else:
            code = cgen.gen.store_f64x2(xmms[0], ptr_reg=ptr_reg)
            code += cgen.gen.store_f64x2(xmms[1], ptr_reg=ptr_reg, offset=16)
            code += cgen.gen.store_f64x2(xmms[2], ptr_reg=ptr_reg, offset=32)
            code += cgen.gen.store_f64x2(xmms[3], ptr_reg=ptr_reg, offset=48)
        return code


float64x2.arg_class = Float64x2Arg
float64x3.arg_class = Float64x3Arg
float64x4.arg_class = Float64x4Arg
float64x8.arg_class = Float64x8Arg
register_arg_factory(Float64x2Arg, lambda: Float64x2Arg())
register_arg_factory(Float64x3Arg, lambda: Float64x3Arg())
register_arg_factory(Float64x4Arg, lambda: Float64x4Arg())
register_arg_factory(Float64x8Arg, lambda: Float64x8Arg())
