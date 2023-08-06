
from .dbl_arg import float64
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32, float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []

# ACCURACY:
#
#                      Relative error:
# arithmetic   domain     # trials      peak         rms
#    IEEE      0.5, 2.0    150000      1.44e-16    5.06e-17
#    IEEE      +-MAXNUM    30000       1.20e-16    4.78e-17
#    DEC       0, 10       170000      1.8e-17     6.3e-18
#

log_f64 = """
def log(x: float64) -> float64:
    exponent = (typecast(abs(x), int64) >> 52) - 1022
    x = typecast(typecast(x, int64) & int64(-9218868437227405313) | int64(4602678819172646912), float64)
    if x < 7.07106781186547524401E-1:
        exponent -= 1
        x = 2.0 * x - 1.0
    else:
        x = x - 1.0

    z = x * x
    y = x * (z * (((((1.01875663804580931796E-4 * x + 4.97494994976747001425E-1) * x + 4.70579119878881725854E0) * x +
                    1.44989225341610930846E1) * x + 1.79368678507819816313E1) * x + 7.70838733755885391666E0) / (((((x + 1.12873587189167450590E1) * x +
                    4.52279145837532221105E1) * x + 8.29875266912776603211E1) * x + 7.11544750618563894466E1) * x + 2.31251620126765340583E1))

    return (x + ((y - float64(exponent) * 2.121944400546905827679e-4) - 0.5 * z)) + float64(exponent) * 0.693359375
"""

register_kernel('log', (('x', float64()),), log_f64, optimize=True)


log_f64x2 = """
def log(x: float64x2) -> float64x2:
    exponent = float64x2(int32x2(rshift(typecast(abs(x), int64x2), 52)) - int32x2(1022))
    x = typecast(typecast(x, int64x2) & int64x2(-9218868437227405313) | int64x2(4602678819172646912), float64x2)
    mask = x < float64x2(7.07106781186547524401E-1)
    x = select(2.0 * x - float64x2(1.0), x - float64x2(1.0), mask)
    exponent = select(exponent - float64x2(1), exponent, mask)

    z = x * x
    y = x * (z * (((((1.01875663804580931796E-4 * x + float64x2(4.97494994976747001425E-1)) * x + float64x2(4.70579119878881725854E0)) * x +
                    float64x2(1.44989225341610930846E1)) * x + float64x2(1.79368678507819816313E1)) * x +
                    float64x2(7.70838733755885391666E0)) / (((((x + float64x2(1.12873587189167450590E1)) * x +
                    float64x2(4.52279145837532221105E1)) * x + float64x2(8.29875266912776603211E1)) * x +
                    float64x2(7.11544750618563894466E1)) * x + float64x2(2.31251620126765340583E1)))

    return (x + ((y - exponent * 2.121944400546905827679e-4) - 0.5 * z)) + exponent * 0.693359375
"""

register_kernel('log', (('x', float64x2()),), log_f64x2, optimize=True)


log_f64x3 = """
def log(x: float64x3) -> float64x3:
    exponent = float64x3(int32x3(rshift(typecast(abs(x), int64x3), 52)) - int32x3(1022))
    x = typecast(typecast(x, int64x3) & int64x3(-9218868437227405313) | int64x3(4602678819172646912), float64x3)
    mask = x < float64x3(7.07106781186547524401E-1)
    x = select(2.0 * x - float64x3(1.0), x - float64x3(1.0), mask)
    exponent = select(exponent - float64x3(1), exponent, mask)

    z = x * x
    y = x * (z * (((((1.01875663804580931796E-4 * x + float64x3(4.97494994976747001425E-1)) * x + float64x3(4.70579119878881725854E0)) * x +
                    float64x3(1.44989225341610930846E1)) * x + float64x3(1.79368678507819816313E1)) * x +
                    float64x3(7.70838733755885391666E0)) / (((((x + float64x3(1.12873587189167450590E1)) * x +
                    float64x3(4.52279145837532221105E1)) * x + float64x3(8.29875266912776603211E1)) * x +
                    float64x3(7.11544750618563894466E1)) * x + float64x3(2.31251620126765340583E1)))

    return (x + ((y - exponent * 2.121944400546905827679e-4) - 0.5 * z)) + exponent * 0.693359375
"""

register_kernel('log', (('x', float64x3()),), log_f64x3, optimize=True)


