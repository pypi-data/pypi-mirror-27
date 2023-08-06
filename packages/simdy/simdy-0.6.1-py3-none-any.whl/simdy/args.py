
from abc import ABCMeta, abstractmethod


class Argument(metaclass=ABCMeta):
    """
    Abstract base class that define interface for type in shading language.

    All supported types in shading language must inherit this class.
    """

    def __init__(self, name=None):
        self._name = name
        if self._name is None:
            self._name = 'var_%i' % id(self)

    @property
    def name(self):
        return self._name

    @abstractmethod
    def data_sec_repr(self):
        pass

    @abstractmethod
    def stack_size(self, cpu):
        pass

    @abstractmethod
    def stack_align(self, cpu):
        pass

    @abstractmethod
    def get_ds_value(self, ds, name=None):
        pass

    @abstractmethod
    def set_ds_value(self, ds, value, name=None):
        pass

    def store_cmd(self, cgen, reg):
        raise NotImplementedError()

    def load_cmd(self, cgen, name=None):
        raise NotImplementedError()

    def can_operate_with_const(self, cgen, op, value):
        return False

    def can_operate_with_arg(self, cgen, arg, op):
        return False

    def arith_with_const(self, cgen, reg, op, value):
        raise NotImplementedError()

    def arith_with_memory(self, cgen, reg, op, arg):
        raise NotImplementedError()

    def arith_with_arg(self, cgen, reg, arg2, reg2, op):
        raise NotImplementedError()

    def do_unary_op(self, cgen, reg, op):
        raise NotImplementedError()

    def fma_supported(self, cgen):
        return False

    def can_cond_with_zero(self, cgen):
        return False

    def can_cond_with_const(self, cgen, value, op):
        return False

    def can_cond_with_mem(self, cgen, arg, op):
        return False

    def can_cond_with_arg(self, cgen, arg, op):
        return False

    def cond_with_zero(self, cgen, reg1, jump_label, satisfied):
        raise NotImplementedError()

    def cond_with_const(self, cgen, reg1, value, op, jump_label, satisfied):
        raise NotImplementedError()

    def cond_with_arg(self, cgen, reg1, arg2, reg2, op, jump_label, satisfied):
        raise NotImplementedError()

    def cond_with_mem(self, cgen, reg1, op, arg, jump_label, satisfied):
        raise NotImplementedError()

    def is_subscriptable(self):
        return False

    def load_item_cmd(self, cgen, index=None, reg=None):
        raise NotImplementedError()

    def store_item_cmd(self, cgen, arg_type, xmm, index=None, reg=None):
        raise NotImplementedError()

    @classmethod
    def type_name(cls):
        raise NotImplementedError()

    def acum_type(self, cgen):
        raise NotImplementedError()

    @classmethod
    def is_pointer(cls):
        return False

    def is_multi_part(self, cgen):
        return False


class ComplexArgument(Argument):

    def refresh_ds(self, ds):
        pass

    def struct_desc(self):
        return ''
