from .dbl_arg import float64
from .flt_arg import float32
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []


tan_f64 = """
def tan(x: float64) -> float64:

    sign = 1.0
    if x < 0:
        x = -x
        sign = -1.0

    if x > 1.073741824e9:
        return 0.0

    y = floor(x * 1.2732395447351628)
    z = y - floor(y * 0.125) * 8.0

    j = int32(z)
    if j & 1:
        y = y + 1.0
        j = j + 1

    z = ((x - y * 7.853981554508209228515625E-1) - y * 7.94662735614792836714E-9) - y * 3.06161699786838294307E-17
    zz = z * z
    
    if zz > 1.0e-14:
        y = z + z * (zz * ((-1.30936939181383777646E4 * zz + 1.15351664838587416140E6) * zz +
        -1.79565251976484877988E7) / ((((zz + 1.36812963470692954678E4) * zz +
        -1.32089234440210967447E6) * zz + 2.50083801823357915839E7) * zz + -5.38695755929454629881E7))
    else:
        y = z

    if j & 2:
        y = -1.0 / y

    if sign < 0:
        y = -y

    return y
"""

register_kernel('tan', (('x', float64()),), tan_f64, optimize=True)


tan_f64x2 = """
def tan(x: float64x2) -> float64x2:

    sign = copysign(float64x2(1.0), x)
    x = abs(x)
    
    mult = select(float64x2(0.0), float64x2(1.0), x > float64x2(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    z = y - floor(y * 0.125) * 8.0
    
    j = int32x2(z)
    
    y = y + float64x2(j & int32x2(1))
    j = j + (j & int32x2(1))
    
    z = ((x - y * 7.853981554508209228515625E-1) - y * 7.94662735614792836714E-9) - y * 3.06161699786838294307E-17
    zz = z * z 

    val = z + z * (zz * ((-1.30936939181383777646E4 * zz + float64x2(1.15351664838587416140E6)) * zz +
        float64x2(-1.79565251976484877988E7)) / ((((zz + float64x2(1.36812963470692954678E4)) * zz +
        float64x2(-1.32089234440210967447E6)) * zz + float64x2(2.50083801823357915839E7)) * zz + float64x2(-5.38695755929454629881E7)))

    y = select(val, z, zz > float64x2(1.0e-14))
    
    y = select(float64x2(-1.0) / y, y, (j & int32x2(2)) > int32x2(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float64x2()),), tan_f64x2, optimize=True)

tan_f64x3 = """
def tan(x: float64x3) -> float64x3:

    sign = copysign(float64x3(1.0), x)
    x = abs(x)

    mult = select(float64x3(0.0), float64x3(1.0), x > float64x3(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    z = y - floor(y * 0.125) * 8.0

    j = int32x3(z)

    y = y + float64x3(j & int32x3(1))
    j = j + (j & int32x3(1))

    z = ((x - y * 7.853981554508209228515625E-1) - y * 7.94662735614792836714E-9) - y * 3.06161699786838294307E-17
    zz = z * z 

    val = z + z * (zz * ((-1.30936939181383777646E4 * zz + float64x3(1.15351664838587416140E6)) * zz +
        float64x3(-1.79565251976484877988E7)) / ((((zz + float64x3(1.36812963470692954678E4)) * zz +
        float64x3(-1.32089234440210967447E6)) * zz + float64x3(2.50083801823357915839E7)) * zz + float64x3(-5.38695755929454629881E7)))

    y = select(val, z, zz > float64x3(1.0e-14))

    y = select(float64x3(-1.0) / y, y, (j & int32x3(2)) > int32x3(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float64x3()),), tan_f64x3, optimize=True)


tan_f64x4 = """
def tan(x: float64x4) -> float64x4:

    sign = copysign(float64x4(1.0), x)
    x = abs(x)

    mult = select(float64x4(0.0), float64x4(1.0), x > float64x4(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    z = y - floor(y * 0.125) * 8.0

    j = int32x4(z)

    y = y + float64x4(j & int32x4(1))
    j = j + (j & int32x4(1))

    z = ((x - y * 7.853981554508209228515625E-1) - y * 7.94662735614792836714E-9) - y * 3.06161699786838294307E-17
    zz = z * z 

    val = z + z * (zz * ((-1.30936939181383777646E4 * zz + float64x4(1.15351664838587416140E6)) * zz +
        float64x4(-1.79565251976484877988E7)) / ((((zz + float64x4(1.36812963470692954678E4)) * zz +
        float64x4(-1.32089234440210967447E6)) * zz + float64x4(2.50083801823357915839E7)) * zz + float64x4(-5.38695755929454629881E7)))

    y = select(val, z, zz > float64x4(1.0e-14))

    y = select(float64x4(-1.0) / y, y, (j & int32x4(2)) > int32x4(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float64x4()),), tan_f64x4, optimize=True)


tan_f64x8 = """
def tan(x: float64x8) -> float64x8:

    sign = copysign(float64x8(1.0), x)
    x = abs(x)

    mult = select(float64x8(0.0), float64x8(1.0), x > float64x8(1.073741824e9))

    y = floor(x * 1.2732395447351628)
    z = y - floor(y * 0.125) * 8.0

    j = int32x8(z)

    y = y + float64x8(j & int32x8(1))
    j = j + (j & int32x8(1))

    z = ((x - y * 7.853981554508209228515625E-1) - y * 7.94662735614792836714E-9) - y * 3.06161699786838294307E-17
    zz = z * z 

    val = z + z * (zz * ((-1.30936939181383777646E4 * zz + float64x8(1.15351664838587416140E6)) * zz +
        float64x8(-1.79565251976484877988E7)) / ((((zz + float64x8(1.36812963470692954678E4)) * zz +
        float64x8(-1.32089234440210967447E6)) * zz + float64x8(2.50083801823357915839E7)) * zz + float64x8(-5.38695755929454629881E7)))

    y = select(val, z, zz > float64x8(1.0e-14))

    y = select(float64x8(-1.0) / y, y, (j & int32x8(2)) > int32x8(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float64x8()),), tan_f64x8, optimize=True)


