
from .flt_arg import float32
from .dbl_arg import float64
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []

# ACCURACY:
#
#                      Relative error:
# arithmetic   domain     # trials      peak         rms
#    DEC       +- 88       50000       2.8e-17     7.0e-18
#    IEEE      +- 708      40000       2.0e-16     5.6e-17

exp_f64 = """
def exp(x: float64) -> float64:
    px = floor(1.4426950408889634073599 * x + 0.5)
    n = int32(px)
    x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
    xx = x * x
    px = x * ((1.26177193074810590878E-4 * xx + 3.02994407707441961300E-2) * xx + 9.99999999999999999910E-1)
    x = px / ((((3.00198505138664455042E-6 * xx + 2.52448340349684104192E-3) * xx + 2.27265548208155028766E-1) * xx + 2.00000000000000000009E0) - px)
    return ldexp(1.0 + 2.0 * x, n)
"""

register_kernel('exp', (('x', float64()),), exp_f64, optimize=True)


exp_f64x2 = """
def exp(x: float64x2) -> float64x2:
    px = floor(1.4426950408889634073599 * x + float64x2(0.5))
    n = int32x2(px)
    x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
    xx = x * x
    px = x * ((1.26177193074810590878E-4 * xx + float64x2(3.02994407707441961300E-2)) * xx + float64x2(9.99999999999999999910E-1))
    x = px / ((((3.00198505138664455042E-6 * xx + float64x2(2.52448340349684104192E-3)) * xx +
                float64x2(2.27265548208155028766E-1)) * xx + float64x2(2.00000000000000000009E0)) - px)
    return ldexp(float64x2(1.0) + 2.0 * x, n)
"""

register_kernel('exp', (('x', float64x2()),), exp_f64x2, optimize=True)


exp_f64x3 = """
def exp(x: float64x3) -> float64x3:
    px = floor(1.4426950408889634073599 * x + float64x3(0.5))
    n = int32x3(px)
    x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
    xx = x * x
    px = x * ((1.26177193074810590878E-4 * xx + float64x3(3.02994407707441961300E-2)) * xx + float64x3(9.99999999999999999910E-1))
    x = px / ((((3.00198505138664455042E-6 * xx + float64x3(2.52448340349684104192E-3)) * xx +
                float64x3(2.27265548208155028766E-1)) * xx + float64x3(2.00000000000000000009E0)) - px)
    return ldexp(float64x3(1.0) + 2.0 * x, n)
"""

register_kernel('exp', (('x', float64x3()),), exp_f64x3, optimize=True)


exp_f64x4 = """
def exp(x: float64x4) -> float64x4:
    px = floor(1.4426950408889634073599 * x + float64x4(0.5))
    n = int32x4(px)
    x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
    xx = x * x
    px = x * ((1.26177193074810590878E-4 * xx + float64x4(3.02994407707441961300E-2)) * xx + float64x4(9.99999999999999999910E-1))
    x = px / ((((3.00198505138664455042E-6 * xx + float64x4(2.52448340349684104192E-3)) * xx +
                float64x4(2.27265548208155028766E-1)) * xx + float64x4(2.00000000000000000009E0)) - px)
    return ldexp(float64x4(1.0) + 2.0 * x, n)
"""

register_kernel('exp', (('x', float64x4()),), exp_f64x4, optimize=True)


exp_f64x8 = """
def exp(x: float64x8) -> float64x8:
    px = floor(1.4426950408889634073599 * x + float64x8(0.5))
    n = int32x8(px)
    x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
    xx = x * x
    px = x * ((1.26177193074810590878E-4 * xx + float64x8(3.02994407707441961300E-2)) * xx + float64x8(9.99999999999999999910E-1))
    x = px / ((((3.00198505138664455042E-6 * xx + float64x8(2.52448340349684104192E-3)) * xx +
                float64x8(2.27265548208155028766E-1)) * xx + float64x8(2.00000000000000000009E0)) - px)
    return ldexp(float64x8(1.0) + 2.0 * x, n)
"""

register_kernel('exp', (('x', float64x8()),), exp_f64x8, optimize=True)


