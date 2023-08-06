from .dbl_arg import float64
from .flt_arg import float32
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []


pow_f64 = """
def pow(x: float64, y: float64) -> float64:

    def pow_log(x: float64) -> float64:
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

    def pow_exp(x: float64) -> float64:
        px = floor(1.4426950408889634073599 * x + 0.5)
        n = int32(px)
        x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
        xx = x * x
        px = x * ((1.26177193074810590878E-4 * xx + 3.02994407707441961300E-2) * xx + 9.99999999999999999910E-1)
        x = px / ((((3.00198505138664455042E-6 * xx + 2.52448340349684104192E-3) * xx + 2.27265548208155028766E-1) * xx + 2.00000000000000000009E0) - px)
        return ldexp(1.0 + 2.0 * x, n)
    
    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float64()), ('y', float64())), pow_f64, optimize=True)

pow_f64x2 = """
def pow(x: float64x2, y: float64x2) -> float64x2:

    def pow_log(x: float64x2) -> float64x2:
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

    def pow_exp(x: float64x2) -> float64x2:
        px = floor(1.4426950408889634073599 * x + float64x2(0.5))
        n = int32x2(px)
        x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
        xx = x * x
        px = x * ((1.26177193074810590878E-4 * xx + float64x2(3.02994407707441961300E-2)) * xx + float64x2(9.99999999999999999910E-1))
        x = px / ((((3.00198505138664455042E-6 * xx + float64x2(2.52448340349684104192E-3)) * xx +
                    float64x2(2.27265548208155028766E-1)) * xx + float64x2(2.00000000000000000009E0)) - px)
        return ldexp(float64x2(1.0) + 2.0 * x, n)

    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float64x2()), ('y', float64x2())), pow_f64x2, optimize=True)


pow_f64x3 = """
def pow(x: float64x3, y: float64x3) -> float64x3:

    def pow_log(x: float64x3) -> float64x3:
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

    def pow_exp(x: float64x3) -> float64x3:
        px = floor(1.4426950408889634073599 * x + float64x3(0.5))
        n = int32x3(px)
        x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
        xx = x * x
        px = x * ((1.26177193074810590878E-4 * xx + float64x3(3.02994407707441961300E-2)) * xx + float64x3(9.99999999999999999910E-1))
        x = px / ((((3.00198505138664455042E-6 * xx + float64x3(2.52448340349684104192E-3)) * xx +
                    float64x3(2.27265548208155028766E-1)) * xx + float64x3(2.00000000000000000009E0)) - px)
        return ldexp(float64x3(1.0) + 2.0 * x, n)

    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float64x3()), ('y', float64x3())), pow_f64x3, optimize=True)


pow_f64x4 = """
def pow(x: float64x4, y: float64x4) -> float64x4:

    def pow_log(x: float64x4) -> float64x4:
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

    def pow_exp(x: float64x4) -> float64x4:
        px = floor(1.4426950408889634073599 * x + float64x4(0.5))
        n = int32x4(px)
        x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
        xx = x * x
        px = x * ((1.26177193074810590878E-4 * xx + float64x4(3.02994407707441961300E-2)) * xx + float64x4(9.99999999999999999910E-1))
        x = px / ((((3.00198505138664455042E-6 * xx + float64x4(2.52448340349684104192E-3)) * xx +
                    float64x4(2.27265548208155028766E-1)) * xx + float64x4(2.00000000000000000009E0)) - px)
        return ldexp(float64x4(1.0) + 2.0 * x, n)

    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float64x4()), ('y', float64x4())), pow_f64x4, optimize=True)


pow_f64x8 = """
def pow(x: float64x8, y: float64x8) -> float64x8:

    def pow_log(x: float64x8) -> float64x8:
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

    def pow_exp(x: float64x8) -> float64x8:
        px = floor(1.4426950408889634073599 * x + float64x8(0.5))
        n = int32x8(px)
        x = ((x - (px * 6.93145751953125E-1)) - (px * 1.42860682030941723212E-6))
        xx = x * x
        px = x * ((1.26177193074810590878E-4 * xx + float64x8(3.02994407707441961300E-2)) * xx + float64x8(9.99999999999999999910E-1))
        x = px / ((((3.00198505138664455042E-6 * xx + float64x8(2.52448340349684104192E-3)) * xx +
                    float64x8(2.27265548208155028766E-1)) * xx + float64x8(2.00000000000000000009E0)) - px)
        return ldexp(float64x8(1.0) + 2.0 * x, n)

    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float64x8()), ('y', float64x8())), pow_f64x8, optimize=True)


pow_f32 = """
def pow(x: float32, y: float32) -> float32:

    def pow_log(x: float32) -> float32:
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

    def pow_exp(x: float32) -> float32:
        z = floor(1.44269504088896341 * x + 0.5)
        
        x -= z * 0.693359375
        x -= z * -2.12194440e-4
        n = int32(z)
        z = x * x
        
        z = (((((1.9875691500E-4  * x + 1.3981999507E-3) * x + 8.3334519073E-3) * x + 4.1665795894E-2) * x + 1.6666665459E-1) * x + 5.0000001201E-1) * z + x + 1.0
        return ldexp(z, n)

    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float32()), ('y', float32())), pow_f32, optimize=True)

