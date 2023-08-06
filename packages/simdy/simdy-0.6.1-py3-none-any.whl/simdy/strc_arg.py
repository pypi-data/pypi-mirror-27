
from .holders import CompileError
from .args import ComplexArgument
from .ptr import PointerArg
from .usr_typ import get_user_type_factory


class struct:
    pass


class StructArg(ComplexArgument):
    """
    Abstract base class that define interface for struct type in shading language.

    All supported structure types in shading language must inherit this class.
    """

    struct_descs = {}

    def __init__(self, name=None, value=struct()):
        super(StructArg, self).__init__(name)
        if not isinstance(value, struct):
            raise TypeError("struct type expected got", value)
        self._value = value
        self._args = []
        for name in value.__slots__:
            val = getattr(value, name)
            self._args.append(val.arg_class(name, value=val))

    @property
    def value(self):
        return self._value

    @property
    def args(self):
        return self._args

    def stack_size(self, cpu):
        return self.struct_descs[self.type_name()].size()

    def stack_align(self, cpu):
        return 64

    @property
    def itemsize(self):
        return self.struct_descs[self.type_name()].size()

    def get_ds_value(self, ds):
        factory = get_user_type_factory(self.type_name())
        if factory is None:
            raise ValueError("User type %s is not registered." % self.type_name())
        new_val = factory()
        for arg in self._args:
            path = '%s.%s' % (self._name, arg.name)
            setattr(new_val, arg.name, arg.get_ds_value(ds, path))
        return new_val

    def set_ds_value(self, ds, value):
        self._value = value
        for name in value.__slots__:
            arg = self.get_arg(name)
            val = getattr(value, name)
            path = '%s.%s' % (self._name, arg.name)
            arg.set_ds_value(ds, val, name=path)

    def refresh_ds(self, ds):
        # TODO improve this
        from .arr import ArrayArg
        for arg in self._args:
            if isinstance(arg, ArrayArg):
                val = getattr(self._value, arg.name)
                path = '%s.%s' % (self._name, arg.name)
                arg.set_ds_value(ds, val, name=path)

    def data_sec_repr(self):
        return '%s %s\n' % (self.type_name(), self.name)

    def struct_desc(self):
        head = 'struct %s\n' % self.type_name()
        body = ''
        for arg in self._args:
            body += arg.data_sec_repr()
        end = 'end\n'
        return head + body + end

    def load_cmd(self, cgen, name=None):
        name = self.name if name is None else name
        ptr_reg = cgen.register('pointer')
        code = cgen.gen.load_addr(ptr_reg, name)
        return code, ptr_reg, PointerArg(self)

    def get_arg(self, path):
        for a in self._args:
            if a.name == path:
                return a
        raise CompileError("Path %s doesn't exist in structure." % path)

    def load_attr_cmd(self, cgen, path, ptr_reg=None):
        arg = self.get_arg(path)
        if ptr_reg is None:
            full_name = '%s.%s' % (self.name, path)
        else:
            full_name = "%s + %s.%s" % (ptr_reg, self.type_name(), path)
        return arg.load_cmd(cgen, name=full_name)

    def load_attr_addr(self, cgen, path, ptr_reg=None):
        if ptr_reg is None:
            full_name = '%s.%s' % (self.name, path)
        else:
            full_name = "%s + %s.%s" % (ptr_reg, self.type_name(), path)
        ptr = cgen.register('pointer')
        code = cgen.gen.load_addr(ptr, full_name)
        return code, ptr

    def store_attr_cmd(self, cgen, path, arg_type, src_reg, ptr_reg=None):
        arg = self.get_arg(path)
        if not isinstance(arg, arg_type):
            raise CompileError("Struct argument type mismatch, path=%s" % path)
        if ptr_reg is None:
            full_name = '%s.%s' % (self.name, path)
        else:
            full_name = "%s + %s.%s" % (ptr_reg, self.type_name(), path)
        return arg.store_cmd(cgen, src_reg, name=full_name)

    def store_attr_item_cmd(self, cgen, arg_type, src_reg, path, index=None, reg=None, ptr_reg=None):
        arg = self.get_arg(path)
        if not arg.is_subscriptable():
            raise ValueError("Argument %s is not subscriptable." % arg.name, arg)

        code, ptr_arr = self.load_attr_addr(cgen, path, ptr_reg=ptr_reg)
        co = arg.store_item_cmd(cgen, arg_type, src_reg, index=index, reg=reg, ptr_reg=ptr_arr)
        code += co
        cgen.release_reg(ptr_arr)
        return code

    def load_attr_item_cmd(self, cgen, path, index=None, reg=None, ptr_reg=None):
        arg = self.get_arg(path)
        if not arg.is_subscriptable():
            raise ValueError("Argument %s is not subscriptable." % arg.name, arg)

        code, ptr_arr = self.load_attr_addr(cgen, path, ptr_reg=ptr_reg)
        co, itm_reg, itm_type = arg.load_item_cmd(cgen, index=index, reg=reg, ptr_reg=ptr_arr)
        code += co
        cgen.release_reg(ptr_arr)
        return code, itm_reg, itm_type

    def set_array_item(self, addr, value):
        desc = self.struct_descs[self.type_name()]
        for arg in self._args:
            arg.set_array_item(addr + desc.offset(arg.name), getattr(value, arg.name))

    def get_array_item(self, addr):
        factory = get_user_type_factory(self.type_name())
        if factory is None:
            raise ValueError("User type %s is not registered." % self.type_name())
        desc = self.struct_descs[self.type_name()]
        new_val = factory()
        for arg in self._args:
            val = arg.get_array_item(addr + desc.offset(arg.name))
            setattr(new_val, arg.name, val)
        return new_val

    def load_item_from_array(self, cgen, ptr_reg):
        reg = cgen.register('pointer')
        code = cgen.gen.move_reg(reg, ptr_reg)
        return code, reg, PointerArg(self)

    def type_name(self):
        return self._value.__class__.__name__

    def acum_type(self, cgen):
        return 'pointer'


struct.arg_class = StructArg
