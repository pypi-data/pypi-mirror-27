
from .dbl_arg import float64
from .flt_arg import float32
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []

# ACCURACY:
#
#                      Relative error:
# arithmetic   domain      # trials      peak         rms
#     DEC       0, 10       150000       3.0e-17     7.8e-18
#     IEEE -1.07e9,+1.07e9  130000       2.1e-16     5.4e-17

sin_f64 = """
def sin(x: float64) -> float64:
    sign = 1.0
    if x < 0:
        x = x * -1
        sign = -1.0

    if x > 1.073741824e9:
        return 0.0

    y = floor(x * 1.2732395447351628)
    z = y - floor(y * 0.0625) * 16.0

    j = int32(z)
    if j & 1:
        y = y + 1.0
        j = j + 1

    j = j & 7
    if j > 3:
        sign = sign * -1.0
        j = j - 4

    z = ((x - y * 7.85398125648498535156E-1) - y * 3.77489470793079817668E-8) - y * 2.69515142907905952645E-15
    zz = z * z

    if j == 1 or j == 2:
        y = zz * (zz * (zz * (zz * (zz * (zz * (zz * -1.13585365213876817300E-11 + 2.08757008419747316778E-9) +
            -2.75573141792967388112E-7) + 2.48015872888517045348E-5) + -1.38888888888730564116E-3) + 4.16666666666665929218E-2) + -0.5) + 1.0
    else:
        y = z * (zz * (zz * (zz * (zz * (zz * (zz * 1.58962301576546568060E-10 + -2.50507477628578072866E-8) +
            2.75573136213857245213E-6) + -1.98412698295895385996E-4) + 8.33333333332211858878E-3) + -1.66666666666666307295E-1) + 1.0)

    if sign < 0:
        y = y * -1.0

    return y
"""

register_kernel('sin', (('x', float64()),), sin_f64, optimize=True)


sin_f64x2 = """
def sin(x: float64x2) -> float64x2:

    sign = copysign(float64x2(1.0), x)
    x = abs(x)

    mult = select(float64x2(0.0), float64x2(1.0), x > float64x2(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    #z = y - floor(y * 0.0625) * 16.0
    mm = int32x2(y - floor(y * 0.0625) * 16.0)

    # y = y + float64x2(int32x2(z) & int32x2(1))
    # j = (int32x2(z) + (int32x2(z) & int32x2(1))) & int32x2(7)

    y = y + float64x2(mm & int32x2(1))
    j = (mm + (mm & int32x2(1))) & int32x2(7)

    sign = select(sign * -1.0, sign, j > int32x2(3))
    j = select(j - int32x2(4), j, j > int32x2(3))

    z = ((x - y * 7.85398125648498535156E-1) - y * 3.77489470793079817668E-8) - y * 2.69515142907905952645E-15
    zz = z * z

    s = zz * (zz * (zz * (zz * (zz * (zz * (zz * -1.13585365213876817300E-11 + float64x2(2.08757008419747316778E-9)) +
        float64x2(-2.75573141792967388112E-7)) + float64x2(2.48015872888517045348E-5)) + float64x2(-1.38888888888730564116E-3)) +
        float64x2(4.16666666666665929218E-2)) + float64x2(-0.5)) + float64x2(1.0)

    c = z * (zz * (zz * (zz * (zz * (zz * (zz * 1.58962301576546568060E-10 + float64x2(-2.50507477628578072866E-8)) +
        float64x2(2.75573136213857245213E-6)) + float64x2(-1.98412698295895385996E-4)) + float64x2(8.33333333332211858878E-3)) +
        float64x2(-1.66666666666666307295E-1)) + float64x2(1.0))

    return select(s, c, (j == int32x2(1)) | (j == int32x2(2))) * sign * mult
"""

register_kernel('sin', (('x', float64x2()),), sin_f64x2, optimize=True)


