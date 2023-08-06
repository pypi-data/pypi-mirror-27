
from .args import ComplexArgument


class PointerArg(ComplexArgument):

    def __init__(self, arg, name=None, value=0):
        super(PointerArg, self).__init__(name)
        if not isinstance(arg, ComplexArgument):
            raise ValueError("PointerArg only accept complex arguments.", arg)
        self._arg = arg
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def arg(self):
        return self._arg

    def data_sec_repr(self):
        return 'uint64 %s = %i \n' % (self.name, self._value)

    def get_ds_value(self, ds):
        return ds[self._name]

    def set_ds_value(self, ds, value):
        ds[self._name] = int(value)

    def stack_size(self, cpu):
        return 8

    def stack_align(self, cpu):
        return 8

    def store_cmd(self, cgen, reg):
        return cgen.gen.store_i64(reg, name=self.name)

    def load_cmd(self, cgen):
        ptr_reg = cgen.register('pointer')
        code = cgen.gen.load_i64(ptr_reg, name=self.name)
        return code, ptr_reg, PointerArg(self._arg)

    @classmethod
    def type_name(cls):
        return 'pointer'

    def acum_type(self, cgen):
        return 'pointer'

    def is_subscriptable(self):
        return self._arg.is_subscriptable()

    def _allocate_ptr(self, cgen, ptr_reg=None):
        code = ''
        if ptr_reg is None:
            ptr = cgen.register('pointer')
            code = cgen.gen.load_i64(ptr, name=self.name)
        else:
            ptr = ptr_reg
        return code, ptr

    def _release_ptr(self, cgen, ptr, ptr_reg=None):
        if ptr_reg is None:
            cgen.release_reg(ptr)

    def load_item_cmd(self, cgen, index=None, reg=None, ptr_reg=None):
        code, ptr = self._allocate_ptr(cgen, ptr_reg=ptr_reg)
        co, reg, arg_type = self._arg.load_item_cmd(cgen, index=index, reg=reg, ptr_reg=ptr)
        self._release_ptr(cgen, ptr, ptr_reg=ptr_reg)
        return code + co, reg, arg_type

    def store_item_cmd(self, cgen, arg_type, src_reg, index=None, reg=None, ptr_reg=None):
        code, ptr = self._allocate_ptr(cgen, ptr_reg=ptr_reg)
        code += self._arg.store_item_cmd(cgen, arg_type, src_reg, index=index, reg=reg, ptr_reg=ptr)
        self._release_ptr(cgen, ptr, ptr_reg=ptr_reg)
        return code

    def load_attr_cmd(self, cgen, path, ptr_reg=None):
        code, ptr = self._allocate_ptr(cgen, ptr_reg=ptr_reg)
        co, reg, arg_type = self._arg.load_attr_cmd(cgen, path, ptr_reg=ptr)
        self._release_ptr(cgen, ptr, ptr_reg=ptr_reg)
        return code + co, reg, arg_type

    def store_attr_cmd(self, cgen, path, arg_type, src_reg, ptr_reg=None):
        code, ptr = self._allocate_ptr(cgen, ptr_reg=ptr_reg)
        code += self._arg.store_attr_cmd(cgen, path, arg_type, src_reg, ptr_reg=ptr)
        self._release_ptr(cgen, ptr, ptr_reg=ptr_reg)
        return code

    def store_attr_item_cmd(self, cgen, arg_type, src_reg, path, index=None, reg=None, ptr_reg=None):
        code, ptr = self._allocate_ptr(cgen, ptr_reg=ptr_reg)
        code += self._arg.store_attr_item_cmd(cgen, arg_type, src_reg, path, index=index, reg=reg, ptr_reg=ptr)
        self._release_ptr(cgen, ptr, ptr_reg=ptr_reg)
        return code

    def load_attr_item_cmd(self, cgen, path, index=None, reg=None, ptr_reg=None):
        code, ptr = self._allocate_ptr(cgen, ptr_reg=ptr_reg)
        co, reg, arg_type = self._arg.load_attr_item_cmd(cgen, path, index=index, reg=reg, ptr_reg=ptr)
        self._release_ptr(cgen, ptr, ptr_reg=ptr_reg)
        return code + co, reg, arg_type

    @classmethod
    def is_pointer(cls):
        return True
