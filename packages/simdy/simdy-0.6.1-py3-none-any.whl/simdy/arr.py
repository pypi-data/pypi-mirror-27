

import x86
from tdasm import translate
from .args import ComplexArgument
from .cpy import memcopy
from .ptr import PointerArg
from .int_arg import int32, int64
from .int_vec_arg import int32x2, int32x3, int32x4, int32x8, int32x16, int64x2, int64x3, int64x4, int64x8
from .flt_arg import float32
from .dbl_arg import float64
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8


class array:
    def __init__(self, cls_factory, size=None, reserve=None):
        self._reserve = reserve if reserve is not None else 1
        self._value = cls_factory()
        self._arg = self._value.arg_class(value=self._value)
        self._itemsize = self._arg.itemsize
        self._address = x86.MemData(self._reserve * self._itemsize)
        self._size = 0
        if size is not None:
            self.resize(size)

    @property
    def arg(self):
        return self._arg

    def _resize(self):
        if self._size >= 0 and self._size <= 100:
            self._reserve += 1
        elif self._size > 100 and self._size <= 10000:
            self._reserve += 100
        elif self._size > 10000 and self._size <= 1000000:
            self._reserve += 10000
        else:
            self._reserve += 100000

        temp = x86.MemData(self._itemsize * self._reserve)
        memcopy(temp.ptr(), self._address.ptr(), self._size * self._itemsize)
        self._address = temp

    def resize(self, new_size):
        if new_size > self._size:
            if new_size > self._reserve:
                self._reserve = new_size
                temp = x86.MemData(self._itemsize * self._reserve)
                memcopy(temp.ptr(), self._address.ptr(), self._size * self._itemsize)
                self._address = temp
                self._size = new_size
            else:
                self._size = new_size
        elif new_size < self._size:
            self._size = new_size

    def __len__(self):
        return self._size

    def append(self, value):
        if self._reserve == self._size:
            self._resize()

        offset = self._itemsize * self._size
        adr = self._address.ptr() + offset
        self._arg.set_array_item(adr, value)
        self._size += 1

    def extend(self, values):
        old_size = self._size
        new_size = self._size + len(values)
        self.resize(new_size)
        adr = self._address.ptr() + self._itemsize * old_size
        for val in values:
            self._arg.set_array_item(adr, val)
            adr += self._itemsize

    def __getitem__(self, key):
        if key >= self._size:
            raise IndexError("Key is out of bounds! ", key)

        offset = self._itemsize * key
        adr = self._address.ptr() + offset
        return self._arg.get_array_item(adr)

    def __setitem__(self, key, value):
        if key >= self._size:
            raise IndexError("Key is out of bounds! ", key)

        offset = self._itemsize * key
        adr = self._address.ptr() + offset
        self._arg.set_array_item(adr, value)

    def addr(self):
        return self._address.ptr()

    @property
    def itemsize(self):
        return self._itemsize

    @classmethod
    def _from_py_array(cls, pyarray, req_typecodes, shape):
        if pyarray.typecode not in req_typecodes:
            raise ValueError("Array cannot be created. ", cls, pyarray, pyarray.typecode, pyarray.itemsize)

        length = len(pyarray) // shape
        arr = cls(size=length)
        sa, length = pyarray.buffer_info()
        memcopy(arr.addr(), sa, len(arr) * arr.itemsize)
        return arr

    def zero(self):
        self._address.fill()


class stack_array:
    def __init__(self, cls_factory, size):
        self._value = cls_factory()
        self._arg = self._value.arg_class(value=self._value)
        self._itemsize = self._arg.itemsize
        self._size = size

    @property
    def arg(self):
        return self._arg

    def __len__(self):
        return self._size

    @property
    def itemsize(self):
        return self._itemsize


def addr_calc(cgen, array, reg, ptr_reg):
    sv = {2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6, 128: 7, 256: 8, 512: 9, 1024: 10}
    if array.itemsize in sv:
        code = 'sal %s, %i\n' % (reg, sv[array.itemsize])
    else:
        code = "imul %s, %s, %i\n" % (reg, reg, array.itemsize)
    if cgen.regs.is_reg32(reg):
        reg = cgen.regs.t_32_to_64(reg)
    code += "add %s, %s\n" % (ptr_reg, reg)
    return code