log_f64x4 = """
def log(x: float64x4) -> float64x4:
    exponent = float64x4(int32x4(rshift(typecast(abs(x), int64x4), 52)) - int32x4(1022))
    x = typecast(typecast(x, int64x4) & int64x4(-9218868437227405313) | int64x4(4602678819172646912), float64x4)
    mask = x < float64x4(7.07106781186547524401E-1)
    x = select(2.0 * x - float64x4(1.0), x - float64x4(1.0), mask)
    exponent = select(exponent - float64x4(1), exponent, mask)

    z = x * x
    y = x * (z * (((((1.01875663804580931796E-4 * x + float64x4(4.97494994976747001425E-1)) * x + float64x4(4.70579119878881725854E0)) * x +
                    float64x4(1.44989225341610930846E1)) * x + float64x4(1.79368678507819816313E1)) * x +
                    float64x4(7.70838733755885391666E0)) / (((((x + float64x4(1.12873587189167450590E1)) * x +
                    float64x4(4.52279145837532221105E1)) * x + float64x4(8.29875266912776603211E1)) * x +
                    float64x4(7.11544750618563894466E1)) * x + float64x4(2.31251620126765340583E1)))

    return (x + ((y - exponent * 2.121944400546905827679e-4) - 0.5 * z)) + exponent * 0.693359375
"""

register_kernel('log', (('x', float64x4()),), log_f64x4, optimize=True)


log_f64x8 = """
def log(x: float64x8) -> float64x8:
    exponent = float64x8(int32x8(rshift(typecast(abs(x), int64x8), 52)) - int32x8(1022))
    x = typecast(typecast(x, int64x8) & int64x8(-9218868437227405313) | int64x8(4602678819172646912), float64x8)
    mask = x < float64x8(7.07106781186547524401E-1)
    x = select(2.0 * x - float64x8(1.0), x - float64x8(1.0), mask)
    exponent = select(exponent - float64x8(1), exponent, mask)

    z = x * x
    y = x * (z * (((((1.01875663804580931796E-4 * x + float64x8(4.97494994976747001425E-1)) * x + float64x8(4.70579119878881725854E0)) * x +
                    float64x8(1.44989225341610930846E1)) * x + float64x8(1.79368678507819816313E1)) * x +
                    float64x8(7.70838733755885391666E0)) / (((((x + float64x8(1.12873587189167450590E1)) * x +
                    float64x8(4.52279145837532221105E1)) * x + float64x8(8.29875266912776603211E1)) * x +
                    float64x8(7.11544750618563894466E1)) * x + float64x8(2.31251620126765340583E1)))
    return (x + ((y - exponent * 2.121944400546905827679e-4) - 0.5 * z)) + exponent * 0.693359375
"""

register_kernel('log', (('x', float64x8()),), log_f64x8, optimize=True)


log_f32 = """
def log(x: float32) -> float32:
    exponent = float32((typecast(abs(x), int32) >> 23) - 126)
    x = typecast(typecast(x, int32) & int32(-2139095041) | int32(1056964608), float32)
    
    if x < 0.707106781186547524:
        exponent -= 1
        x = x + x - 1.0
    else:
        x = x - 1.0

    z = x * x
    
    y = (((((((( 7.0376836292E-2 * x - 1.1514610310E-1) * x + 1.1676998740E-1) * x - 1.2420140846E-1) * x +
            1.4249322787E-1) * x - 1.6668057665E-1) * x + 2.0000714765E-1) * x - 2.4999993993E-1) * x + 3.3333331174E-1) * x * z

    y += -2.12194440e-4 * exponent
    y +=  -0.5 * z
    z = x + y
    z += 0.693359375 * exponent
    return z
"""

register_kernel('log', (('x', float32()),), log_f32, optimize=True)


log_f32x2 = """
def log(x: float32x2) -> float32x2:    
    exponent = float32x2(int32x2(rshift(typecast(abs(x), int32x2), 23)) - int32x2(126))
    x = typecast(typecast(x, int32x2) & int32x2(-2139095041) | int32x2(1056964608), float32x2)

    mask = x < float32x2(0.707106781186547524)
    exponent = select(exponent - float32x2(1), exponent, mask)
    x = select(x + x - float32x2(1.0), x - float32x2(1.0), mask)
    
    z = x * x

    y = (((((((( 7.0376836292E-2 * x - float32x2(1.1514610310E-1)) * x + float32x2(1.1676998740E-1)) * x - float32x2(1.2420140846E-1)) * x +
            float32x2(1.4249322787E-1)) * x - float32x2(1.6668057665E-1)) * x + float32x2(2.0000714765E-1)) * x - float32x2(2.4999993993E-1)) * x +
            float32x2(3.3333331174E-1)) * x * z

    y += -2.12194440e-4 * exponent
    y +=  -0.5 * z
    z = x + y
    z += 0.693359375 * exponent
    return z
"""

register_kernel('log', (('x', float32x2()),), log_f32x2, optimize=True)


