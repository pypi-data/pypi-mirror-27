
import x86
from .cgen import register_arg_factory
from .args import Argument
from .int_arg import int32, int64, Int32Arg, Int64Arg
from .mask import MaskI32x2Arg, MaskI32x3Arg, MaskI32x4Arg, MaskI32x8Arg, MaskI32x16Arg
from .mask import MaskI64x2Arg, MaskI64x3Arg, MaskI64x4Arg, MaskI64x8Arg
from .holders import CompileError


class int32x2:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (int32(), int32())
        elif len(args) == 1:
            self.values = (int32(args[0]), int32(args[0]))
        else:
            self.values = (int32(args[0]), int32(args[1]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int32(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s" % (repr(v[0]), repr(v[1]))


class int32x3:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (int32(), int32(), int32())
        elif len(args) == 1:
            self.values = (int32(args[0]), int32(args[0]), int32(args[0]))
        else:
            self.values = (int32(args[0]), int32(args[1]), int32(args[2]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int32(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s %s" % (repr(v[0]), repr(v[1]), repr(v[2]))


class int32x4:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (int32(), int32(), int32(), int32())
        elif len(args) == 1:
            self.values = (int32(args[0]), int32(args[0]), int32(args[0]), int32(args[0]))
        else:
            self.values = (int32(args[0]), int32(args[1]), int32(args[2]), int32(args[3]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int32(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s %s %s" % (repr(v[0]), repr(v[1]), repr(v[2]), repr(v[3]))


class int32x8:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = tuple([int32()] * 8)
        elif len(args) == 1:
            self.values = tuple([int32(args[0])] * 8)
        elif len(args) == 8:
            self.values = tuple(int32(a) for a in args)
        else:
            raise ValueError("Constructor for type int32x8 only accept 0, 1 or 8 arguments.", args)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int32(value)
        self.values = tuple(v)

    def __repr__(self):
        vals = ' '.join(repr(v) for v in self.values)
        return "%s" % vals


class int32x16:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = tuple([int32()] * 16)
        elif len(args) == 1:
            self.values = tuple([int32(args[0])] * 16)
        elif len(args) == 16:
            self.values = tuple(int32(a) for a in args)
        else:
            raise ValueError("Constructor for type int32x16 only accept 0, 1 or 16 arguments.", args)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int32(value)
        self.values = tuple(v)

    def __repr__(self):
        vals = ' '.join(repr(v) for v in self.values)
        return "%s" % vals


class Int32VecBase(Argument):

    def data_sec_repr(self):
        vals = ', '.join(repr(v) for v in self._value.values)
        align = 4
        length = (len(self) + align - 1) & ~(align - 1)
        return 'int32 %s[%i] = %s\n' % (self._name, length, vals)

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

        if len(self) in (2, 3, 4):
            xmms = cgen.register('xmm')
            code = cgen.gen.load_i32x4(xmms, name=name, ptr_reg=ptr_reg)
        elif len(self) == 8:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_i32x8(xmms, name=name, ptr_reg=ptr_reg)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i32x4(xmm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_i32x4(xmm2, name=name, ptr_reg=ptr_reg, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 16:
            if cgen.cpu.AVX512F:
                xmms = cgen.register('zmm')
                code = cgen.gen.load_i32x16(xmms, name=name, ptr_reg=ptr_reg)
            elif cgen.cpu.AVX2:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_i32x8(ymm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_i32x8(ymm2, name=name, ptr_reg=ptr_reg, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i32x4(xmm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_i32x4(xmm2, name=name, ptr_reg=ptr_reg, offset=16)
                code += cgen.gen.load_i32x4(xmm3, name=name, ptr_reg=ptr_reg, offset=32)
                code += cgen.gen.load_i32x4(xmm4, name=name, ptr_reg=ptr_reg, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms, name=None):
        name = self.name if name is None else name

        if len(self) in (2, 3, 4):
            code = cgen.gen.store_i32x4(xmms, name=name)
        elif len(self) == 8:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                code = cgen.gen.store_i32x8(xmms, name=name)
            else:
                code = cgen.gen.store_i32x4(xmms[0], name=name)
                code += cgen.gen.store_i32x4(xmms[1], name=name, offset=16)
        elif len(self) == 16:
            if cgen.cpu.AVX512F:
                code = cgen.gen.store_i32x16(xmms, name=name)
            elif cgen.cpu.AVX2:
                code = cgen.gen.store_i32x8(xmms[0], name=name)
                code += cgen.gen.store_i32x8(xmms[1], name=name, offset=32)
            else:
                code = cgen.gen.store_i32x4(xmms[0], name=name)
                code += cgen.gen.store_i32x4(xmms[1], name=name, offset=16)
                code += cgen.gen.store_i32x4(xmms[2], name=name, offset=32)
                code += cgen.gen.store_i32x4(xmms[3], name=name, offset=48)

        return code

    def can_operate_with_const(self, cgen, op, value):
        if not isinstance(value, int):
            return False
        if value > 127 or value < -128:
            return False
        elif op in ('>>', '<<'):
            return True
        else:
            return False

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('+', '-', '*', '&', '^', '|', '==', '>')

    def arith_with_const(self, cgen, reg, op, value):
        if len(self) in (2, 3, 4):
            dst_xmms = reg if cgen.can_destruct(reg) else cgen.register('xmm')
            code = cgen.gen.arith_i32x4_con(reg, op, value, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = reg if cgen.can_destruct(reg) else cgen.register('ymm')
                code = cgen.gen.arith_i32x8_con(reg, op, value, dst_reg=dst_xmms)
            else:
                dst_xmms = reg if cgen.can_destruct(reg) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i32x4_con(reg[0], op, value, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4_con(reg[1], op, value, dst_reg=dst_xmms[1])
        elif len(self) == 16:
            if cgen.cpu.AVX512F:
                dst_xmms = reg if cgen.can_destruct(reg) else cgen.register('zmm')
                code = cgen.gen.arith_i32x16_con(reg, op, value, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2:
                dst_xmms = reg if cgen.can_destruct(reg) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_i32x8_con(reg[0], op, value, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x8_con(reg[1], op, value, dst_reg=dst_xmms[1])
            else:
                if cgen.can_destruct(reg):
                    dst_xmms = reg
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_i32x4_con(reg[0], op, value, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4_con(reg[1], op, value, dst_reg=dst_xmms[1])
                code += cgen.gen.arith_i32x4_con(reg[2], op, value, dst_reg=dst_xmms[2])
                code += cgen.gen.arith_i32x4_con(reg[3], op, value, dst_reg=dst_xmms[3])
        return code, dst_xmms, type(self)

    def arith_with_memory(self, cgen, xmms, op, arg):
        if len(self) in (2, 3, 4):
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_i32x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
                code = cgen.gen.arith_i32x8(xmms, op, name=arg.name, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_i32x8(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i32x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 16:
            if cgen.cpu.AVX512F:
                if op in ('>', '=='):
                    dst_xmms = cgen.register('mask')
                else:
                    dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('zmm')
                code = cgen.gen.arith_i32x16(xmms, op, name=arg.name, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_i32x8(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x8(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=32)
            else:
                if cgen.can_destruct(xmms):
                    dst_xmms = xmms
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_i32x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
                code += cgen.gen.arith_i32x4(xmms[2], op, name=arg.name, dst_reg=dst_xmms[2], offset=32)
                code += cgen.gen.arith_i32x4(xmms[3], op, name=arg.name, dst_reg=dst_xmms[3], offset=48)

        if op in ('>', '=='):
            int_type = {2: MaskI32x2Arg, 3: MaskI32x3Arg, 4: MaskI32x4Arg, 8: MaskI32x8Arg, 16: MaskI32x16Arg}
            return code, dst_xmms, int_type[len(self)]
        else:
            return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):
        if len(self) in (2, 3, 4):
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_i32x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
                code = cgen.gen.arith_i32x8(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_i32x8(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i32x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 16:
            if cgen.cpu.AVX512F:
                if op in ('>', '=='):
                    dst_xmms = cgen.register('mask')
                else:
                    dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('zmm')
                code = cgen.gen.arith_i32x8(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_i32x8(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x8(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
            else:
                if cgen.can_destruct(xmms1):
                    dst_xmms = xmms1
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_i32x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
                code += cgen.gen.arith_i32x4(xmms1[2], op, xmm2=xmms2[2], dst_reg=dst_xmms[2])
                code += cgen.gen.arith_i32x4(xmms1[3], op, xmm2=xmms2[3], dst_reg=dst_xmms[3])

        if op in ('>', '=='):
            int_type = {2: MaskI32x2Arg, 3: MaskI32x3Arg, 4: MaskI32x4Arg, 8: MaskI32x8Arg, 16: MaskI32x16Arg}
            return code, dst_xmms, int_type[len(self)]
        else:
            return code, dst_xmms, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def do_unary_op(self, cgen, xmms, op):
        if op not in ('+', '-'):
            raise CompileError("Unsupported unary operation %s for %s type!" % (str(op), str(self)))

        if op == '+':
            return '', xmms, type(self)

        def un_op(reg1, reg2):
            if cgen.cpu.AVX512F:
                code = 'vpxord %s, %s, %s\n' % (reg1, reg1, reg1)
                code += 'vpsubd %s, %s, %s\n' % (reg1, reg1, reg2)
            elif cgen.cpu.AVX:
                code = 'vpxor %s, %s, %s\n' % (reg1, reg1, reg1)
                code += 'vpsubd %s, %s, %s\n' % (reg1, reg1, reg2)
            else:
                code = 'pxor %s, %s\n' % (reg1, reg1)
                code += 'psubd %s, %s\n' % (reg1, reg2)
            return code


        if len(self) in (2, 3, 4):
            xmms1 = cgen.register('xmm')
            code = un_op(xmms1, xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                xmms1 = cgen.register('ymm')
                code = un_op(xmms1, xmms)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = un_op(xmm1, xmms[0])
                code += un_op(xmm2, xmms[1])
                xmms1 = (xmm1, xmm2)
        elif len(self) == 16:
            if cgen.cpu.AVX512F:
                xmms1 = cgen.register('zmm')
                code = un_op(xmms1, xmms)
            elif cgen.cpu.AVX2:
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

    def is_subscriptable(self):
        return True

    def load_item_cmd(self, cgen, index=None, reg=None, ptr_reg=None):
        if index is not None:
            if index < 0 or index > len(self) - 1:
                raise IndexError("Index is out of bounds! ", index, type(self), self.name)

        def load_item(ret_reg, ptr, reg):
            if cgen.regs.is_reg32(reg):
                reg = cgen.regs.t_32_to_64(reg)
            code = 'mov %s, dword[%s + %s * 4]\n' % (ret_reg, ptr, reg)
            return code

        ret_reg = cgen.register('general')

        if ptr_reg is None:
            if index is None:
                ptr = cgen.register('pointer')
                code = cgen.gen.load_addr(ptr, self.name)
                code += load_item(ret_reg, ptr, reg)
                cgen.release_reg(ptr)
            else:
                code = cgen.gen.load_i32(ret_reg, name=self.name, offset=index * 4)
        else:
            if index is None:
                code = load_item(ret_reg, ptr_reg, reg)
            else:
                code = cgen.gen.load_i32(ret_reg, ptr_reg=ptr_reg, offset=index * 4)
        return code, ret_reg, Int32Arg

    def store_item_cmd(self, cgen, arg_type, src_reg, index=None, reg=None, ptr_reg=None):

        if arg_type is not Int32Arg:
            raise ValueError("int32 item argument expected!", self, arg_type)

        if index is not None:
            if index < 0 or index > len(self) - 1:
                raise IndexError("Index is out of bounds! ", index, type(self), self.name)

        def store_item(src_reg, ptr, reg):
            if cgen.regs.is_reg32(reg):
                reg = cgen.regs.t_32_to_64(reg)
            code = 'mov dword[%s + %s * 4], %s\n' % (ptr, reg, src_reg)
            return code

        if ptr_reg is None:
            if index is None:
                ptr = cgen.register('pointer')
                code = cgen.gen.load_addr(ptr, self.name)
                code += store_item(src_reg, ptr, reg)
                cgen.release_reg(ptr)
            else:
                code = cgen.gen.store_i32(src_reg, name=self.name, offset=index * 4)
        else:
            if index is None:
                code = store_item(src_reg, ptr_reg, reg)
            else:
                code = cgen.gen.store_i32(src_reg, ptr_reg=ptr_reg, offset=index * 4)
        return code

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F and len(self) == 16:
            return 'zmm'
        elif (cgen.cpu.AVX2 or cgen.cpu.AVX512F) and len(self) == 8:
            return 'ymm'
        else:
            return 'xmm'

    def is_multi_part(self, cgen):
        if cgen.cpu.AVX512F:
            return False
        elif cgen.cpu.AVX2:
            return len(self) > 8
        else:
            return len(self) > 4

    def set_array_item(self, addr, value):
        if not isinstance(value, type(self._value)):
            raise TypeError("Expected %s got %s" % (type(self._value), type(value)))
        x86.SetInt32(addr, value.values, 0)

    def get_array_item(self, addr):
        return type(self._value)(*x86.GetInt32(addr, 0, len(self)))

    @property
    def itemsize(self):
        return 4 * len(self)


class Int32x2Arg(Int32VecBase):
    def __init__(self, name=None, value=int32x2()):
        super(Int32x2Arg, self).__init__(name)
        if not isinstance(value, int32x2):
            raise TypeError("int32x2 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 16

    def stack_size(self, cpu):
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'int32x2'

    def load_item_from_array(self, cgen, ptr_reg):
        xmm = cgen.register('xmm')
        code = cgen.gen.load_i32x4(xmm, ptr_reg=ptr_reg, align=False)
        return code, xmm, Int32x2Arg

    def store_item_to_array(self, cgen, ptr_reg, xmm):
        # TODO AVX512 - use mask register - TODO tdasm - oword [mem] {k}, xmm
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vmovq qword [%s], %s\n' % (ptr_reg, xmm)
        else:
            code = 'movq qword [%s], %s\n' % (ptr_reg, xmm)
        return code


class Int32x3Arg(Int32VecBase):
    def __init__(self, name=None, value=int32x3()):
        super(Int32x3Arg, self).__init__(name)
        if not isinstance(value, int32x3):
            raise TypeError("int32x3 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 16

    def stack_size(self, cpu):
        return 16

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'int32x3'

    def load_item_from_array(self, cgen, ptr_reg):
        xmm = cgen.register('xmm')
        code = cgen.gen.load_i32x4(xmm, ptr_reg=ptr_reg, align=False)
        return code, xmm, Int32x3Arg

    def store_item_to_array(self, cgen, ptr_reg, xmm):
        # TODO AVX512 - use mask register - TODO tdasm - oword [mem] {k}, xmm
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vmovq qword [%s], %s\n' % (ptr_reg, xmm)
            code += "vpunpckhqdq %s, %s, %s\n" % (xmm, xmm, xmm)
            code += 'vmovd dword [%s + 8], %s\n' % (ptr_reg, xmm)
        else:
            code = 'movq qword [%s], %s\n' % (ptr_reg, xmm)
            code += "punpckhqdq %s, %s\n" % (xmm, xmm)
            code += 'movd dword [%s + 8], %s\n' % (ptr_reg, xmm)
        return code


class Int32x4Arg(Int32VecBase):
    def __init__(self, name=None, value=int32x4()):
        super(Int32x4Arg, self).__init__(name)
        if not isinstance(value, int32x4):
            raise TypeError("int32x4 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 16

    def stack_size(self, cpu):
        return 16

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'int32x4'

    def load_item_from_array(self, cgen, ptr_reg):
        xmm = cgen.register('xmm')
        code = cgen.gen.load_i32x4(xmm, ptr_reg=ptr_reg)
        return code, xmm, Int32x4Arg

    def store_item_to_array(self, cgen, ptr_reg, xmm):
        return cgen.gen.store_i32x4(xmm, ptr_reg=ptr_reg)


class Int32x8Arg(Int32VecBase):
    def __init__(self, name=None, value=int32x8()):
        super(Int32x8Arg, self).__init__(name)
        if not isinstance(value, int32x8):
            raise TypeError("int32x8 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 32

    def stack_size(self, cpu):
        return 32

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'int32x8'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            xmms = cgen.register('ymm')
            code = cgen.gen.load_i32x8(xmms, ptr_reg=ptr_reg, align=True)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_i32x4(xmm1, ptr_reg=ptr_reg)
            code += cgen.gen.load_i32x4(xmm2, ptr_reg=ptr_reg, offset=16)
            xmms = (xmm1, xmm2)
        return code, xmms, Int32x8Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            code = cgen.gen.store_i32x8(xmms, ptr_reg=ptr_reg, align=True)
        else:
            code = cgen.gen.store_i32x4(xmms[0], ptr_reg=ptr_reg)
            code += cgen.gen.store_i32x4(xmms[1], ptr_reg=ptr_reg, offset=16)
        return code


class Int32x16Arg(Int32VecBase):
    def __init__(self, name=None, value=int32x16()):
        super(Int32x16Arg, self).__init__(name)
        if not isinstance(value, int32x16):
            raise TypeError("int32x16 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 64

    def stack_size(self, cpu):
        return 64

    def __len__(self):
        return 16

    @classmethod
    def type_name(cls):
        return 'int32x16'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX512F:
            xmms = cgen.register('zmm')
            code = cgen.gen.load_i32x16(xmms, ptr_reg=ptr_reg, align=True)
        elif cgen.cpu.AVX2:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = cgen.gen.load_i32x8(ymm1, ptr_reg=ptr_reg, align=False)
            code += cgen.gen.load_i32x8(ymm2, ptr_reg=ptr_reg, offset=32, align=False)
            xmms = (ymm1, ymm2)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_i32x4(xmm1, ptr_reg=ptr_reg)
            code += cgen.gen.load_i32x4(xmm2, ptr_reg=ptr_reg, offset=16)
            code += cgen.gen.load_i32x4(xmm3, ptr_reg=ptr_reg, offset=32)
            code += cgen.gen.load_i32x4(xmm4, ptr_reg=ptr_reg, offset=48)
            xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, Int32x16Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX512F:
            code = cgen.gen.store_i32x16(xmms, ptr_reg=ptr_reg, align=True)
        elif cgen.cpu.AVX2:
            code = cgen.gen.store_i32x8(xmms[0], ptr_reg=ptr_reg, align=False)
            code += cgen.gen.store_i32x8(xmms[1], ptr_reg=ptr_reg, offset=32, align=False)
        else:
            code = cgen.gen.store_i32x4(xmms[0], ptr_reg=ptr_reg)
            code += cgen.gen.store_i32x4(xmms[1], ptr_reg=ptr_reg, offset=16)
            code += cgen.gen.store_i32x4(xmms[2], ptr_reg=ptr_reg, offset=32)
            code += cgen.gen.store_i32x4(xmms[3], ptr_reg=ptr_reg, offset=48)
        return code


int32x2.arg_class = Int32x2Arg
int32x3.arg_class = Int32x3Arg
int32x4.arg_class = Int32x4Arg
int32x8.arg_class = Int32x8Arg
int32x16.arg_class = Int32x16Arg
register_arg_factory(Int32x2Arg, lambda: Int32x2Arg())
register_arg_factory(Int32x3Arg, lambda: Int32x3Arg())
register_arg_factory(Int32x4Arg, lambda: Int32x4Arg())
register_arg_factory(Int32x8Arg, lambda: Int32x8Arg())
register_arg_factory(Int32x16Arg, lambda: Int32x16Arg())


class int64x2:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (int64(), int64())
        elif len(args) == 1:
            self.values = (int64(args[0]), int64(args[0]))
        else:
            self.values = (int64(args[0]), int64(args[1]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int64(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s" % (repr(v[0]), repr(v[1]))


class int64x3:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (int64(), int64(), int64())
        elif len(args) == 1:
            self.values = (int64(args[0]), int64(args[0]), int64(args[0]))
        else:
            self.values = (int64(args[0]), int64(args[1]), int64(args[2]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int64(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s %s" % (repr(v[0]), repr(v[1]), repr(v[2]))


class int64x4:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = (int64(), int64(), int64(), int64())
        elif len(args) == 1:
            self.values = (int64(args[0]), int64(args[0]), int64(args[0]), int64(args[0]))
        else:
            self.values = (int64(args[0]), int64(args[1]), int64(args[2]), int64(args[3]))

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int64(value)
        self.values = tuple(v)

    def __repr__(self):
        v = self.values
        return "%s %s %s %s" % (repr(v[0]), repr(v[1]), repr(v[2]), repr(v[3]))


class int64x8:
    def __init__(self, *args):
        if len(args) == 0:
            self.values = tuple([int64()] * 8)
        elif len(args) == 1:
            self.values = tuple([int64(args[0])] * 8)
        elif len(args) == 8:
            self.values = tuple(int64(a) for a in args)
        else:
            raise ValueError("Constructor for type int64x8 only accept 0, 1 or 8 arguments.", args)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        v = list(self.values)
        v[key] = int64(value)
        self.values = tuple(v)

    def __repr__(self):
        vals = ' '.join(repr(v) for v in self.values)
        return "%s" % vals


class Int64VecBase(Argument):

    def data_sec_repr(self):
        vals = ', '.join(repr(v) for v in self._value.values)
        align = 2
        length = (len(self) + align - 1) & ~(align - 1)
        return 'int64 %s[%i] = %s\n' % (self._name, length, vals)

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
            code = cgen.gen.load_i64x2(xmms, name=name, ptr_reg=ptr_reg)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_i64x4(xmms, name=name, ptr_reg=ptr_reg)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i64x2(xmm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_i64x2(xmm2, name=name, ptr_reg=ptr_reg, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                xmms = cgen.register('zmm')
                code = cgen.gen.load_i64x8(xmms, name=name, ptr_reg=ptr_reg)
            elif cgen.cpu.AVX2:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_i64x4(ymm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_i64x4(ymm2, name=name, ptr_reg=ptr_reg, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i64x2(xmm1, name=name, ptr_reg=ptr_reg)
                code += cgen.gen.load_i64x2(xmm2, name=name, ptr_reg=ptr_reg, offset=16)
                code += cgen.gen.load_i64x2(xmm3, name=name, ptr_reg=ptr_reg, offset=32)
                code += cgen.gen.load_i64x2(xmm4, name=name, ptr_reg=ptr_reg, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms, name=None):
        name = self.name if name is None else name

        if len(self) == 2:
            code = cgen.gen.store_i64x2(xmms, name=name)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                code = cgen.gen.store_i64x4(xmms, name=name)
            else:
                code = cgen.gen.store_i64x2(xmms[0], name=name)
                code += cgen.gen.store_i64x2(xmms[1], name=name, offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                code = cgen.gen.store_i64x8(xmms, name=name)
            elif cgen.cpu.AVX2:
                code = cgen.gen.store_i64x4(xmms[0], name=name)
                code += cgen.gen.store_i64x4(xmms[1], name=name, offset=32)
            else:
                code = cgen.gen.store_i64x2(xmms[0], name=name)
                code += cgen.gen.store_i64x2(xmms[1], name=name, offset=16)
                code += cgen.gen.store_i64x2(xmms[2], name=name, offset=32)
                code += cgen.gen.store_i64x2(xmms[3], name=name, offset=48)

        return code

    def can_operate_with_const(self, cgen, op, value):
        if not isinstance(value, int):
            return False
        if value > 127 or value < -128:
            return False
        elif op in ('<<',):
            return True
        else:
            return False

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('+', '-', '&', '^', '|', '==', '>')

    def arith_with_const(self, cgen, reg, op, value):
        if len(self) == 2:
            dst_xmms = reg if cgen.can_destruct(reg) else cgen.register('xmm')
            code = cgen.gen.arith_i64x2_con(reg, op, value, dst_reg=dst_xmms)
        elif len(self) in (3, 4):
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = reg if cgen.can_destruct(reg) else cgen.register('ymm')
                code = cgen.gen.arith_i64x4_con(reg, op, value, dst_reg=dst_xmms)
            else:
                dst_xmms = reg if cgen.can_destruct(reg) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i64x2_con(reg[0], op, value, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2_con(reg[1], op, value, dst_reg=dst_xmms[1])
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                dst_xmms = reg if cgen.can_destruct(reg) else cgen.register('zmm')
                code = cgen.gen.arith_i64x8_con(reg, op, value, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2:
                dst_xmms = reg if cgen.can_destruct(reg) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_i64x4_con(reg[0], op, value, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x4_con(reg[1], op, value, dst_reg=dst_xmms[1])
            else:
                if cgen.can_destruct(reg):
                    dst_xmms = reg
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_i64x2_con(reg[0], op, value, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2_con(reg[1], op, value, dst_reg=dst_xmms[1])
                code += cgen.gen.arith_i64x2_con(reg[2], op, value, dst_reg=dst_xmms[2])
                code += cgen.gen.arith_i64x2_con(reg[3], op, value, dst_reg=dst_xmms[3])
        return code, dst_xmms, type(self)

    def arith_with_memory(self, cgen, xmms, op, arg):
        if len(self) == 2:
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_i64x2(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
                code = cgen.gen.arith_i64x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_i64x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i64x2(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                if op in ('>', '=='):
                    dst_xmms = cgen.register('mask')
                else:
                    dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('zmm')
                code = cgen.gen.arith_i64x8(xmms, op, name=arg.name, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_i64x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=32)
            else:
                if cgen.can_destruct(xmms):
                    dst_xmms = xmms
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_i64x2(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
                code += cgen.gen.arith_i64x2(xmms[2], op, name=arg.name, dst_reg=dst_xmms[2], offset=32)
                code += cgen.gen.arith_i64x2(xmms[3], op, name=arg.name, dst_reg=dst_xmms[3], offset=48)

        if op in ('>', '=='):
            int_type = {2: MaskI64x2Arg, 3: MaskI64x3Arg, 4: MaskI64x4Arg, 8: MaskI64x8Arg}
            return code, dst_xmms, int_type[len(self)]
        else:
            return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):
        if len(self) == 2:
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_i64x2(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX512F and op in ('>', '=='):
                dst_xmms = cgen.register('mask')
                code = cgen.gen.arith_i64x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2 or cgen.cpu.AVX512F:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_i64x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i64x2(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 8:
            if cgen.cpu.AVX512F:
                if op in ('>', '=='):
                    dst_xmms = cgen.register('mask')
                else:
                    dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('zmm')
                code = cgen.gen.arith_i64x8(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            elif cgen.cpu.AVX2:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_i64x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
            else:
                if cgen.can_destruct(xmms1):
                    dst_xmms = xmms1
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_i64x2(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
                code += cgen.gen.arith_i64x2(xmms1[2], op, xmm2=xmms2[2], dst_reg=dst_xmms[2])
                code += cgen.gen.arith_i64x2(xmms1[3], op, xmm2=xmms2[3], dst_reg=dst_xmms[3])

        if op in ('>', '=='):
            int_type = {2: MaskI64x2Arg, 3: MaskI64x3Arg, 4: MaskI64x4Arg, 8: MaskI64x8Arg}
            return code, dst_xmms, int_type[len(self)]
        else:
            return code, dst_xmms, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def do_unary_op(self, cgen, xmms, op):
        if op not in ('+', '-'):
            raise CompileError("Unsupported unary operation %s for %s type!" % (str(op), str(self)))

        if op == '+':
            return '', xmms, type(self)

        def un_op(reg1, reg2):
            if cgen.cpu.AVX512F:
                code = 'vpxorq %s, %s, %s\n' % (reg1, reg1, reg1)
                code += 'vpsubq %s, %s, %s\n' % (reg1, reg1, reg2)
            elif cgen.cpu.AVX:
                code = 'vpxor %s, %s, %s\n' % (reg1, reg1, reg1)
                code += 'vpsubq %s, %s, %s\n' % (reg1, reg1, reg2)
            else:
                code = 'pxor %s, %s\n' % (reg1, reg1)
                code += 'psubq %s, %s\n' % (reg1, reg2)
            return code


        if len(self) == 2:
            xmms1 = cgen.register('xmm')
            code = un_op(xmms1, xmms)
        elif len(self) in (3, 4):
            if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
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
            elif cgen.cpu.AVX2:
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

    def is_subscriptable(self):
        return True

    def load_item_cmd(self, cgen, index=None, reg=None, ptr_reg=None):
        if index is not None:
            if index < 0 or index > len(self) - 1:
                raise IndexError("Index is out of bounds! ", index, type(self), self.name)

        def load_item(ret_reg, ptr, reg):
            if cgen.regs.is_reg32(reg):
                reg = cgen.regs.t_32_to_64(reg)
            code = 'mov %s, qword[%s + %s * 8]\n' % (ret_reg, ptr, reg)
            return code

        ret_reg = cgen.register('general64')

        if ptr_reg is None:
            if index is None:
                ptr = cgen.register('pointer')
                code = cgen.gen.load_addr(ptr, self.name)
                code += load_item(ret_reg, ptr, reg)
                cgen.release_reg(ptr)
            else:
                code = cgen.gen.load_i64(ret_reg, name=self.name, offset=index * 8)
        else:
            if index is None:
                code = load_item(ret_reg, ptr_reg, reg)
            else:
                code = cgen.gen.load_i64(ret_reg, ptr_reg=ptr_reg, offset=index * 8)
        return code, ret_reg, Int64Arg

    def store_item_cmd(self, cgen, arg_type, src_reg, index=None, reg=None, ptr_reg=None):

        if arg_type is not Int64Arg:
            raise ValueError("int64 item argument expected!", self, arg_type)

        if index is not None:
            if index < 0 or index > len(self) - 1:
                raise IndexError("Index is out of bounds! ", index, type(self), self.name)

        def store_item(src_reg, ptr, reg):
            if cgen.regs.is_reg32(reg):
                reg = cgen.regs.t_32_to_64(reg)
            code = 'mov qword[%s + %s * 8], %s\n' % (ptr, reg, src_reg)
            return code

        if ptr_reg is None:
            if index is None:
                ptr = cgen.register('pointer')
                code = cgen.gen.load_addr(ptr, self.name)
                code += store_item(src_reg, ptr, reg)
                cgen.release_reg(ptr)
            else:
                code = cgen.gen.store_i64(src_reg, name=self.name, offset=index * 8)
        else:
            if index is None:
                code = store_item(src_reg, ptr_reg, reg)
            else:
                code = cgen.gen.store_i64(src_reg, ptr_reg=ptr_reg, offset=index * 8)
        return code

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F and len(self) == 8:
            return 'zmm'
        elif (cgen.cpu.AVX2 or cgen.cpu.AVX512F) and len(self) in (3, 4):
            return 'ymm'
        else:
            return 'xmm'

    def is_multi_part(self, cgen):
        if cgen.cpu.AVX512F:
            return False
        elif cgen.cpu.AVX2:
            return len(self) > 4
        else:
            return len(self) > 2

    def set_array_item(self, addr, value):
        if not isinstance(value, type(self._value)):
            raise TypeError("Expected %s got %s" % (type(self._value), type(value)))
        x86.SetInt64(addr, value.values, 0)

    def get_array_item(self, addr):
        return type(self._value)(*x86.GetInt64(addr, 0, len(self)))

    @property
    def itemsize(self):
        return 8 * len(self)


class Int64x2Arg(Int64VecBase):
    def __init__(self, name=None, value=int64x2()):
        super(Int64x2Arg, self).__init__(name)
        if not isinstance(value, int64x2):
            raise TypeError("int64x2 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 16

    def stack_size(self, cpu):
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'int64x2'

    def load_item_from_array(self, cgen, ptr_reg):
        xmm = cgen.register('xmm')
        code = cgen.gen.load_i64x2(xmm, ptr_reg=ptr_reg)
        return code, xmm, Int64x2Arg

    def store_item_to_array(self, cgen, ptr_reg, xmm):
        return cgen.gen.store_i64x2(xmm, ptr_reg=ptr_reg)


class Int64x3Arg(Int64VecBase):
    def __init__(self, name=None, value=int64x3()):
        super(Int64x3Arg, self).__init__(name)
        if not isinstance(value, int64x3):
            raise TypeError("int64x3 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 32

    def stack_size(self, cpu):
        return 32

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'int64x3'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            xmms = cgen.register('ymm')
            code = cgen.gen.load_i64x4(xmms, ptr_reg=ptr_reg, align=False)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_i64x2(xmm1, ptr_reg=ptr_reg, align=False)
            code += cgen.gen.load_i64x2(xmm2, ptr_reg=ptr_reg, offset=16, align=False)
            xmms = (xmm1, xmm2)
        return code, xmms, Int64x3Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        # TODO AVX512 - use mask register - TODO tdasm - oword [mem] {k}, xmm
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            code = cgen.gen.store_i64x2('x' + xmms[1:], ptr_reg=ptr_reg, align=False)
            if cgen.cpu.AVX512F:
                code += 'vextracti64x2 %s, %s, 1\n' % ('x' + xmms[1:], xmms)
            else:
                code += 'vextracti128 %s, %s, 1\n' % ('x' + xmms[1:], xmms)
            code += 'vmovq qword [%s + 16], %s\n' % (ptr_reg, 'x' + xmms[1:])
        else:
            code = cgen.gen.store_i64x2(xmms[0], ptr_reg=ptr_reg, align=False)
            if cgen.cpu.AVX:
                code += 'vmovq qword [%s + 16], %s\n' % (ptr_reg, xmms[1])
            else:
                code += 'movq qword [%s + 16], %s\n' % (ptr_reg, xmms[1])
        return code


class Int64x4Arg(Int64VecBase):
    def __init__(self, name=None, value=int64x4()):
        super(Int64x4Arg, self).__init__(name)
        if not isinstance(value, int64x4):
            raise TypeError("int64x4 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 32

    def stack_size(self, cpu):
        return 32

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'int64x4'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            xmms = cgen.register('ymm')
            code = cgen.gen.load_i64x4(xmms, ptr_reg=ptr_reg, align=True)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_i64x2(xmm1, ptr_reg=ptr_reg)
            code += cgen.gen.load_i64x2(xmm2, ptr_reg=ptr_reg, offset=16)
            xmms = (xmm1, xmm2)
        return code, xmms, Int64x4Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            code = cgen.gen.store_i64x4(xmms, ptr_reg=ptr_reg, align=True)
        else:
            code = cgen.gen.store_i64x2(xmms[0], ptr_reg=ptr_reg)
            code += cgen.gen.store_i64x2(xmms[1], ptr_reg=ptr_reg, offset=16)
        return code


class Int64x8Arg(Int64VecBase):
    def __init__(self, name=None, value=int64x8()):
        super(Int64x8Arg, self).__init__(name)
        if not isinstance(value, int64x8):
            raise TypeError("int64x8 type expected got", value)
        self._value = value

    def stack_align(self, cpu):
        return 64

    def stack_size(self, cpu):
        return 64

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'int64x8'

    def load_item_from_array(self, cgen, ptr_reg):
        if cgen.cpu.AVX512F:
            xmms = cgen.register('zmm')
            code = cgen.gen.load_i64x8(xmms, ptr_reg=ptr_reg, align=True)
        elif cgen.cpu.AVX2:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = cgen.gen.load_i64x4(ymm1, ptr_reg=ptr_reg, align=True)
            code += cgen.gen.load_i64x4(ymm2, ptr_reg=ptr_reg, offset=32, align=True)
            xmms = (ymm1, ymm2)
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = cgen.gen.load_i64x2(xmm1, ptr_reg=ptr_reg)
            code += cgen.gen.load_i64x2(xmm2, ptr_reg=ptr_reg, offset=16)
            code += cgen.gen.load_i64x2(xmm3, ptr_reg=ptr_reg, offset=32)
            code += cgen.gen.load_i64x2(xmm4, ptr_reg=ptr_reg, offset=48)
            xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, Int64x8Arg

    def store_item_to_array(self, cgen, ptr_reg, xmms):
        if cgen.cpu.AVX512F:
            code = cgen.gen.store_i64x8(xmms, ptr_reg=ptr_reg, align=True)
        elif cgen.cpu.AVX2:
            code = cgen.gen.store_i64x4(xmms[0], ptr_reg=ptr_reg, align=True)
            code += cgen.gen.store_i64x4(xmms[1], ptr_reg=ptr_reg, offset=32, align=True)
        else:
            code = cgen.gen.store_i64x2(xmms[0], ptr_reg=ptr_reg)
            code += cgen.gen.store_i64x2(xmms[1], ptr_reg=ptr_reg, offset=16)
            code += cgen.gen.store_i64x2(xmms[2], ptr_reg=ptr_reg, offset=32)
            code += cgen.gen.store_i64x2(xmms[3], ptr_reg=ptr_reg, offset=48)
        return code


int64x2.arg_class = Int64x2Arg
int64x3.arg_class = Int64x3Arg
int64x4.arg_class = Int64x4Arg
int64x8.arg_class = Int64x8Arg
register_arg_factory(Int64x2Arg, lambda: Int64x2Arg())
register_arg_factory(Int64x3Arg, lambda: Int64x3Arg())
register_arg_factory(Int64x4Arg, lambda: Int64x4Arg())
register_arg_factory(Int64x8Arg, lambda: Int64x8Arg())
