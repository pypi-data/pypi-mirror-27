

from .cgen import register_arg_factory
from .args import Argument


class MaskF64VecBase(Argument):

    def data_sec_repr(self):
        raise ValueError("Masks can only be placed on stack!")

    def set_ds_value(self, ds, val):
        pass

    def get_ds_value(self, ds):
        pass

    def load_cmd(self, cgen):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, self.name)
            return code, mask, type(self)

        if len(self) == 2:
            xmms = cgen.register('xmm')
            code = cgen.gen.load_f64x2(xmms, name=self.name)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_f64x4(xmms, name=self.name)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_f64x2(xmm1, name=self.name)
                code += cgen.gen.load_f64x2(xmm2, name=self.name, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 8:
            if cgen.cpu.AVX:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_f64x4(ymm1, name=self.name)
                code += cgen.gen.load_f64x4(ymm2, name=self.name, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_f64x2(xmm1, name=self.name)
                code += cgen.gen.load_f64x2(xmm2, name=self.name, offset=16)
                code += cgen.gen.load_f64x2(xmm3, name=self.name, offset=32)
                code += cgen.gen.load_f64x2(xmm4, name=self.name, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms):
        if cgen.cpu.AVX512F:
            code = "kmovw word[%s], %s\n" % (self.name, xmms)
            return code

        if len(self) == 2:
            code = cgen.gen.store_f64x2(xmms, name=self.name)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX:
                code = cgen.gen.store_f64x4(xmms, name=self.name)
            else:
                code = cgen.gen.store_f64x2(xmms[0], name=self.name)
                code += cgen.gen.store_f64x2(xmms[1], name=self.name, offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX:
                code = cgen.gen.store_f64x4(xmms[0], name=self.name)
                code += cgen.gen.store_f64x4(xmms[1], name=self.name, offset=32)
            else:
                code = cgen.gen.store_f64x2(xmms[0], name=self.name)
                code += cgen.gen.store_f64x2(xmms[1], name=self.name, offset=16)
                code += cgen.gen.store_f64x2(xmms[2], name=self.name, offset=32)
                code += cgen.gen.store_f64x2(xmms[3], name=self.name, offset=48)
        return code

    def can_operate_with_memory(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('&', '^', '|')

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('&', '^', '|')

    def arith_with_memory(self, cgen, xmms, op, arg):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, arg.name)
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code += "%s %s, %s, %s\n" % (insts[op], mask, xmms, mask)
            return code, mask, type(self)

        if len(self) == 2:
            dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_f64x2(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_f64x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_f64x2(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x2(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX:
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

        return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):
        if cgen.cpu.AVX512F:
            mask = xmms1 if cgen.can_destruct(xmms1) else cgen.register('mask')
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code = "%s %s, %s, %s\n" % (insts[op], mask, xmms1, xmms2)
            return code, mask, type(self)

        if len(self) == 2:
            dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_f64x2(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_f64x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_f64x2(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f64x2(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 8:
            if cgen.cpu.AVX:
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

        return code, dst_xmms, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F:
            return 'mask'
        elif cgen.cpu.AVX and len(self) in (3, 4):
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


class MaskF64x2Arg(MaskF64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'maskf64x2'


class MaskF64x3Arg(MaskF64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'maskf64x3'


class MaskF64x4Arg(MaskF64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'maskf64x4'


class MaskF64x8Arg(MaskF64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'maskf64x8'


register_arg_factory(MaskF64x2Arg, lambda: MaskF64x2Arg())
register_arg_factory(MaskF64x3Arg, lambda: MaskF64x3Arg())
register_arg_factory(MaskF64x4Arg, lambda: MaskF64x4Arg())
register_arg_factory(MaskF64x8Arg, lambda: MaskF64x8Arg())


class MaskF32VecBase(Argument):

    def data_sec_repr(self):
        raise ValueError("Masks can only be on stack!")

    def set_ds_value(self, ds, val):
        pass

    def get_ds_value(self, ds):
        pass

    def load_cmd(self, cgen):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, self.name)
            return code, mask, type(self)

        if len(self) in (2, 3, 4):
            xmms = cgen.register('xmm')
            code = cgen.gen.load_f32x4(xmms, name=self.name)
        elif len(self) == 8:
            if cgen.cpu.AVX:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_f32x8(xmms, name=self.name)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_f32x4(xmm1, name=self.name)
                code += cgen.gen.load_f32x4(xmm2, name=self.name, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 16:
            if cgen.cpu.AVX:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_f32x8(ymm1, name=self.name)
                code += cgen.gen.load_f32x8(ymm2, name=self.name, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_f32x4(xmm1, name=self.name)
                code += cgen.gen.load_f32x4(xmm2, name=self.name, offset=16)
                code += cgen.gen.load_f32x4(xmm3, name=self.name, offset=32)
                code += cgen.gen.load_f32x4(xmm4, name=self.name, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms):
        if cgen.cpu.AVX512F:
            code = "kmovw word[%s], %s\n" % (self.name, xmms)
            return code

        if len(self) in (2, 3, 4):
            code = cgen.gen.store_f32x4(xmms, name=self.name)
        elif len(self) == 8:
            if cgen.cpu.AVX:
                code = cgen.gen.store_f32x8(xmms, name=self.name)
            else:
                code = cgen.gen.store_f32x4(xmms[0], name=self.name)
                code += cgen.gen.store_f32x4(xmms[1], name=self.name, offset=16)
        elif len(self) == 16:
            if cgen.cpu.AVX:
                code = cgen.gen.store_f32x8(xmms[0], name=self.name)
                code += cgen.gen.store_f32x8(xmms[1], name=self.name, offset=32)
            else:
                code = cgen.gen.store_f32x4(xmms[0], name=self.name)
                code += cgen.gen.store_f32x4(xmms[1], name=self.name, offset=16)
                code += cgen.gen.store_f32x4(xmms[2], name=self.name, offset=32)
                code += cgen.gen.store_f32x4(xmms[3], name=self.name, offset=48)
        return code

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('&', '^', '|')

    def arith_with_memory(self, cgen, xmms, op, arg):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, arg.name)
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code += "%s %s, %s, %s\n" % (insts[op], mask, xmms, mask)
            return code, mask, type(self)

        if len(self) in (2, 3, 4):
            dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_f32x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_f32x8(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_f32x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f32x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 16:
            if cgen.cpu.AVX:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_f32x8(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f32x8(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=32)
            else:
                if cgen.can_destruct(xmms):
                    dst_xmms = xmms
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_f32x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f32x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
                code += cgen.gen.arith_f32x4(xmms[2], op, name=arg.name, dst_reg=dst_xmms[2], offset=32)
                code += cgen.gen.arith_f32x4(xmms[3], op, name=arg.name, dst_reg=dst_xmms[3], offset=48)

        return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):
        if cgen.cpu.AVX512F:
            mask = xmms1 if cgen.can_destruct(xmms1) else cgen.register('mask')
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code = "%s %s, %s, %s\n" % (insts[op], mask, xmms1, xmms2)
            return code, mask, type(self)

        if len(self) in (2, 3, 4):
            dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_f32x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_f32x8(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_f32x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f32x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 16:
            if cgen.cpu.AVX:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('ymm'), cgen.register('ymm'))
                code = cgen.gen.arith_f32x8(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f32x8(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
            else:
                if cgen.can_destruct(xmms1):
                    dst_xmms = xmms1
                else:
                    dst_xmms = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.arith_f32x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_f32x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
                code += cgen.gen.arith_f32x4(xmms1[2], op, xmm2=xmms2[2], dst_reg=dst_xmms[2])
                code += cgen.gen.arith_f32x4(xmms1[3], op, xmm2=xmms2[3], dst_reg=dst_xmms[3])

        return code, dst_xmms, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F:
            return 'mask'
        elif cgen.cpu.AVX and len(self) == 8:
            return 'ymm'
        else:
            return 'xmm'

    def is_multi_part(self, cgen):
        if cgen.cpu.AVX512F:
            return False
        elif cgen.cpu.AVX:
            return len(self) > 8
        else:
            return len(self) > 4



class MaskF32x2Arg(MaskF32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'maskf32x2'


class MaskF32x3Arg(MaskF32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'maskf32x3'


class MaskF32x4Arg(MaskF32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'maskf32x4'


class MaskF32x8Arg(MaskF32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'maskf32x8'


class MaskF32x16Arg(MaskF32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def __len__(self):
        return 16

    @classmethod
    def type_name(cls):
        return 'maskf32x16'


register_arg_factory(MaskF32x2Arg, lambda: MaskF32x2Arg())
register_arg_factory(MaskF32x3Arg, lambda: MaskF32x3Arg())
register_arg_factory(MaskF32x4Arg, lambda: MaskF32x4Arg())
register_arg_factory(MaskF32x8Arg, lambda: MaskF32x8Arg())
register_arg_factory(MaskF32x16Arg, lambda: MaskF32x16Arg())


class MaskI32VecBase(Argument):

    def data_sec_repr(self):
        raise ValueError("Masks can only be on stack!")

    def set_ds_value(self, ds, val):
        pass

    def get_ds_value(self, ds):
        pass

    def load_cmd(self, cgen):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, self.name)
            return code, mask, type(self)

        if len(self) == 2:
            xmms = cgen.register('xmm')
            code = cgen.gen.load_f64(xmms, name=self.name)
        elif len(self) == 3 or len(self) == 4:
            xmms = cgen.register('xmm')
            code = cgen.gen.load_i32x4(xmms, name=self.name)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_i32x8(xmms, name=self.name)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i32x4(xmm1, name=self.name)
                code += cgen.gen.load_i32x4(xmm2, name=self.name, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 16:
            if cgen.cpu.AVX2:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_i32x8(ymm1, name=self.name)
                code += cgen.gen.load_i32x8(ymm2, name=self.name, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i32x4(xmm1, name=self.name)
                code += cgen.gen.load_i32x4(xmm2, name=self.name, offset=16)
                code += cgen.gen.load_i32x4(xmm3, name=self.name, offset=32)
                code += cgen.gen.load_i32x4(xmm4, name=self.name, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms):
        if cgen.cpu.AVX512F:
            code = "kmovw word[%s], %s\n" % (self.name, xmms)
            return code

        if len(self) in (2, 3, 4):
            code = cgen.gen.store_i32x4(xmms, name=self.name)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
                code = cgen.gen.store_i32x8(xmms, name=self.name)
            else:
                code = cgen.gen.store_i32x4(xmms[0], name=self.name)
                code += cgen.gen.store_i32x4(xmms[1], name=self.name, offset=16)
        elif len(self) == 16:
            if cgen.cpu.AVX2:
                code = cgen.gen.store_i32x8(xmms[0], name=self.name)
                code += cgen.gen.store_i32x8(xmms[1], name=self.name, offset=32)
            else:
                code = cgen.gen.store_i32x4(xmms[0], name=self.name)
                code += cgen.gen.store_i32x4(xmms[1], name=self.name, offset=16)
                code += cgen.gen.store_i32x4(xmms[2], name=self.name, offset=32)
                code += cgen.gen.store_i32x4(xmms[3], name=self.name, offset=48)

        return code

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('&', '^', '|')

    def arith_with_memory(self, cgen, xmms, op, arg):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, arg.name)
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code += "%s %s, %s, %s\n" % (insts[op], mask, xmms, mask)
            return code, mask, type(self)

        if len(self) in (2, 3, 4):
            dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_i32x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_i32x8(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i32x4(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 16:
            if cgen.cpu.AVX2:
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

        return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):
        if cgen.cpu.AVX512F:
            mask = xmms1 if cgen.can_destruct(xmms1) else cgen.register('mask')
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code = "%s %s, %s, %s\n" % (insts[op], mask, xmms1, xmms2)
            return code, mask, type(self)

        if len(self) in (2, 3, 4):
            dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_i32x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_i32x8(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i32x4(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i32x4(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 16:
            if cgen.cpu.AVX2:
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

        return code, dst_xmms, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F:
            return 'mask'
        elif cgen.cpu.AVX2 and len(self) == 8:
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


class MaskI32x2Arg(MaskI32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'maski32x2'


class MaskI32x3Arg(MaskI32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'maski32x3'


class MaskI32x4Arg(MaskI32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'maski32x4'


class MaskI32x8Arg(MaskI32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'maski32x8'


class MaskI32x16Arg(MaskI32VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def __len__(self):
        return 16

    @classmethod
    def type_name(cls):
        return 'maski32x16'


register_arg_factory(MaskI32x2Arg, lambda: MaskI32x2Arg())
register_arg_factory(MaskI32x3Arg, lambda: MaskI32x3Arg())
register_arg_factory(MaskI32x4Arg, lambda: MaskI32x4Arg())
register_arg_factory(MaskI32x8Arg, lambda: MaskI32x8Arg())
register_arg_factory(MaskI32x16Arg, lambda: MaskI32x16Arg())


class MaskI64VecBase(Argument):

    def data_sec_repr(self):
        raise ValueError("Masks can only be on stack!")

    def set_ds_value(self, ds, val):
        pass

    def get_ds_value(self, ds):
        pass

    def load_cmd(self, cgen):

        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, self.name)
            return code, mask, type(self)

        if len(self) == 2:
            xmms = cgen.register('xmm')
            code = cgen.gen.load_i64x2(xmms, name=self.name)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2:
                xmms = cgen.register('ymm')
                code = cgen.gen.load_i64x4(xmms, name=self.name)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i64x2(xmm1, name=self.name)
                code += cgen.gen.load_i64x2(xmm2, name=self.name, offset=16)
                xmms = (xmm1, xmm2)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
                ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
                code = cgen.gen.load_i64x4(ymm1, name=self.name)
                code += cgen.gen.load_i64x4(ymm2, name=self.name, offset=32)
                xmms = (ymm1, ymm2)
            else:
                xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
                xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
                code = cgen.gen.load_i64x2(xmm1, name=self.name)
                code += cgen.gen.load_i64x2(xmm2, name=self.name, offset=16)
                code += cgen.gen.load_i64x2(xmm3, name=self.name, offset=32)
                code += cgen.gen.load_i64x2(xmm4, name=self.name, offset=48)
                xmms = (xmm1, xmm2, xmm3, xmm4)

        return code, xmms, type(self)

    def store_cmd(self, cgen, xmms):
        if cgen.cpu.AVX512F:
            code = "kmovw word[%s], %s\n" % (self.name, xmms)
            return code

        if len(self) == 2:
            code = cgen.gen.store_i64x2(xmms, name=self.name)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2:
                code = cgen.gen.store_i64x4(xmms, name=self.name)
            else:
                code = cgen.gen.store_i64x2(xmms[0], name=self.name)
                code += cgen.gen.store_i64x2(xmms[1], name=self.name, offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
                code = cgen.gen.store_i64x4(xmms[0], name=self.name)
                code += cgen.gen.store_i64x4(xmms[1], name=self.name, offset=32)
            else:
                code = cgen.gen.store_i64x2(xmms[0], name=self.name)
                code += cgen.gen.store_i64x2(xmms[1], name=self.name, offset=16)
                code += cgen.gen.store_i64x2(xmms[2], name=self.name, offset=32)
                code += cgen.gen.store_i64x2(xmms[3], name=self.name, offset=48)

        return code

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, type(self)) and op in ('&', '^', '|')

    def arith_with_memory(self, cgen, xmms, op, arg):
        if cgen.cpu.AVX512F:
            mask = cgen.register('mask')
            code = "kmovw %s, word[%s]\n" % (mask, arg.name)
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code += "%s %s, %s, %s\n" % (insts[op], mask, xmms, mask)
            return code, mask, type(self)

        if len(self) == 2:
            dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('xmm')
            code = cgen.gen.arith_i64x2(xmms, op, name=arg.name, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2:
                dst_xmms = xmms if cgen.can_destruct(xmms) else cgen.register('ymm')
                code = cgen.gen.arith_i64x4(xmms, op, name=arg.name, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms if cgen.can_destruct(xmms) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i64x2(xmms[0], op, name=arg.name, dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2(xmms[1], op, name=arg.name, dst_reg=dst_xmms[1], offset=16)
        elif len(self) == 8:
            if cgen.cpu.AVX2:
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

        return code, dst_xmms, type(self)

    def arith_with_arg(self, cgen, xmms1, arg2, xmms2, op):

        if cgen.cpu.AVX512F:
            mask = xmms1 if cgen.can_destruct(xmms1) else cgen.register('mask')
            insts = {"&": "kandw", "^": "kxorw", "|": "korw"}
            code = "%s %s, %s, %s\n" % (insts[op], mask, xmms1, xmms2)
            return code, mask, type(self)

        if len(self) == 2:
            dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('xmm')
            code = cgen.gen.arith_i64x2(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
        elif len(self) == 3 or len(self) == 4:
            if cgen.cpu.AVX2:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else cgen.register('ymm')
                code = cgen.gen.arith_i64x4(xmms1, op, xmm2=xmms2, dst_reg=dst_xmms)
            else:
                dst_xmms = xmms1 if cgen.can_destruct(xmms1) else (cgen.register('xmm'), cgen.register('xmm'))
                code = cgen.gen.arith_i64x2(xmms1[0], op, xmm2=xmms2[0], dst_reg=dst_xmms[0])
                code += cgen.gen.arith_i64x2(xmms1[1], op, xmm2=xmms2[1], dst_reg=dst_xmms[1])
        elif len(self) == 8:
            if cgen.cpu.AVX2:
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

        return code, dst_xmms, type(self)

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def acum_type(self, cgen):
        if self.is_multi_part(cgen):
            return 'pointer'
        elif cgen.cpu.AVX512F:
            return 'mask'
        elif cgen.cpu.AVX2 and len(self) in (3, 4):
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



class MaskI64x2Arg(MaskI64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 16

    def __len__(self):
        return 2

    @classmethod
    def type_name(cls):
        return 'maski64x2'


class MaskI64x3Arg(MaskI64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def __len__(self):
        return 3

    @classmethod
    def type_name(cls):
        return 'maski64x3'


class MaskI64x4Arg(MaskI64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 32

    def __len__(self):
        return 4

    @classmethod
    def type_name(cls):
        return 'maski64x4'


class MaskI64x8Arg(MaskI64VecBase):

    def stack_align(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def stack_size(self, cpu):
        if cpu.AVX512F:
            return 8
        return 64

    def __len__(self):
        return 8

    @classmethod
    def type_name(cls):
        return 'maski64x8'


register_arg_factory(MaskI64x2Arg, lambda: MaskI64x2Arg())
register_arg_factory(MaskI64x3Arg, lambda: MaskI64x3Arg())
register_arg_factory(MaskI64x4Arg, lambda: MaskI64x4Arg())
register_arg_factory(MaskI64x8Arg, lambda: MaskI64x8Arg())