log_f32x3 = """
def log(x: float32x3) -> float32x3:    
    exponent = float32x3(int32x3(rshift(typecast(abs(x), int32x3), 23)) - int32x3(126))
    x = typecast(typecast(x, int32x3) & int32x3(-2139095041) | int32x3(1056964608), float32x3)

    mask = x < float32x3(0.707106781186547524)
    exponent = select(exponent - float32x3(1), exponent, mask)
    x = select(x + x - float32x3(1.0), x - float32x3(1.0), mask)

    z = x * x

    y = (((((((( 7.0376836292E-2 * x - float32x3(1.1514610310E-1)) * x + float32x3(1.1676998740E-1)) * x - float32x3(1.2420140846E-1)) * x +
            float32x3(1.4249322787E-1)) * x - float32x3(1.6668057665E-1)) * x + float32x3(2.0000714765E-1)) * x - float32x3(2.4999993993E-1)) * x +
            float32x3(3.3333331174E-1)) * x * z

    y += -2.12194440e-4 * exponent
    y +=  -0.5 * z
    z = x + y
    z += 0.693359375 * exponent
    return z
"""

register_kernel('log', (('x', float32x3()),), log_f32x3, optimize=True)


log_f32x4 = """
def log(x: float32x4) -> float32x4:    
    exponent = float32x4(int32x4(rshift(typecast(abs(x), int32x4), 23)) - int32x4(126))
    x = typecast(typecast(x, int32x4) & int32x4(-2139095041) | int32x4(1056964608), float32x4)

    mask = x < float32x4(0.707106781186547524)
    exponent = select(exponent - float32x4(1), exponent, mask)
    x = select(x + x - float32x4(1.0), x - float32x4(1.0), mask)

    z = x * x

    y = ((((((((7.0376836292E-2 * x - float32x4(1.1514610310E-1)) * x + float32x4(1.1676998740E-1)) * x - float32x4(1.2420140846E-1)) * x +
            float32x4(1.4249322787E-1)) * x - float32x4(1.6668057665E-1)) * x + float32x4(2.0000714765E-1)) * x - float32x4(2.4999993993E-1)) * x +
            float32x4(3.3333331174E-1)) * x * z

    y += -2.12194440e-4 * exponent
    y +=  -0.5 * z
    z = x + y
    z += 0.693359375 * exponent
    return z
"""

register_kernel('log', (('x', float32x4()),), log_f32x4, optimize=True)


log_f32x8 = """
def log(x: float32x8) -> float32x8:    
    exponent = float32x8(int32x8(rshift(typecast(abs(x), int32x8), 23)) - int32x8(126))
    x = typecast(typecast(x, int32x8) & int32x8(-2139095041) | int32x8(1056964608), float32x8)

    mask = x < float32x8(0.707106781186547524)
    exponent = select(exponent - float32x8(1), exponent, mask)
    x = select(x + x - float32x8(1.0), x - float32x8(1.0), mask)

    z = x * x

    y = ((((((((7.0376836292E-2 * x - float32x8(1.1514610310E-1)) * x + float32x8(1.1676998740E-1)) * x - float32x8(1.2420140846E-1)) * x +
            float32x8(1.4249322787E-1)) * x - float32x8(1.6668057665E-1)) * x + float32x8(2.0000714765E-1)) * x - float32x8(2.4999993993E-1)) * x +
            float32x8(3.3333331174E-1)) * x * z

    y += -2.12194440e-4 * exponent
    y +=  -0.5 * z
    z = x + y
    z += 0.693359375 * exponent
    return z
"""

register_kernel('log', (('x', float32x8()),), log_f32x8, optimize=True)


log_f32x16 = """
def log(x: float32x16) -> float32x16:    
    exponent = float32x16(int32x16(rshift(typecast(abs(x), int32x16), 23)) - int32x16(126))
    x = typecast(typecast(x, int32x16) & int32x16(-2139095041) | int32x16(1056964608), float32x16)

    mask = x < float32x16(0.707106781186547524)
    exponent = select(exponent - float32x16(1), exponent, mask)
    x = select(x + x - float32x16(1.0), x - float32x16(1.0), mask)

    z = x * x

    y = ((((((((7.0376836292E-2 * x - float32x16(1.1514610310E-1)) * x + float32x16(1.1676998740E-1)) * x - float32x16(1.2420140846E-1)) * x +
            float32x16(1.4249322787E-1)) * x - float32x16(1.6668057665E-1)) * x + float32x16(2.0000714765E-1)) * x - float32x16(2.4999993993E-1)) * x +
            float32x16(3.3333331174E-1)) * x * z

    y += -2.12194440e-4 * exponent
    y +=  -0.5 * z
    z = x + y
    z += 0.693359375 * exponent
    return z
"""

register_kernel('log', (('x', float32x16()),), log_f32x16, optimize=True)