def load_item_from_ptr(cgen, ptr, array, name, index=None, reg=None):
    if index is None and reg is None:
        raise ValueError("Array element cannot be loaded, index is missing!", name)

    code = ''
    if index is not None:
        if index < 0:
            raise ValueError("Negative index not supported.", index)
        offset = index * array.itemsize
        # TODO could be improved, we dont need add instruction!!!
        # TODO handle case when offset is outside 32-bit, 64-bit constant must be supported
        if offset != 0:
            code += "add %s, %i\n" % (ptr, offset)
        code1, dest_reg, ret_type = array.arg.load_item_from_array(cgen, ptr)
        code += code1
        return code, dest_reg, ret_type

    if reg is not None:
        index_reg = reg
        if not cgen.can_destruct(reg):
            index_reg = cgen.register('general') if cgen.regs.is_reg32(reg) else cgen.register('general64')
            code += cgen.gen.move_reg(index_reg, reg)
        code += addr_calc(cgen, array, index_reg, ptr)
        code1, dest_reg, ret_type = array.arg.load_item_from_array(cgen, ptr)
        code += code1
        if index_reg != reg:
            cgen.release_reg(index_reg)
        return code, dest_reg, ret_type


def store_item_to_ptr(cgen, ptr, arg_type, src_reg, array, name, index=None, reg=None):
    if index is None and reg is None:
        raise ValueError("Array element cannot be stored, index is missing!", name)

    cgen.type_arg_check(array.arg, arg_type)

    code = ''
    if index is not None:
        if index < 0:
            raise ValueError("Negative index not supported.", index)
        offset = index * array.itemsize
        # TODO could be improved, we dont need add instruction!!!
        code += "add %s, %i\n" % (ptr, offset)
        code += array.arg.store_item_to_array(cgen, ptr, src_reg)
        return code

    if reg is not None:
        index_reg = reg
        if not cgen.can_destruct(reg):
            index_reg = cgen.register('general') if cgen.regs.is_reg32(reg) else cgen.register('general64')
            code += cgen.gen.move_reg(index_reg, reg)
        code += addr_calc(cgen, array, index_reg, ptr)
        code += array.arg.store_item_to_array(cgen, ptr, src_reg)
        if index_reg != reg:
            cgen.release_reg(index_reg)
        return code


def _struc_arr_def():
    asm = """
    #DATA
    struct Array
    uint64 size
    uint64 address
    end
    """
    return asm


def _struc_arr_desc():
    code = translate(_struc_arr_def())
    desc = code.get_struct_desc('Array')
    return desc


class ArrayArg(ComplexArgument):
    array_desc = _struc_arr_desc()

    def __init__(self, name=None, value=array(int32)):
        super(ArrayArg, self).__init__(name)
        if not isinstance(value, array):
            raise TypeError("array type expected got", value)
        self._array = value

    @property
    def value(self):
        return self._array

    def data_sec_repr(self):
        return 'Array %s\n' % self.name

    def stack_size(self, cpu):
        raise ValueError("Array arg %s cannot be placed on stack." % self.name)

    def stack_align(self, cpu):
        raise ValueError("Array arg %s cannot be placed on stack." % self.name)

    @property
    def itemsize(self):
        return self.array_desc.size()

    def get_ds_value(self, ds):
        return self._array

    def set_ds_value(self, ds, value, name=None):
        if not isinstance(value, array):
            raise TypeError("Array expected got.", value)
        if type(value.arg) is not type(self._array.arg):
            raise TypeError("Wrong array type.", value)
        self._array = value
        name = self._name if name is None else name
        path = '%s.size' % name
        ds[path] = len(self._array)
        path = '%s.address' % name
        ds[path] = self._array.addr()

    def load_cmd(self, cgen, name=None):
        name = self.name if name is None else name
        ptr_reg = cgen.register('pointer')
        code = cgen.gen.load_addr(ptr_reg, name)
        return code, ptr_reg, PointerArg(self)

    def refresh_ds(self, ds):
        path = '%s.size' % self.name
        ds[path] = len(self._array)
        path = '%s.address' % self.name
        ds[path] = self._array.addr()

    def struct_desc(self):
        return _struc_arr_def()

    def is_subscriptable(self):
        return True

    def load_item_cmd(self, cgen, index=None, reg=None, ptr_reg=None):
        ptr = cgen.register('pointer')
        if ptr_reg is not None:
            full_name = "%s + Array.address" % ptr_reg
            code = "mov %s, qword [%s]\n" % (ptr, full_name)
        else:
            path = '%s.%s' % (self.name, 'address')
            code = "mov %s, qword[%s]\n" % (ptr, path)
        co, dest_reg, ret_type = load_item_from_ptr(cgen, ptr, self._array, self.name, index=index, reg=reg)
        code += co
        cgen.release_reg(ptr)
        return code, dest_reg, ret_type

    def store_item_cmd(self, cgen, arg_type, src_reg, index=None, reg=None, ptr_reg=None):
        ptr = cgen.register('pointer')
        if ptr_reg is not None:
            full_name = "%s + Array.address" % ptr_reg
            code = "mov %s, qword [%s]\n" % (ptr, full_name)
        else:
            path = '%s.%s' % (self.name, 'address')
            code = "mov %s, qword[%s]\n" % (ptr, path)

        code += store_item_to_ptr(cgen, ptr, arg_type, src_reg, self._array, self.name, index=index, reg=reg)
        cgen.release_reg(ptr)
        return code

    def type_name(self):
        return 'array_' + self._array.arg.type_name()

    def acum_type(self, cgen):
        return 'pointer'

    def set_array_item(self, addr, value):
        x86.SetUInt64(addr + self.array_desc.offset('size'), len(value), 0)
        x86.SetUInt64(addr + self.array_desc.offset('address'), value.addr(), 0)