sin_f64x3 = """
def sin(x: float64x3) -> float64x3:

    sign = copysign(float64x3(1.0), x)
    x = abs(x)

    mult = select(float64x3(0.0), float64x3(1.0), x > float64x3(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    #z = y - floor(y * 0.0625) * 16.0
    mm = int32x3(y - floor(y * 0.0625) * 16.0)

    # y = y + float64x3(int32x3(z) & int32x3(1))
    # j = (int32x3(z) + (int32x3(z) & int32x3(1))) & int32x3(7)

    y = y + float64x3(mm & int32x3(1))
    j = (mm + (mm & int32x3(1))) & int32x3(7)

    sign = select(sign * -1.0, sign, j > int32x3(3))
    j = select(j - int32x3(4), j, j > int32x3(3))

    z = ((x - y * 7.85398125648498535156E-1) - y * 3.77489470793079817668E-8) - y * 2.69515142907905952645E-15
    zz = z * z

    s = zz * (zz * (zz * (zz * (zz * (zz * (zz * -1.13585365213876817300E-11 + float64x3(2.08757008419747316778E-9)) +
        float64x3(-2.75573141792967388112E-7)) + float64x3(2.48015872888517045348E-5)) + float64x3(-1.38888888888730564116E-3)) +
        float64x3(4.16666666666665929218E-2)) + float64x3(-0.5)) + float64x3(1.0)

    c = z * (zz * (zz * (zz * (zz * (zz * (zz * 1.58962301576546568060E-10 + float64x3(-2.50507477628578072866E-8)) +
        float64x3(2.75573136213857245213E-6)) + float64x3(-1.98412698295895385996E-4)) + float64x3(8.33333333332211858878E-3)) +
        float64x3(-1.66666666666666307295E-1)) + float64x3(1.0))

    return select(s, c, (j == int32x3(1)) | (j == int32x3(2))) * sign * mult
"""

register_kernel('sin', (('x', float64x3()),), sin_f64x3, optimize=True)

sin_f64x4 = """
def sin(x: float64x4) -> float64x4:

    sign = copysign(float64x4(1.0), x)
    x = abs(x)
    mult = select(float64x4(0.0), float64x4(1.0), x > float64x4(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    #z = y - floor(y * 0.0625) * 16.0
    mm = int32x4(y - floor(y * 0.0625) * 16.0)

    # y = y + float64x4(int32x4(z) & int32x4(1))
    # j = (int32x4(z) + (int32x4(z) & int32x4(1))) & int32x4(7)

    y = y + float64x4(mm & int32x4(1))
    j = (mm + (mm & int32x4(1))) & int32x4(7)

    sign = select(sign * -1.0, sign, j > int32x4(3))
    j = select(j - int32x4(4), j, j > int32x4(3))

    z = ((x - y * 7.85398125648498535156E-1) - y * 3.77489470793079817668E-8) - y * 2.69515142907905952645E-15
    zz = z * z

    s = zz * (zz * (zz * (zz * (zz * (zz * (zz * -1.13585365213876817300E-11 + float64x4(2.08757008419747316778E-9)) +
        float64x4(-2.75573141792967388112E-7)) + float64x4(2.48015872888517045348E-5)) + float64x4(-1.38888888888730564116E-3)) +
        float64x4(4.16666666666665929218E-2)) + float64x4(-0.5)) + float64x4(1.0)

    c = z * (zz * (zz * (zz * (zz * (zz * (zz * 1.58962301576546568060E-10 + float64x4(-2.50507477628578072866E-8)) +
        float64x4(2.75573136213857245213E-6)) + float64x4(-1.98412698295895385996E-4)) + float64x4(8.33333333332211858878E-3)) +
        float64x4(-1.66666666666666307295E-1)) + float64x4(1.0))

    return select(s, c, (j == int32x4(1)) | (j == int32x4(2))) * sign * mult
"""

register_kernel('sin', (('x', float64x4()),), sin_f64x4, optimize=True)


sin_f64x8 = """
def sin(x: float64x8) -> float64x8:

    sign = copysign(float64x8(1.0), x)
    x = abs(x)
    mult = select(float64x8(0.0), float64x8(1.0), x > float64x8(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    #z = y - floor(y * 0.0625) * 16.0
    mm = int32x8(y - floor(y * 0.0625) * 16.0)

    # y = y + float64x8(int32x8(z) & int32x8(1))
    # j = (int32x8(z) + (int32x8(z) & int32x8(1))) & int32x8(7)

    y = y + float64x8(mm & int32x8(1))
    j = (mm + (mm & int32x8(1))) & int32x8(7)

    sign = select(sign * -1.0, sign, j > int32x8(3))
    j = select(j - int32x8(4), j, j > int32x8(3))

    z = ((x - y * 7.85398125648498535156E-1) - y * 3.77489470793079817668E-8) - y * 2.69515142907905952645E-15
    zz = z * z

    s = zz * (zz * (zz * (zz * (zz * (zz * (zz * -1.13585365213876817300E-11 + float64x8(2.08757008419747316778E-9)) +
        float64x8(-2.75573141792967388112E-7)) + float64x8(2.48015872888517045348E-5)) + float64x8(-1.38888888888730564116E-3)) +
        float64x8(4.16666666666665929218E-2)) + float64x8(-0.5)) + float64x8(1.0)

    c = z * (zz * (zz * (zz * (zz * (zz * (zz * 1.58962301576546568060E-10 + float64x8(-2.50507477628578072866E-8)) +
        float64x8(2.75573136213857245213E-6)) + float64x8(-1.98412698295895385996E-4)) + float64x8(8.33333333332211858878E-3)) +
        float64x8(-1.66666666666666307295E-1)) + float64x8(1.0))

    return select(s, c, (j == int32x8(1)) | (j == int32x8(2))) * sign * mult
"""