tan_f32 = """
def tan(x: float32) -> float32:

    sign = float32(1.0)
    if x < 0:
        x = -x
        sign = float32(-1.0)

    if x > 8192.0:
        return float32(0.0)

    j = int32(1.27323954473516 * x)
    y = float32(j)
    
    if j & 1:
        y = y + 1.0
        j = j + 1
    
    z = ((x - y * 0.78515625) - y * 2.4187564849853515625e-4) - y * 3.77489497744594108e-8  
    zz = z * z

    if zz > 1.0e-4:
      y = (((((9.38540185543E-3 * zz + 3.11992232697E-3) * zz + 2.44301354525E-2) * zz +
            5.34112807005E-2) * zz + 1.33387994085E-1) * zz + 3.33331568548E-1) * zz * z + z
    else:
        y = z

    if j & 2:
        y = float32(-1.0) / y

    if sign < 0:
        y = -y

    return y
"""

register_kernel('tan', (('x', float32()),), tan_f32, optimize=True)


tan_f32x2 = """
def tan(x: float32x2) -> float32x2:

    sign = copysign(float32x2(1.0), x)
    x = abs(x)

    mult = select(float32x2(0.0), float32x2(1.0), x > float32x2(8192.0))

    j = int32x2(1.27323954473516 * x)
    y = float32x2(j)

    y = y + float32x2(j & int32x2(1))
    j = j + (j & int32x2(1))
    
    z = ((x - y * 0.78515625) - y * 2.4187564849853515625e-4) - y * 3.77489497744594108e-8
    zz = z * z 
    
    val = (((((9.38540185543E-3 * zz + float32x2(3.11992232697E-3)) * zz + float32x2(2.44301354525E-2)) * zz +
            float32x2(5.34112807005E-2)) * zz + float32x2(1.33387994085E-1)) * zz + float32x2(3.33331568548E-1)) * zz * z + z

    y = select(val, z, zz > float32x2(1.0e-4))

    y = select(float32x2(-1.0) / y, y, (j & int32x2(2)) > int32x2(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float32x2()),), tan_f32x2, optimize=True)


tan_f32x3 = """
def tan(x: float32x3) -> float32x3:

    sign = copysign(float32x3(1.0), x)
    x = abs(x)

    mult = select(float32x3(0.0), float32x3(1.0), x > float32x3(8192.0))

    j = int32x3(1.27323954473516 * x)
    y = float32x3(j)

    y = y + float32x3(j & int32x3(1))
    j = j + (j & int32x3(1))

    z = ((x - y * 0.78515625) - y * 2.4187564849853515625e-4) - y * 3.77489497744594108e-8
    zz = z * z 

    val = (((((9.38540185543E-3 * zz + float32x3(3.11992232697E-3)) * zz + float32x3(2.44301354525E-2)) * zz +
            float32x3(5.34112807005E-2)) * zz + float32x3(1.33387994085E-1)) * zz + float32x3(3.33331568548E-1)) * zz * z + z

    y = select(val, z, zz > float32x3(1.0e-4))

    y = select(float32x3(-1.0) / y, y, (j & int32x3(2)) > int32x3(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float32x3()),), tan_f32x3, optimize=True)