pow_f32x2 = """
def pow(x: float32x2, y: float32x2) -> float32x2:

    def pow_log(x: float32x2) -> float32x2:    
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

    def pow_exp(x: float32x2) -> float32x2:
        z = floor(1.44269504088896341 * x + float32x2(0.5))
    
        x -= z * 0.693359375
        x -= z * -2.12194440e-4
        n = int32x2(z)
        z = x * x
    
        z = (((((1.9875691500E-4 * x + float32x2(1.3981999507E-3)) * x + float32x2(8.3334519073E-3)) * x +
            float32x2(4.1665795894E-2)) * x + float32x2(1.6666665459E-1)) * x + float32x2(5.0000001201E-1)) * z + x + float32x2(1.0)
        return ldexp(z, n)
    
    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float32x2()), ('y', float32x2())), pow_f32x2, optimize=True)


pow_f32x3 = """
def pow(x: float32x3, y: float32x3) -> float32x3:

    def pow_log(x: float32x3) -> float32x3:    
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

    def pow_exp(x: float32x3) -> float32x3:
        z = floor(1.44269504088896341 * x + float32x3(0.5))
    
        x -= z * 0.693359375
        x -= z * -2.12194440e-4
        n = int32x3(z)
        z = x * x
    
        z = (((((1.9875691500E-4 * x + float32x3(1.3981999507E-3)) * x + float32x3(8.3334519073E-3)) * x +
            float32x3(4.1665795894E-2)) * x + float32x3(1.6666665459E-1)) * x + float32x3(5.0000001201E-1)) * z + x + float32x3(1.0)
        return ldexp(z, n)
        
    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float32x3()), ('y', float32x3())), pow_f32x3, optimize=True)


pow_f32x4 = """
def pow(x: float32x4, y: float32x4) -> float32x4:

    def pow_log(x: float32x4) -> float32x4:    
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

    def pow_exp(x: float32x4) -> float32x4:
        z = floor(1.44269504088896341 * x + float32x4(0.5))
    
        x -= z * 0.693359375
        x -= z * -2.12194440e-4
        n = int32x4(z)
        z = x * x
    
        z = (((((1.9875691500E-4 * x + float32x4(1.3981999507E-3)) * x + float32x4(8.3334519073E-3)) * x +
            float32x4(4.1665795894E-2)) * x + float32x4(1.6666665459E-1)) * x + float32x4(5.0000001201E-1)) * z + x + float32x4(1.0)
        return ldexp(z, n)
    
    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float32x4()), ('y', float32x4())), pow_f32x4, optimize=True)


pow_f32x8 = """
def pow(x: float32x8, y: float32x8) -> float32x8:

    def pow_log(x: float32x8) -> float32x8:    
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
    
    def pow_exp(x: float32x8) -> float32x8:
        z = floor(1.44269504088896341 * x + float32x8(0.5))
    
        x -= z * 0.693359375
        x -= z * -2.12194440e-4
        n = int32x8(z)
        z = x * x
    
        z = (((((1.9875691500E-4 * x + float32x8(1.3981999507E-3)) * x + float32x8(8.3334519073E-3)) * x +
            float32x8(4.1665795894E-2)) * x + float32x8(1.6666665459E-1)) * x + float32x8(5.0000001201E-1)) * z + x + float32x8(1.0)
        return ldexp(z, n)
        
    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float32x8()), ('y', float32x8())), pow_f32x8, optimize=True)


pow_f32x16 = """
def pow(x: float32x16, y: float32x16) -> float32x16:

    def pow_log(x: float32x16) -> float32x16:    
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

    def pow_exp(x: float32x16) -> float32x16:
        z = floor(1.44269504088896341 * x + float32x16(0.5))
    
        x -= z * 0.693359375
        x -= z * -2.12194440e-4
        n = int32x16(z)
        z = x * x
    
        z = (((((1.9875691500E-4 * x + float32x16(1.3981999507E-3)) * x + float32x16(8.3334519073E-3)) * x +
            float32x16(4.1665795894E-2)) * x + float32x16(1.6666665459E-1)) * x + float32x16(5.0000001201E-1)) * z + x + float32x16(1.0)
        return ldexp(z, n)   

    return pow_exp(pow_log(x) * y)
"""

register_kernel('pow', (('x', float32x16()), ('y', float32x16())), pow_f32x16, optimize=True)