exp_f32 = """
def exp(x: float32) -> float32:
    z = floor(1.44269504088896341 * x + 0.5)
    
    x -= z * 0.693359375
    x -= z * -2.12194440e-4
    n = int32(z)
    z = x * x
    
    z = (((((1.9875691500E-4  * x + 1.3981999507E-3) * x + 8.3334519073E-3) * x + 4.1665795894E-2) * x + 1.6666665459E-1) * x + 5.0000001201E-1) * z + x + 1.0
    return ldexp(z, n)
"""

register_kernel('exp', (('x', float32()),), exp_f32, optimize=True)


exp_f32x2 = """
def exp(x: float32x2) -> float32x2:
    z = floor(1.44269504088896341 * x + float32x2(0.5))

    x -= z * 0.693359375
    x -= z * -2.12194440e-4
    n = int32x2(z)
    z = x * x

    z = (((((1.9875691500E-4 * x + float32x2(1.3981999507E-3)) * x + float32x2(8.3334519073E-3)) * x +
        float32x2(4.1665795894E-2)) * x + float32x2(1.6666665459E-1)) * x + float32x2(5.0000001201E-1)) * z + x + float32x2(1.0)
    return ldexp(z, n)
"""

register_kernel('exp', (('x', float32x2()),), exp_f32x2, optimize=True)


exp_f32x3 = """
def exp(x: float32x3) -> float32x3:
    z = floor(1.44269504088896341 * x + float32x3(0.5))

    x -= z * 0.693359375
    x -= z * -2.12194440e-4
    n = int32x3(z)
    z = x * x

    z = (((((1.9875691500E-4 * x + float32x3(1.3981999507E-3)) * x + float32x3(8.3334519073E-3)) * x +
        float32x3(4.1665795894E-2)) * x + float32x3(1.6666665459E-1)) * x + float32x3(5.0000001201E-1)) * z + x + float32x3(1.0)
    return ldexp(z, n)
"""

register_kernel('exp', (('x', float32x3()),), exp_f32x3, optimize=True)


exp_f32x4 = """
def exp(x: float32x4) -> float32x4:
    z = floor(1.44269504088896341 * x + float32x4(0.5))

    x -= z * 0.693359375
    x -= z * -2.12194440e-4
    n = int32x4(z)
    z = x * x

    z = (((((1.9875691500E-4 * x + float32x4(1.3981999507E-3)) * x + float32x4(8.3334519073E-3)) * x +
        float32x4(4.1665795894E-2)) * x + float32x4(1.6666665459E-1)) * x + float32x4(5.0000001201E-1)) * z + x + float32x4(1.0)
    return ldexp(z, n)
"""

register_kernel('exp', (('x', float32x4()),), exp_f32x4, optimize=True)


exp_f32x8 = """
def exp(x: float32x8) -> float32x8:
    z = floor(1.44269504088896341 * x + float32x8(0.5))

    x -= z * 0.693359375
    x -= z * -2.12194440e-4
    n = int32x8(z)
    z = x * x

    z = (((((1.9875691500E-4 * x + float32x8(1.3981999507E-3)) * x + float32x8(8.3334519073E-3)) * x +
        float32x8(4.1665795894E-2)) * x + float32x8(1.6666665459E-1)) * x + float32x8(5.0000001201E-1)) * z + x + float32x8(1.0)
    return ldexp(z, n)
"""

register_kernel('exp', (('x', float32x8()),), exp_f32x8, optimize=True)


exp_f32x16 = """
def exp(x: float32x16) -> float32x16:
    z = floor(1.44269504088896341 * x + float32x16(0.5))

    x -= z * 0.693359375
    x -= z * -2.12194440e-4
    n = int32x16(z)
    z = x * x

    z = (((((1.9875691500E-4 * x + float32x16(1.3981999507E-3)) * x + float32x16(8.3334519073E-3)) * x +
        float32x16(4.1665795894E-2)) * x + float32x16(1.6666665459E-1)) * x + float32x16(5.0000001201E-1)) * z + x + float32x16(1.0)
    return ldexp(z, n)
"""

register_kernel('exp', (('x', float32x16()),), exp_f32x16, optimize=True)
