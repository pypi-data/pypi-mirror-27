

from tdasm import translate, Runtime
from array import array


_asm_code = """
    #DATA
    uint64 sa, da, n

    #CODE
    mov rcx, qword [n]
    mov rsi, qword [sa]
    mov rdi, qword [da]
    rep movsb
"""

_runtime = Runtime()
_data = _runtime.load("memcopy", translate(_asm_code))


def memcopy(da, sa, n):
    """Copy n bytes form source address(sa) to destination address(da)."""
    _data["da"] = da
    _data["sa"] = sa
    _data["n"] = n
    _runtime.run("memcopy")


if __name__ == '__main__':

    arr = array('f')
    arr.append(5)
    arr.append(9)

    arr2 = array('f')
    arr2.append(59)
    arr2.append(79)

    sa, nelem = arr.buffer_info()
    da, nelem2 = arr2.buffer_info()

    memcopy(da, sa, 8)
    print(arr)
    print(arr2)