register_kernel('sin', (('x', float64x8()),), sin_f64x8, optimize=True)


# ACCURACY:
#
#                      Relative error:
# arithmetic   domain      # trials      peak         rms
#    IEEE    -8192,+8192   100,000      3.0e-7     3.0e-8

sin_f32 = """
def sin(x: float32) -> float32:

    sign = 1
    if x < float32(0.0):
        x = x * -1
        sign = -1

    if x > float32(16777215.0):
        return float32(0.0)

    y = floor(x * float32(1.27323954473516))
    j = int32(y)

    if j & 1:
        y = y + 1.0
        j = j + 1

    j = j & 7
    if j > 3:
        sign = sign * -1
        j = j - 4

    if x > float32(8192.0):
        x = x - y * float32(0.7853981633974483096)
    else:
        x = ((x - y * float32(0.78515625)) - y * float32(2.4187564849853515625e-4)) - y * float32(3.77489497744594108e-8)

    z = x * x
    if j == 1 or j == 2:
        y = ((float32(2.443315711809948E-005) * z - float32(1.388731625493765E-003)) * z + float32(4.166664568298827E-002)) * z * z - float32(0.5) * z + float32(1.0)
    else:
        y = ((float32(-1.9515295891E-4) * z + float32(8.3321608736E-3)) * z - float32(1.6666654611E-1)) * z * x + x

    if sign < 0:
        y = y * -1.0

    return y
"""

register_kernel('sin', (('x', float32()),), sin_f32, optimize=True)


sin_f32x2 = """
def sin(x: float32x2) -> float32x2:

    sign = copysign(float32x2(1.0), x)
    x = abs(x)

    mult = select(float32x2(0.0), float32x2(1.0), x > float32x2(16777215.0))

    y = floor(x * float32x2(1.27323954473516))
    j = int32x2(y)

    y = y + float32x2(j & int32x2(1))
    j = (j + (j & int32x2(1))) & int32x2(7)

    sign = select(sign * -1.0, sign, j > int32x2(3))
    j = select(j - int32x2(4), j, j > int32x2(3))

    x1 = x - y * float32x2(0.7853981633974483096)
    x2 = ((x - y * float32x2(0.78515625)) - y * float32x2(2.4187564849853515625e-4)) - y * float32x2(3.77489497744594108e-8)
    x = select(x1, x2, x > float32x2(8192.0))

    z = x * x
    s = ((float32x2(2.443315711809948E-005) * z - float32x2(1.388731625493765E-003)) * z + float32x2(4.166664568298827E-002)) * z * z - float32x2(0.5) * z + float32x2(1.0)
    c = ((float32x2(-1.9515295891E-4) * z + float32x2(8.3321608736E-3)) * z - float32x2(1.6666654611E-1)) * z * x + x
    return select(s, c, (j == int32x2(1)) | (j == int32x2(2))) * sign * mult
"""

register_kernel('sin', (('x', float32x2()),), sin_f32x2, optimize=True)


sin_f32x3 = """
def sin(x: float32x3) -> float32x3:

    sign = copysign(float32x3(1.0), x)
    x = abs(x)

    mult = select(float32x3(0.0), float32x3(1.0), x > float32x3(16777215.0))

    y = floor(x * float32x3(1.27323954473516))
    j = int32x3(y)

    y = y + float32x3(j & int32x3(1))
    j = (j + (j & int32x3(1))) & int32x3(7)

    sign = select(sign * -1.0, sign, j > int32x3(3))
    j = select(j - int32x3(4), j, j > int32x3(3))

    x1 = x - y * float32x3(0.7853981633974483096)
    x2 = ((x - y * float32x3(0.78515625)) - y * float32x3(2.4187564849853515625e-4)) - y * float32x3(3.77489497744594108e-8)
    x = select(x1, x2, x > float32x3(8192.0))

    z = x * x
    s = ((float32x3(2.443315711809948E-005) * z - float32x3(1.388731625493765E-003)) * z + float32x3(4.166664568298827E-002)) * z * z - float32x3(0.5) * z + float32x3(1.0)
    c = ((float32x3(-1.9515295891E-4) * z + float32x3(8.3321608736E-3)) * z - float32x3(1.6666654611E-1)) * z * x + x
    return select(s, c, (j == int32x3(1)) | (j == int32x3(2))) * sign * mult
"""

