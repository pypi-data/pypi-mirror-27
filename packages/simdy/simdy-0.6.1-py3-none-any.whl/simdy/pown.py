
from .int_arg import int32
from .dbl_arg import float64
from .flt_arg import float32
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []


pown_f64 = """
def pown(x: float64, n: int32) -> float64:
    result = 1.0
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return 1.0 / result
"""

register_kernel('pown', (('x', float64()), ('n', int32())), pown_f64, optimize=True)


pown_f64x2 = """
def pown(x: float64x2, n: int32) -> float64x2:
    result = float64x2(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float64x2(1.0) / result
"""

register_kernel('pown', (('x', float64x2()), ('n', int32())), pown_f64x2, optimize=True)


pown_f64x3 = """
def pown(x: float64x3, n: int32) -> float64x3:
    result = float64x3(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float64x3(1.0) / result
"""

register_kernel('pown', (('x', float64x3()), ('n', int32())), pown_f64x3, optimize=True)


pown_f64x4 = """
def pown(x: float64x4, n: int32) -> float64x4:
    result = float64x4(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float64x4(1.0) / result
"""

register_kernel('pown', (('x', float64x4()), ('n', int32())), pown_f64x4, optimize=True)


pown_f64x8 = """
def pown(x: float64x8, n: int32) -> float64x8:
    result = float64x8(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float64x8(1.0) / result
"""

register_kernel('pown', (('x', float64x8()), ('n', int32())), pown_f64x8, optimize=True)


pown_f32 = """
def pown(x: float32, n: int32) -> float32:
    result = float32(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float32(1.0) / result
"""

register_kernel('pown', (('x', float32()), ('n', int32())), pown_f32, optimize=True)


pown_f32x2 = """
def pown(x: float32x2, n: int32) -> float32x2:
    result = float32x2(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float32x2(1.0) / result
"""

register_kernel('pown', (('x', float32x2()), ('n', int32())), pown_f32x2, optimize=True)


pown_f32x3 = """
def pown(x: float32x3, n: int32) -> float32x3:
    result = float32x3(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float32x3(1.0) / result
"""

register_kernel('pown', (('x', float32x3()), ('n', int32())), pown_f32x3, optimize=True)


pown_f32x4 = """
def pown(x: float32x4, n: int32) -> float32x4:
    result = float32x4(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float32x4(1.0) / result
"""

register_kernel('pown', (('x', float32x4()), ('n', int32())), pown_f32x4, optimize=True)


pown_f32x8 = """
def pown(x: float32x8, n: int32) -> float32x8:
    result = float32x8(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float32x8(1.0) / result
"""

register_kernel('pown', (('x', float32x8()), ('n', int32())), pown_f32x8, optimize=False)


pown_f32x16 = """
def pown(x: float32x16, n: int32) -> float32x16:
    result = float32x16(1.0)
    tmp = x

    an = abs(n)
    while an > 0:
        if an & 1:
            result *= tmp
        tmp *= tmp
        an >>= 1

    if n >= 0:
        return result
    return float32x16(1.0) / result
"""

register_kernel('pown', (('x', float32x16()), ('n', int32())), pown_f32x16, optimize=True)