tan_f32x4 = """
def tan(x: float32x4) -> float32x4:

    sign = copysign(float32x4(1.0), x)
    x = abs(x)

    mult = select(float32x4(0.0), float32x4(1.0), x > float32x4(8192.0))

    j = int32x4(1.27323954473516 * x)
    y = float32x4(j)

    y = y + float32x4(j & int32x4(1))
    j = j + (j & int32x4(1))

    z = ((x - y * 0.78515625) - y * 2.4187564849853515625e-4) - y * 3.77489497744594108e-8
    zz = z * z 

    val = (((((9.38540185543E-3 * zz + float32x4(3.11992232697E-3)) * zz + float32x4(2.44301354525E-2)) * zz +
            float32x4(5.34112807005E-2)) * zz + float32x4(1.33387994085E-1)) * zz + float32x4(3.33331568548E-1)) * zz * z + z

    y = select(val, z, zz > float32x4(1.0e-4))

    y = select(float32x4(-1.0) / y, y, (j & int32x4(2)) > int32x4(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float32x4()),), tan_f32x4, optimize=True)


tan_f32x8 = """
def tan(x: float32x8) -> float32x8:

    sign = copysign(float32x8(1.0), x)
    x = abs(x)

    mult = select(float32x8(0.0), float32x8(1.0), x > float32x8(8192.0))

    j = int32x8(1.27323954473516 * x)
    y = float32x8(j)

    y = y + float32x8(j & int32x8(1))
    j = j + (j & int32x8(1))

    z = ((x - y * 0.78515625) - y * 2.4187564849853515625e-4) - y * 3.77489497744594108e-8
    zz = z * z 

    val = (((((9.38540185543E-3 * zz + float32x8(3.11992232697E-3)) * zz + float32x8(2.44301354525E-2)) * zz +
            float32x8(5.34112807005E-2)) * zz + float32x8(1.33387994085E-1)) * zz + float32x8(3.33331568548E-1)) * zz * z + z

    y = select(val, z, zz > float32x8(1.0e-4))

    y = select(float32x8(-1.0) / y, y, (j & int32x8(2)) > int32x8(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float32x8()),), tan_f32x8, optimize=True)


tan_f32x16 = """
def tan(x: float32x16) -> float32x16:

    sign = copysign(float32x16(1.0), x)
    x = abs(x)

    mult = select(float32x16(0.0), float32x16(1.0), x > float32x16(8192.0))

    j = int32x16(1.27323954473516 * x)
    y = float32x16(j)

    y = y + float32x16(j & int32x16(1))
    j = j + (j & int32x16(1))

    z = ((x - y * 0.78515625) - y * 2.4187564849853515625e-4) - y * 3.77489497744594108e-8
    zz = z * z 

    val = (((((9.38540185543E-3 * zz + float32x16(3.11992232697E-3)) * zz + float32x16(2.44301354525E-2)) * zz +
            float32x16(5.34112807005E-2)) * zz + float32x16(1.33387994085E-1)) * zz + float32x16(3.33331568548E-1)) * zz * z + z

    y = select(val, z, zz > float32x16(1.0e-4))

    y = select(float32x16(-1.0) / y, y, (j & int32x16(2)) > int32x16(0))
    return y * sign * mult
"""

register_kernel('tan', (('x', float32x16()),), tan_f32x16, optimize=True)