register_kernel('sin', (('x', float32x3()),), sin_f32x3, optimize=True)


sin_f32x4 = """
def sin(x: float32x4) -> float32x4:

    sign = copysign(float32x4(1.0), x)
    x = abs(x)

    mult = select(float32x4(0.0), float32x4(1.0), x > float32x4(16777215.0))

    y = floor(x * float32x4(1.27323954473516))
    j = int32x4(y)

    y = y + float32x4(j & int32x4(1))
    j = (j + (j & int32x4(1))) & int32x4(7)

    sign = select(sign * -1.0, sign, j > int32x4(3))
    j = select(j - int32x4(4), j, j > int32x4(3))

    x1 = x - y * float32x4(0.7853981633974483096)
    x2 = ((x - y * float32x4(0.78515625)) - y * float32x4(2.4187564849853515625e-4)) - y * float32x4(3.77489497744594108e-8)
    x = select(x1, x2, x > float32x4(8192.0))

    z = x * x
    s = ((float32x4(2.443315711809948E-005) * z - float32x4(1.388731625493765E-003)) * z + float32x4(4.166664568298827E-002)) * z * z - float32x4(0.5) * z + float32x4(1.0)
    c = ((float32x4(-1.9515295891E-4) * z + float32x4(8.3321608736E-3)) * z - float32x4(1.6666654611E-1)) * z * x + x
    return select(s, c, (j == int32x4(1)) | (j == int32x4(2))) * sign * mult
"""

register_kernel('sin', (('x', float32x4()),), sin_f32x4, optimize=True)


sin_f32x8 = """
def sin(x: float32x8) -> float32x8:

    sign = copysign(float32x8(1.0), x)
    x = abs(x)

    mult = select(float32x8(0.0), float32x8(1.0), x > float32x8(16777215.0))

    y = floor(x * float32x8(1.27323954473516))
    j = int32x8(y)

    y = y + float32x8(j & int32x8(1))
    j = (j + (j & int32x8(1))) & int32x8(7)

    sign = select(sign * -1.0, sign, j > int32x8(3))
    j = select(j - int32x8(4), j, j > int32x8(3))

    x1 = x - y * float32x8(0.7853981633974483096)
    x2 = ((x - y * float32x8(0.78515625)) - y * float32x8(2.4187564849853515625e-4)) - y * float32x8(3.77489497744594108e-8)
    x = select(x1, x2, x > float32x8(8192.0))

    z = x * x
    s = ((float32x8(2.443315711809948E-005) * z - float32x8(1.388731625493765E-003)) * z + float32x8(4.166664568298827E-002)) * z * z - float32x8(0.5) * z + float32x8(1.0)
    c = ((float32x8(-1.9515295891E-4) * z + float32x8(8.3321608736E-3)) * z - float32x8(1.6666654611E-1)) * z * x + x
    return select(s, c, (j == int32x8(1)) | (j == int32x8(2))) * sign * mult
"""

register_kernel('sin', (('x', float32x8()),), sin_f32x8, optimize=True)


sin_f32x16 = """
def sin(x: float32x16) -> float32x16:

    sign = copysign(float32x16(1.0), x)
    x = abs(x)

    mult = select(float32x16(0.0), float32x16(1.0), x > float32x16(16777215.0))

    y = floor(x * float32x16(1.27323954473516))
    j = int32x16(y)

    y = y + float32x16(j & int32x16(1))
    j = (j + (j & int32x16(1))) & int32x16(7)

    sign = select(sign * -1.0, sign, j > int32x16(3))
    j = select(j - int32x16(4), j, j > int32x16(3))
    
    x1 = x - y * float32x16(0.7853981633974483096)
    x2 = ((x - y * float32x16(0.78515625)) - y * float32x16(2.4187564849853515625e-4)) - y * float32x16(3.77489497744594108e-8)
    x = select(x1, x2, x > float32x16(8192.0))
    
    z = x * x
    s = ((float32x16(2.443315711809948E-005) * z - float32x16(1.388731625493765E-003)) * z + float32x16(4.166664568298827E-002)) * z * z - float32x16(0.5) * z + float32x16(1.0)
    c = ((float32x16(-1.9515295891E-4) * z + float32x16(8.3321608736E-3)) * z - float32x16(1.6666654611E-1)) * z * x + x
    return select(s, c, (j == int32x16(1)) | (j == int32x16(2))) * sign * mult
"""

register_kernel('sin', (('x', float32x16()),), sin_f32x16, optimize=True)
