

import x86
from .cgen import register_arg_factory
from .args import Argument
from .holders import CompileError


class int32(int):
    pass


class Int32Arg(Argument):

    def __init__(self, name=None, value=int32()):
        super(Int32Arg, self).__init__(name)
        if not isinstance(value, int32):
            raise TypeError("int32 type expected got", value)
        self._value = value

    @property
    def value(self):
        return self._value

    def data_sec_repr(self):
        return 'int32 %s = %i \n' % (self.name, self._value)

    def stack_size(self, cpu):
        return 4

    def stack_align(self, cpu):
        return 4

    @property
    def itemsize(self):
        return 4

    def get_ds_value(self, ds, name=None):
        name = self._name if name is None else name
        return int32(ds[name])

    def set_ds_value(self, ds, value, name=None):
        name = self._name if name is None else name
        ds[name] = int32(value)

    def store_cmd(self, cgen, reg, name=None):
        name = self.name if name is None else name
        return cgen.gen.store_i32(reg, name=name)

    def load_cmd(self, cgen, name=None):
        name = self.name if name is None else name
        reg = cgen.register('general')
        code = cgen.gen.load_i32(reg, name=name)
        return code, reg, Int32Arg

    def can_operate_with_const(self, cgen, op, value):
        if not isinstance(value, int):
            return False
        if value > 2147483647 or value < -2147483648:
            return False
        elif op in ('+', '*', '-', '>>', '<<', '&', '^', '|'):
            return True
        else:
            return False

    def can_operate_with_memory(self, cgen, arg, op):
        return isinstance(arg, Int32Arg) and op in ('+', '*', '-', '&', '^', '|')

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, Int32Arg) and op in ('+', '*', '-', '/', '%', '&', '^', '|', '<<', '>>')

    def can_cond_with_const(self, cgen, value, op):
        return isinstance(value, int) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_mem(self, cgen, arg, op):
        return isinstance(arg, Int32Arg) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_arg(self, cgen, arg, op):
        return isinstance(arg, Int32Arg) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_zero(self, cgen):
        return True

    def _cond_operators(self, satisfied):
        if satisfied:
            cons = {'==': 'je', '<': 'jl', '>': 'jg',
                    '<=': 'jle', '>=': 'jge', '!=': 'jne'}
        else:
            cons = {'==': 'jne', '<': 'jge', '>': 'jle',
                    '<=': 'jg', '>=': 'jl', '!=': 'je'}
        return cons

    def cond_with_const(self, cgen, reg1, value, op, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        code = 'cmp %s, %i\n' % (reg1, value)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_mem(self, cgen, reg1, op, arg, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        code = 'cmp %s, dword [%s]\n' % (reg1, arg.name)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_arg(self, cgen, reg1, arg2, reg2, op, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        code = 'cmp %s, %s\n' % (reg1, reg2)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_zero(self, cgen, reg1, jump_label, satisfied):
        code = 'cmp %s, 0\n' % reg1
        if satisfied:
            code += "jne %s\n" % jump_label
        else:
            code += "je %s\n" % jump_label
        return code

    def arith_with_const(self, cgen, reg, op, value):
        if cgen.can_destruct(reg):
            code = cgen.gen.arith_i32(reg, op, value=value)
            return code, reg, Int32Arg
        else:
            dest = cgen.register('general')
            code1 = cgen.gen.move_reg(dest, reg)
            code2 = cgen.gen.arith_i32(dest, op, value=value)
            return code1 + code2, dest, Int32Arg

    def arith_with_memory(self, cgen, reg, op, arg):
        if cgen.can_destruct(reg):
            code = cgen.gen.arith_i32(reg, op, name=arg.name)
            return code, reg, Int32Arg
        else:
            dest = cgen.register('general')
            code1 = cgen.gen.move_reg(dest, reg)
            code2 = cgen.gen.arith_i32(dest, op, name=arg.name)
            return code1 + code2, dest, Int32Arg

    def arith_with_arg(self, cgen, reg, arg2, reg2, op):
        tmp1, tmp2 = None, None
        if op in ('<<', '>>', '/', '%'):
            tmp1, tmp2 = cgen.register('general'), cgen.register('general')
        if cgen.can_destruct(reg):
            code = cgen.gen.arith_i32(reg, op, src_reg=reg2, tmp_reg1=tmp1, tmp_reg2=tmp2)
            dest_reg = reg
        elif cgen.can_destruct(reg2) and op in ('+', '*', '&', '^', '|'):
            code = cgen.gen.arith_i32(reg2, op, src_reg=reg, tmp_reg1=tmp1, tmp_reg2=tmp2)
            dest_reg = reg2
        else:
            dest = cgen.register('general')
            code = cgen.gen.move_reg(dest, reg)
            code += cgen.gen.arith_i32(dest, op, src_reg=reg2, tmp_reg1=tmp1, tmp_reg2=tmp2)
            dest_reg = dest
        if tmp1 is not None:
            cgen.release_reg(tmp1)
        if tmp2 is not None:
            cgen.release_reg(tmp2)
        return code, dest_reg, Int32Arg

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)

        if self.can_operate_with_memory(cgen, arg2, op):
            return self.arith_with_memory(cgen, reg1, op, arg2)
        else:
            tmp_reg = cgen.register('general')
            code = cgen.gen.load_i32(tmp_reg, name=arg2.name)
            co, dest_reg, typ = self.arith_with_arg(cgen, reg1, arg2, tmp_reg, op)
            if dest_reg != tmp_reg:
                cgen.release_reg(tmp_reg)
            return code + co, dest_reg, typ

    def do_unary_op(self, cgen, reg, op):
        if op not in ('+', '-', '~'):
            raise CompileError("Unsupported unary operation %s!" % str(op))
        code = ''
        if op == '-':
            code = 'neg %s\n' % reg
        elif op == '~':
            code = 'not %s\n' % reg

        return code, reg, Int32Arg

    @classmethod
    def type_name(cls):
        return 'int32'

    def acum_type(self, cgen):
        return 'general'

    def set_array_item(self, addr, value):
        if not isinstance(value, int):
            raise TypeError("Expected %s got %s" % (int32, type(value)))
        x86.SetInt32(addr, value, 0)

    def get_array_item(self, addr):
        return int32(x86.GetInt32(addr, 0, 0))

    def load_item_from_array(self, cgen, ptr_reg):
        reg = cgen.register('general')
        code = cgen.gen.load_i32(reg, ptr_reg=ptr_reg)
        return code, reg, Int32Arg

    def store_item_to_array(self, cgen, ptr_reg, reg):
        return cgen.gen.store_i32(reg, ptr_reg=ptr_reg)


int32.arg_class = Int32Arg

register_arg_factory(Int32Arg, lambda: Int32Arg())


class int64(int):
    pass


class Int64Arg(Argument):

    def __init__(self, name=None, value=int64()):
        super(Int64Arg, self).__init__(name)
        if not isinstance(value, int64):
            raise TypeError("int64 type expected got", value)
        self._value = value

    @property
    def value(self):
        return self._value

    def data_sec_repr(self):
        return 'int64 %s = %i \n' % (self.name, self._value)

    def stack_size(self, cpu):
        return 8

    def stack_align(self, cpu):
        return 8

    @property
    def itemsize(self):
        return 8

    def get_ds_value(self, ds, name=None):
        name = self._name if name is None else name
        return int64(ds[name])

    def set_ds_value(self, ds, value, name=None):
        name = self._name if name is None else name
        ds[name] = int64(value)

    def store_cmd(self, cgen, reg, name=None):
        name = self.name if name is None else name
        return cgen.gen.store_i64(reg, name=name)

    def load_cmd(self, cgen, name=None):
        name = self.name if name is None else name
        reg = cgen.register('general64')
        code = cgen.gen.load_i64(reg, name=name)
        return code, reg, Int64Arg

    def can_operate_with_const(self, cgen, op, value):
        if not isinstance(value, int):
            return False
        if value > 9223372036854775807 or value < -9223372036854775808:
            return False
        if op not in ('+', '*', '-', '/', '%', '&', '^', '|', '<<', '>>'):
            return False
        return True

    def can_operate_with_memory(self, cgen, arg, op):
        return isinstance(arg, Int64Arg) and op in ('+', '*', '-', '&', '^', '|')

    def can_operate_with_arg(self, cgen, arg, op):
        return isinstance(arg, Int64Arg) and op in ('+', '*', '-', '/', '%', '&', '^', '|', '<<', '>>')

    def can_cond_with_const(self, cgen, value, op):
        return isinstance(value, int) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_mem(self, cgen, arg, op):
        return isinstance(arg, Int64Arg) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_arg(self, cgen, arg, op):
        return isinstance(arg, Int64Arg) and op in ('>', '<', '==', '<=', '>=', '!=')

    def can_cond_with_zero(self, cgen):
        return True

    def _cond_operators(self, satisfied):
        if satisfied:
            cons = {'==': 'je', '<': 'jl', '>': 'jg',
                    '<=': 'jle', '>=': 'jge', '!=': 'jne'}
        else:
            cons = {'==': 'jne', '<': 'jge', '>': 'jle',
                    '<=': 'jg', '>=': 'jl', '!=': 'je'}
        return cons

    def cond_with_const(self, cgen, reg1, value, op, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        code = 'cmp %s, %i\n' % (reg1, value)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_mem(self, cgen, reg1, op, arg, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        code = 'cmp %s, qword [%s]\n' % (reg1, arg.name)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_arg(self, cgen, reg1, arg2, reg2, op, jump_label, satisfied):
        cons = self._cond_operators(satisfied)
        code = 'cmp %s, %s\n' % (reg1, reg2)
        code += "%s %s\n" % (cons[op], jump_label)
        return code

    def cond_with_zero(self, cgen, reg1, jump_label, satisfied):
        code = 'cmp %s, 0\n' % reg1
        if satisfied:
            code += "jne %s\n" % jump_label
        else:
            code += "je %s\n" % jump_label
        return code

    def arith_with_const(self, cgen, reg, op, value):
        tmp1, tmp2 = None, None
        if op in ('/', '%'):
            tmp1, tmp2 = cgen.register('general64'), cgen.register('general64')

        dest, code = reg, ''
        if not cgen.can_destruct(reg):
            dest = cgen.register('general64')
            code = cgen.gen.move_reg(dest, reg)

        if op in ('/', '%') or value > 2147483647 or value < -2147483648:
            tmp = cgen.register('general64')
            code += 'mov %s, %i\n' % (tmp, value)
            code += cgen.gen.arith_i64(dest, op, src_reg=tmp, tmp_reg1=tmp1, tmp_reg2=tmp2)
            cgen.release_reg(tmp)
        else:
            code += cgen.gen.arith_i64(dest, op, value=value, tmp_reg1=tmp1, tmp_reg2=tmp2)

        if tmp1 is not None:
            cgen.release_reg(tmp1)
        if tmp2 is not None:
            cgen.release_reg(tmp2)
        return code, dest, Int64Arg

    def arith_with_memory(self, cgen, reg, op, arg):
        if cgen.can_destruct(reg):
            code = cgen.gen.arith_i64(reg, op, name=arg.name)
            return code, reg, Int64Arg
        else:
            dest = cgen.register('general64')
            code1 = cgen.gen.move_reg(dest, reg)
            code2 = cgen.gen.arith_i64(dest, op, name=arg.name)
            return code1 + code2, dest, Int64Arg

    def arith_with_arg(self, cgen, reg, arg2, reg2, op):
        tmp1, tmp2 = None, None
        if op in ('<<', '>>', '/', '%'):
            tmp1, tmp2 = cgen.register('general64'), cgen.register('general64')
        if cgen.can_destruct(reg):
            code = cgen.gen.arith_i64(reg, op, src_reg=reg2, tmp_reg1=tmp1, tmp_reg2=tmp2)
            dest_reg = reg
        elif cgen.can_destruct(reg2) and op in ('+', '*', '&', '^', '|'):
            code = cgen.gen.arith_i64(reg2, op, src_reg=reg, tmp_reg1=tmp1, tmp_reg2=tmp2)
            dest_reg = reg2
        else:
            dest = cgen.register('general64')
            code = cgen.gen.move_reg(dest, reg)
            code += cgen.gen.arith_i64(dest, op, src_reg=reg2, tmp_reg1=tmp1, tmp_reg2=tmp2)
            dest_reg = dest
        if tmp1 is not None:
            cgen.release_reg(tmp1)
        if tmp2 is not None:
            cgen.release_reg(tmp2)
        return code, dest_reg, Int64Arg

    def arith_arg_cmd(self, cgen, op, arg2, reg1, reg2=None):
        if reg2 is not None:
            return self.arith_with_arg(cgen, reg1, arg2, reg2, op)

        if self.can_operate_with_memory(cgen, arg2, op):
            return self.arith_with_memory(cgen, reg1, op, arg2)
        else:
            tmp_reg = cgen.register('general64')
            code = cgen.gen.load_i64(tmp_reg, name=arg2.name)
            co, dest_reg, typ = self.arith_with_arg(cgen, reg1, arg2, tmp_reg, op)
            if dest_reg != tmp_reg:
                cgen.release_reg(tmp_reg)
            return code + co, dest_reg, typ

    def do_unary_op(self, cgen, reg, op):
        if op not in ('+', '-', '~'):
            raise CompileError("Unsupported unary operation %s!" % str(op))
        code = ''
        if op == '-':
            code = 'neg %s\n' % reg
        elif op == '~':
            code = 'not %s\n' % reg

        return code, reg, Int64Arg

    @classmethod
    def type_name(cls):
        return 'int64'

    def acum_type(self, cgen):
        return 'general64'

    def set_array_item(self, addr, value):
        if not isinstance(value, int):
            raise TypeError("Expected %s got %s" % (int64, type(value)))
        x86.SetInt64(addr, value, 0)

    def get_array_item(self, addr):
        return int64(x86.GetInt64(addr, 0, 0))

    def load_item_from_array(self, cgen, ptr_reg):
        reg = cgen.register('general64')
        code = cgen.gen.load_i64(reg, ptr_reg=ptr_reg)
        return code, reg, Int64Arg

    def store_item_to_array(self, cgen, ptr_reg, reg):
        return cgen.gen.store_i64(reg, ptr_reg=ptr_reg)


int64.arg_class = Int64Arg

register_arg_factory(Int64Arg, lambda: Int64Arg())
