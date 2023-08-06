
import x86
from .cgen import register_arg_factory
from .args import Argument
from .holders import CompileError

class float64(float):
    pass


class Float64Arg(Argument):
    def __init__(self, name=None, value=float64()):
        super(Float64Arg, self).__init__(name)
        if not isinstance(value, float64):
            raise TypeError("float64 type expected got", value)
        self._value = value

    @property
    def value(self):
        return self._value

    def data_sec_repr(self):
        return 'double %s = %s\n' % (self.name, repr(self._value))

    def stack_size(self, cpu):
        return 8

    def stack_align(self, cpu):
        return 8

    @property
    def itemsize(self):
        return 8

    def get_ds_value(self, ds, name=None):
        name = self._name if name is None else name
        return float64(ds[name])

    def set_ds_value(self, ds, value, name=None):
        name = self._name if name is None else name
        ds[name] = float64(value)

    def load_cmd(self, cgen, name=None):
        name = self.name if name is None else name
        xmm = cgen.register('xmm')
        code = cgen.gen.load_f64(xmm, name=name)
        return code, xmm, Float64Arg

    def store_cmd(self, cgen, xmm, name=None):
        name = self.name if name is None else name
        return cgen.gen.store_f64(xmm, name=name)

    def fma_supported(self, cgen):
        return True

    def can_operate_with_const(self, cgen, op, value):
        return isinstance(value, (int, float)) and op in ('+', '-', '/', '*', '>', '<', '==', '<=', '>=', '!=')

    def can_operate_with_memory(self, cgen, arg, op):
        return isinstance(arg, Float64Arg) and op in ('+', '-', '/', '*', '>', '<', '==', '<=', '>=', '!=')

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, Float64Arg) and op in ('+', '-', '/', '*', '>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_zero(self, cgen):
        return True

    def can_cond_with_const(self, cgen, value, op):
        return isinstance(value, (int, float)) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_mem(self, cgen, arg, op):
        return isinstance(arg, Float64Arg) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_arg(self, cgen, arg, op):
        return isinstance(arg, Float64Arg) and op in ('>', '<', '==', '<=', '>=', '!=')

    def cond_with_zero(self, cgen, reg1, jump_label, satisfied):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vxorpd %s, %s, %s\n' % (xmm, xmm, xmm)
            code += 'vucomisd %s, %s\n' % (reg1, xmm)
        else:
            code = 'xorpd %s, %s\n' % (xmm, xmm)
            code += 'ucomisd %s, %s\n' % (reg1, xmm)
        if satisfied:
            code += "jne %s\n" % jump_label
        else:
            code += "je %s\n" % jump_label
        cgen.release_reg(xmm)
        return code

    def _cond_operators(self, satisfied):
        if satisfied:
            cons = {'==': 'je', '<': 'jb', '>': 'ja',
                    '<=': 'jbe', '>=': 'jae', '!=': 'jne'}
        else:
            cons = {'==': 'jne', '<': 'jae', '>': 'jbe',
                    '<=': 'ja', '>=': 'jb', '!=': 'je'}
        return cons

    def cond_with_arg(self, cgen, reg1, arg2, reg2, op, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vucomisd %s, %s\n' % (reg1, reg2)
        else:
            code = 'ucomisd %s, %s\n' % (reg1, reg2)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_mem(self, cgen, reg1, op, arg, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vucomisd %s, qword [%s]\n' % (reg1, arg.name)
        else:
            code = 'ucomisd %s, qword[%s]\n' % (reg1, arg.name)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_const(self, cgen, reg1, value, op, jump_label, satisfied):
        arg = Float64Arg(value=float64(value))
        const_arg = cgen.create_const(arg)
        return self.cond_with_mem(cgen, reg1, op, const_arg, jump_label, satisfied)

    def arith_with_const(self, cgen, reg, op, value):
        arg = Float64Arg(value=float64(value))
        const_arg = cgen.create_const(arg)
        return self.arith_with_memory(cgen, reg, op, const_arg)

    def arith_with_memory(self, cgen, reg, op, arg):
        xmm3 = None
        if not cgen.can_destruct(reg):
            xmm3 = cgen.register('xmm')
        code = cgen.gen.arith_f64(reg, op, name=arg.name, dst_reg=xmm3)
        dest_reg = reg if xmm3 is None else xmm3
        return code, dest_reg, Float64Arg

    def arith_with_arg(self, cgen, reg, arg2, reg2, op):
        if cgen.can_destruct(reg):
            code = cgen.gen.arith_f64(reg, op, xmm2=reg2)
            dest_reg = reg
        elif cgen.can_destruct(reg2) and op in ('+', '*'):
            code = cgen.gen.arith_f64(reg2, op, xmm2=reg)
            dest_reg = reg2
        else:
            xmm3 = cgen.register('xmm')
            code = cgen.gen.arith_f64(reg, op, xmm2=reg2, dst_reg=xmm3)
            dest_reg = xmm3
        return code, dest_reg, Float64Arg

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)
        return self.arith_with_memory(cgen, reg1, op, arg2)

    def do_unary_op(self, cgen, xmm, op):
        if op not in ('+', '-'):
            raise CompileError("Unsupported unary operation %s!" % str(op))

        if op == '+':
            return '', xmm, Float64Arg

        xmm2 = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vxorpd %s, %s, %s\n' % (xmm2, xmm2, xmm2)
            code += 'vsubsd %s, %s, %s\n' % (xmm2, xmm2, xmm)
        else:
            code = 'xorpd %s, %s\n' % (xmm2, xmm2)
            code += 'subsd %s, %s\n' % (xmm2, xmm)

        return code, xmm2, Float64Arg

    def fma_cmd(self, cgen, arg2, op, reverse, arg3, reg1, reg2, reg3=None):
        # arg1 * arg2 +/- arg3
        # arg3 +/- arg1 * arg2
        if cgen.cpu.FMA:
            negate = reverse and op == '-'
            if negate:
                op = '+'
            if cgen.can_destruct(reg1):
                code = cgen.gen.fma_f64_213(reg1, reg2, op, negate, xmm3=reg3, name=arg3.name)
                dest_reg = reg1
            elif cgen.can_destruct(reg2):
                code = cgen.gen.fma_f64_213(reg2, reg1, op, negate, xmm3=reg3, name=arg3.name)
                dest_reg = reg2
            elif reg3 is not None and cgen.can_destruct(reg3):
                code = cgen.gen.fma_f64_231(reg3, reg1, op, negate, xmm3=reg2)
                dest_reg = reg3
            else:
                xmm4 = cgen.register('xmm')
                code = cgen.gen.move_reg(xmm4, reg1)
                code += cgen.gen.fma_f64_213(xmm4, reg2, op, negate, xmm3=reg3, name=arg3.name)
                dest_reg = xmm4
        else:
            code4, reg4, typ4 = self.arith_with_arg(cgen, reg1, arg2, reg2, '*')
            arg4 = cgen.arg_factory(typ4)
            if reverse and op == '-':
                if reg3 is not None:
                    code5, arg5, reg5 = "", arg3, reg3
                else:
                    code5, reg5, typ5 = arg3.load_cmd(cgen)
                    arg5 = cgen.arg_factory(typ5)
                code6, reg6, typ6 = arg5.arith_with_arg(cgen, reg5, arg4, reg4, op)

                if reg4 not in (reg6, reg1, reg2):
                    cgen.release_reg(reg4)
                if reg5 not in (reg6, reg1, reg2, reg4):
                    cgen.release_reg(reg5)
                dest_reg = reg6
                code = code4 + code5 + code6
            else:
                code5, reg5, typ5 = self.arith_arg_cmd(cgen, op, arg3, reg1=reg4, reg2=reg3)
                if reg4 not in (reg5, reg1, reg2):
                    cgen.release_reg(reg4)
                dest_reg = reg5
                code = code4 + code5

        return code, dest_reg, Float64Arg

    def set_array_item(self, addr, value):
        if not isinstance(value, float):
            raise TypeError("Expected %s got %s" % (float64, type(value)))
        x86.SetDouble(addr, value, 0)

    def get_array_item(self, addr):
        return float64(x86.GetDouble(addr, 0, 0))

    @classmethod
    def type_name(cls):
        return 'float64'

    def acum_type(self, cgen):
        return 'xmm'

    def load_item_from_array(self, cgen, ptr_reg):
        xmm = cgen.register('xmm')
        code = cgen.gen.load_f64(xmm, ptr_reg=ptr_reg)
        return code, xmm, Float64Arg

    def store_item_to_array(self, cgen, ptr_reg, xmm):
        return cgen.gen.store_f64(xmm, ptr_reg=ptr_reg)


float64.arg_class = Float64Arg

register_arg_factory(Float64Arg, lambda: Float64Arg())