array.arg_class = ArrayArg


class StackedArrayArg(ComplexArgument):
    array_desc = _struc_arr_desc()

    def __init__(self, name=None, value=stack_array(int32, 1)):
        super(StackedArrayArg, self).__init__(name)
        if not isinstance(value, stack_array):
            raise TypeError("array type expected got", value)
        self._array = value

    @property
    def value(self):
        return self._array

    def data_sec_repr(self):
        size = len(self._array) * self._array.itemsize
        return 'uint8 %s[%i]\n' % (self.name, size)

    def stack_size(self, cpu):
        return len(self._array) * self._array.itemsize

    def stack_align(self, cpu):
        return 64

    def get_ds_value(self, ds):
        pass

    def set_ds_value(self, ds, value):
        pass

    def load_cmd(self, cgen, name=None):
        name = self.name if name is None else name
        ptr_reg = cgen.register('pointer')
        code = cgen.gen.load_addr(ptr_reg, name)
        return code, ptr_reg, PointerArg(self)

    def is_subscriptable(self):
        return True

    def struct_desc(self):
        return _struc_arr_def()

    def load_item_cmd(self, cgen, index=None, reg=None, ptr_reg=None):
        ptr = cgen.register('pointer')
        if ptr_reg is None:
            code = cgen.gen.load_addr(ptr, self.name)
        else:
            code = 'mov %s, %s\n' % (ptr, ptr_reg)
        co, dest_reg, ret_type = load_item_from_ptr(cgen, ptr, self._array, self.name, index=index, reg=reg)
        code += co
        cgen.release_reg(ptr)
        return code, dest_reg, ret_type

    def store_item_cmd(self, cgen, arg_type, src_reg, index=None, reg=None, ptr_reg=None):
        ptr = cgen.register('pointer')
        if ptr_reg is None:
            code = cgen.gen.load_addr(ptr, self.name)
        else:
            code = 'mov %s, %s\n' % (ptr, ptr_reg)
        code += store_item_to_ptr(cgen, ptr, arg_type, src_reg, self._array, self.name, index=index, reg=reg)
        cgen.release_reg(ptr)
        return code

    def type_name(self):
        return 'array_' + self._array.arg.type_name()

    def acum_type(self, cgen):
        return 'pointer'


stack_array.arg_class = StackedArrayArg


class array_int32(array):
    def __init__(self, size=None, reserve=None):
        super(array_int32, self).__init__(int32, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int32, cls)._from_py_array(pyarray, ['i', 'l'], shape=1)


class array_int64(array):
    def __init__(self, size=None, reserve=None):
        super(array_int64, self).__init__(int64, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int64, cls)._from_py_array(pyarray, ['q'], shape=1)


class array_float32(array):
    def __init__(self, size=None, reserve=None):
        super(array_float32, self).__init__(float32, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float32, cls)._from_py_array(pyarray, ['f'], shape=1)


class array_float64(array):
    def __init__(self, size=None, reserve=None):
        super(array_float64, self).__init__(float64, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float64, cls)._from_py_array(pyarray, ['d'], shape=1)


class array_int32x2(array):
    def __init__(self, size=None, reserve=None):
        super(array_int32x2, self).__init__(int32x2, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int32x2, cls)._from_py_array(pyarray, ['i', 'l'], shape=2)


class array_int32x3(array):
    def __init__(self, size=None, reserve=None):
        super(array_int32x3, self).__init__(int32x3, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int32x3, cls)._from_py_array(pyarray, ['i', 'l'], shape=3)


class array_int32x4(array):
    def __init__(self, size=None, reserve=None):
        super(array_int32x4, self).__init__(int32x4, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int32x4, cls)._from_py_array(pyarray, ['i', 'l'], shape=4)


class array_int32x8(array):
    def __init__(self, size=None, reserve=None):
        super(array_int32x8, self).__init__(int32x8, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int32x8, cls)._from_py_array(pyarray, ['i', 'l'], shape=8)


class array_int32x16(array):
    def __init__(self, size=None, reserve=None):
        super(array_int32x16, self).__init__(int32x16, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int32x16, cls)._from_py_array(pyarray, ['i', 'l'], shape=16)


class array_int64x2(array):
    def __init__(self, size=None, reserve=None):
        super(array_int64x2, self).__init__(int64x2, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int64x2, cls)._from_py_array(pyarray, ['q'], shape=2)

class array_int64x3(array):
    def __init__(self, size=None, reserve=None):
        super(array_int64x3, self).__init__(int64x3, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int64x3, cls)._from_py_array(pyarray, ['q'], shape=3)

class array_int64x4(array):
    def __init__(self, size=None, reserve=None):
        super(array_int64x4, self).__init__(int64x4, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int64x4, cls)._from_py_array(pyarray, ['q'], shape=4)

class array_int64x8(array):
    def __init__(self, size=None, reserve=None):
        super(array_int64x8, self).__init__(int64x8, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_int64x8, cls)._from_py_array(pyarray, ['q'], shape=8)


class array_float32x2(array):
    def __init__(self, size=None, reserve=None):
        super(array_float32x2, self).__init__(float32x2, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float32x2, cls)._from_py_array(pyarray, ['f'], shape=2)


class array_float32x3(array):
    def __init__(self, size=None, reserve=None):
        super(array_float32x3, self).__init__(float32x3, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float32x3, cls)._from_py_array(pyarray, ['f'], shape=3)


class array_float32x4(array):
    def __init__(self, size=None, reserve=None):
        super(array_float32x4, self).__init__(float32x4, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float32x4, cls)._from_py_array(pyarray, ['f'], shape=4)


class array_float32x8(array):
    def __init__(self, size=None, reserve=None):
        super(array_float32x8, self).__init__(float32x8, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float32x8, cls)._from_py_array(pyarray, ['f'], shape=8)


class array_float32x16(array):
    def __init__(self, size=None, reserve=None):
        super(array_float32x16, self).__init__(float32x16, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float32x16, cls)._from_py_array(pyarray, ['f'], shape=16)


class array_float64x2(array):
    def __init__(self, size=None, reserve=None):
        super(array_float64x2, self).__init__(float64x2, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float64x2, cls)._from_py_array(pyarray, ['d'], shape=2)


class array_float64x3(array):
    def __init__(self, size=None, reserve=None):
        super(array_float64x3, self).__init__(float64x3, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float64x3, cls)._from_py_array(pyarray, ['d'], shape=3)


class array_float64x4(array):
    def __init__(self, size=None, reserve=None):
        super(array_float64x4, self).__init__(float64x4, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float64x4, cls)._from_py_array(pyarray, ['d'], shape=4)


class array_float64x8(array):
    def __init__(self, size=None, reserve=None):
        super(array_float64x8, self).__init__(float64x8, size=size, reserve=reserve)

    @classmethod
    def from_py_array(cls, pyarray):
        return super(array_float64x8, cls)._from_py_array(pyarray, ['d'], shape=8)
