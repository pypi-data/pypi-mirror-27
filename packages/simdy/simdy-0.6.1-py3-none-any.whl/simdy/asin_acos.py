from .dbl_arg import float64
from .flt_arg import float32
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel


__all__ = []


asin_f64 = """
def asin(x: float64) -> float64:
    
    if x > 0:
        sign = 1.0
        a = x
    else:
        sign = -1.0
        a = -x
        
    if a > 0.625:
        zz = 1.0 - a 
        p = zz * ((((2.967721961301243206100E-3 * zz + -5.634242780008963776856E-1) * zz + 6.968710824104713396794E0) * zz + -2.556901049652824852289E1) * zz +
            2.853665548261061424989E1) / ((((zz + -2.194779531642920639778E1) * zz + 1.470656354026814941758E2) * zz + -3.838770957603691357202E2) * zz + 3.424398657913078477438E2)
        zz = sqrt(zz + zz)
        z = ((7.85398163397448309616E-1 - zz) - (zz * p - 6.123233995736765886130E-17)) + 7.85398163397448309616E-1
    else:
        if a < 1.0e-8:
            return x
        zz = a * a
        z = zz * (((((4.253011369004428248960E-3 * zz + -6.019598008014123785661E-1) * zz + 5.444622390564711410273E0) * zz +
                    -1.626247967210700244449E1) * zz + 1.956261983317594739197E1) * zz + -8.198089802484824371615E0) / (((((zz + -1.474091372988853791896E1) * zz +
                    7.049610280856842141659E1) * zz + -1.471791292232726029859E2) * zz + 1.395105614657485689735E2) * zz + -4.918853881490881290097E1)
        z = a * z + a

    if sign < 0:
        z = -z
        
    return z
"""

register_kernel('asin', (('x', float64()),), asin_f64, optimize=True)


acos_f64 = """
def acos(x: float64) -> float64:

    def _asin(x: float64) -> float64:
        
        if x > 0:
            sign = 1.0
            a = x
        else:
            sign = -1.0
            a = -x
            
        if a > 0.625:
            zz = 1.0 - a 
            p = zz * ((((2.967721961301243206100E-3 * zz + -5.634242780008963776856E-1) * zz + 6.968710824104713396794E0) * zz + -2.556901049652824852289E1) * zz +
                2.853665548261061424989E1) / ((((zz + -2.194779531642920639778E1) * zz + 1.470656354026814941758E2) * zz + -3.838770957603691357202E2) * zz + 3.424398657913078477438E2)
            zz = sqrt(zz + zz)
            z = ((7.85398163397448309616E-1 - zz) - (zz * p - 6.123233995736765886130E-17)) + 7.85398163397448309616E-1
        else:
            if a < 1.0e-8:
                return x
            zz = a * a
            z = zz * (((((4.253011369004428248960E-3 * zz + -6.019598008014123785661E-1) * zz + 5.444622390564711410273E0) * zz +
                        -1.626247967210700244449E1) * zz + 1.956261983317594739197E1) * zz + -8.198089802484824371615E0) / (((((zz + -1.474091372988853791896E1) * zz +
                        7.049610280856842141659E1) * zz + -1.471791292232726029859E2) * zz + 1.395105614657485689735E2) * zz + -4.918853881490881290097E1)
            z = a * z + a
    
        if sign < 0:
            z = -z
            
        return z

    arg = x
    if x > 0.5:
        arg = sqrt(0.5 - 0.5 * x)
    
    val = _asin(arg)
    
    if x > 0.5:
        return val * 2.0

    z = 7.85398163397448309616E-1 - val
    return (z + 6.123233995736765886130E-17) + 7.85398163397448309616E-1
"""

register_kernel('acos', (('x', float64()),), acos_f64, optimize=True)


asin_f64x2 = """
def asin(x: float64x2) -> float64x2:

    sign = copysign(float64x2(1.0), x)
    a = x * sign
    
    zz1 = float64x2(1.0) - a 
    p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x2(-5.634242780008963776856E-1)) * zz1 + float64x2(6.968710824104713396794E0)) * zz1 + float64x2(-2.556901049652824852289E1)) * zz1 +
            float64x2(2.853665548261061424989E1)) / ((((zz1 + float64x2(-2.194779531642920639778E1)) * zz1 + float64x2(1.470656354026814941758E2)) * zz1 + float64x2(-3.838770957603691357202E2)) * zz1 + float64x2(3.424398657913078477438E2))
    zz1 = sqrt(zz1 + zz1)
    z1 = ((float64x2(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x2(6.123233995736765886130E-17))) + float64x2(7.85398163397448309616E-1)
    
    zz2 = a * a
    z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x2(-6.019598008014123785661E-1)) * zz2 + float64x2(5.444622390564711410273E0)) * zz2 +
                    float64x2(-1.626247967210700244449E1)) * zz2 + float64x2(1.956261983317594739197E1)) * zz2 + float64x2(-8.198089802484824371615E0)) / (((((zz2 + float64x2(-1.474091372988853791896E1)) * zz2 +
                    float64x2(7.049610280856842141659E1)) * zz2 + float64x2(-1.471791292232726029859E2)) * zz2 + float64x2(1.395105614657485689735E2)) * zz2 + float64x2(-4.918853881490881290097E1))
    z2 = a * z2 + a
    
    val = select(z1, z2, a > float64x2(0.625))
    val = select(x, val, a < float64x2(1.0e-8))
    return val * sign
"""

register_kernel('asin', (('x', float64x2()),), asin_f64x2, optimize=True)


acos_f64x2 = """
def acos(x: float64x2) -> float64x2:

    def _asin(x: float64x2) -> float64x2:
    
        sign = copysign(float64x2(1.0), x)
        a = x * sign
        
        zz1 = float64x2(1.0) - a 
        p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x2(-5.634242780008963776856E-1)) * zz1 + float64x2(6.968710824104713396794E0)) * zz1 + float64x2(-2.556901049652824852289E1)) * zz1 +
                float64x2(2.853665548261061424989E1)) / ((((zz1 + float64x2(-2.194779531642920639778E1)) * zz1 + float64x2(1.470656354026814941758E2)) * zz1 + float64x2(-3.838770957603691357202E2)) * zz1 + float64x2(3.424398657913078477438E2))
        zz1 = sqrt(zz1 + zz1)
        z1 = ((float64x2(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x2(6.123233995736765886130E-17))) + float64x2(7.85398163397448309616E-1)
        
        zz2 = a * a
        z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x2(-6.019598008014123785661E-1)) * zz2 + float64x2(5.444622390564711410273E0)) * zz2 +
                        float64x2(-1.626247967210700244449E1)) * zz2 + float64x2(1.956261983317594739197E1)) * zz2 + float64x2(-8.198089802484824371615E0)) / (((((zz2 + float64x2(-1.474091372988853791896E1)) * zz2 +
                        float64x2(7.049610280856842141659E1)) * zz2 + float64x2(-1.471791292232726029859E2)) * zz2 + float64x2(1.395105614657485689735E2)) * zz2 + float64x2(-4.918853881490881290097E1))
        z2 = a * z2 + a
        
        val = select(z1, z2, a > float64x2(0.625))
        val = select(x, val, a < float64x2(1.0e-8))
        return val * sign
    
    mask = x > float64x2(0.5)
    arg = select(sqrt(float64x2(0.5) - 0.5 * x), x, mask)
    val = _asin(arg)
    return select(val * 2.0, (float64x2(7.85398163397448309616E-1) - val + float64x2(6.123233995736765886130E-17)) + float64x2(7.85398163397448309616E-1), mask)
"""

register_kernel('acos', (('x', float64x2()),), acos_f64x2, optimize=True)


asin_f64x3 = """
def asin(x: float64x3) -> float64x3:

    sign = copysign(float64x3(1.0), x)
    a = x * sign

    zz1 = float64x3(1.0) - a 
    p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x3(-5.634242780008963776856E-1)) * zz1 + float64x3(6.968710824104713396794E0)) * zz1 + float64x3(-2.556901049652824852289E1)) * zz1 +
            float64x3(2.853665548261061424989E1)) / ((((zz1 + float64x3(-2.194779531642920639778E1)) * zz1 + float64x3(1.470656354026814941758E2)) * zz1 + float64x3(-3.838770957603691357202E2)) * zz1 + float64x3(3.424398657913078477438E2))
    zz1 = sqrt(zz1 + zz1)
    z1 = ((float64x3(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x3(6.123233995736765886130E-17))) + float64x3(7.85398163397448309616E-1)

    zz2 = a * a
    z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x3(-6.019598008014123785661E-1)) * zz2 + float64x3(5.444622390564711410273E0)) * zz2 +
                    float64x3(-1.626247967210700244449E1)) * zz2 + float64x3(1.956261983317594739197E1)) * zz2 + float64x3(-8.198089802484824371615E0)) / (((((zz2 + float64x3(-1.474091372988853791896E1)) * zz2 +
                    float64x3(7.049610280856842141659E1)) * zz2 + float64x3(-1.471791292232726029859E2)) * zz2 + float64x3(1.395105614657485689735E2)) * zz2 + float64x3(-4.918853881490881290097E1))
    z2 = a * z2 + a

    val = select(z1, z2, a > float64x3(0.625))
    val = select(x, val, a < float64x3(1.0e-8))
    return val * sign
"""

register_kernel('asin', (('x', float64x3()),), asin_f64x3, optimize=True)


acos_f64x3 = """
def acos(x: float64x3) -> float64x3:

    def _asin(x: float64x3) -> float64x3:
    
        sign = copysign(float64x3(1.0), x)
        a = x * sign
    
        zz1 = float64x3(1.0) - a 
        p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x3(-5.634242780008963776856E-1)) * zz1 + float64x3(6.968710824104713396794E0)) * zz1 + float64x3(-2.556901049652824852289E1)) * zz1 +
                float64x3(2.853665548261061424989E1)) / ((((zz1 + float64x3(-2.194779531642920639778E1)) * zz1 + float64x3(1.470656354026814941758E2)) * zz1 + float64x3(-3.838770957603691357202E2)) * zz1 + float64x3(3.424398657913078477438E2))
        zz1 = sqrt(zz1 + zz1)
        z1 = ((float64x3(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x3(6.123233995736765886130E-17))) + float64x3(7.85398163397448309616E-1)
    
        zz2 = a * a
        z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x3(-6.019598008014123785661E-1)) * zz2 + float64x3(5.444622390564711410273E0)) * zz2 +
                        float64x3(-1.626247967210700244449E1)) * zz2 + float64x3(1.956261983317594739197E1)) * zz2 + float64x3(-8.198089802484824371615E0)) / (((((zz2 + float64x3(-1.474091372988853791896E1)) * zz2 +
                        float64x3(7.049610280856842141659E1)) * zz2 + float64x3(-1.471791292232726029859E2)) * zz2 + float64x3(1.395105614657485689735E2)) * zz2 + float64x3(-4.918853881490881290097E1))
        z2 = a * z2 + a
    
        val = select(z1, z2, a > float64x3(0.625))
        val = select(x, val, a < float64x3(1.0e-8))
        return val * sign
    
    mask = x > float64x3(0.5)
    arg = select(sqrt(float64x3(0.5) - 0.5 * x), x, mask)
    val = _asin(arg)
    return select(val * 2.0, (float64x3(7.85398163397448309616E-1) - val + float64x3(6.123233995736765886130E-17)) + float64x3(7.85398163397448309616E-1), mask)
"""

register_kernel('acos', (('x', float64x3()),), acos_f64x3, optimize=True)


asin_f64x4 = """
def asin(x: float64x4) -> float64x4:

    sign = copysign(float64x4(1.0), x)
    a = x * sign

    zz1 = float64x4(1.0) - a 
    p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x4(-5.634242780008963776856E-1)) * zz1 + float64x4(6.968710824104713396794E0)) * zz1 + float64x4(-2.556901049652824852289E1)) * zz1 +
            float64x4(2.853665548261061424989E1)) / ((((zz1 + float64x4(-2.194779531642920639778E1)) * zz1 + float64x4(1.470656354026814941758E2)) * zz1 + float64x4(-3.838770957603691357202E2)) * zz1 + float64x4(3.424398657913078477438E2))
    zz1 = sqrt(zz1 + zz1)
    z1 = ((float64x4(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x4(6.123233995736765886130E-17))) + float64x4(7.85398163397448309616E-1)

    zz2 = a * a
    z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x4(-6.019598008014123785661E-1)) * zz2 + float64x4(5.444622390564711410273E0)) * zz2 +
                    float64x4(-1.626247967210700244449E1)) * zz2 + float64x4(1.956261983317594739197E1)) * zz2 + float64x4(-8.198089802484824371615E0)) / (((((zz2 + float64x4(-1.474091372988853791896E1)) * zz2 +
                    float64x4(7.049610280856842141659E1)) * zz2 + float64x4(-1.471791292232726029859E2)) * zz2 + float64x4(1.395105614657485689735E2)) * zz2 + float64x4(-4.918853881490881290097E1))
    z2 = a * z2 + a

    val = select(z1, z2, a > float64x4(0.625))
    val = select(x, val, a < float64x4(1.0e-8))
    return val * sign
"""

register_kernel('asin', (('x', float64x4()),), asin_f64x4, optimize=True)


acos_f64x4 = """
def acos(x: float64x4) -> float64x4:

    def _asin(x: float64x4) -> float64x4:
    
        sign = copysign(float64x4(1.0), x)
        a = x * sign
    
        zz1 = float64x4(1.0) - a 
        p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x4(-5.634242780008963776856E-1)) * zz1 + float64x4(6.968710824104713396794E0)) * zz1 + float64x4(-2.556901049652824852289E1)) * zz1 +
                float64x4(2.853665548261061424989E1)) / ((((zz1 + float64x4(-2.194779531642920639778E1)) * zz1 + float64x4(1.470656354026814941758E2)) * zz1 + float64x4(-3.838770957603691357202E2)) * zz1 + float64x4(3.424398657913078477438E2))
        zz1 = sqrt(zz1 + zz1)
        z1 = ((float64x4(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x4(6.123233995736765886130E-17))) + float64x4(7.85398163397448309616E-1)
    
        zz2 = a * a
        z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x4(-6.019598008014123785661E-1)) * zz2 + float64x4(5.444622390564711410273E0)) * zz2 +
                        float64x4(-1.626247967210700244449E1)) * zz2 + float64x4(1.956261983317594739197E1)) * zz2 + float64x4(-8.198089802484824371615E0)) / (((((zz2 + float64x4(-1.474091372988853791896E1)) * zz2 +
                        float64x4(7.049610280856842141659E1)) * zz2 + float64x4(-1.471791292232726029859E2)) * zz2 + float64x4(1.395105614657485689735E2)) * zz2 + float64x4(-4.918853881490881290097E1))
        z2 = a * z2 + a
    
        val = select(z1, z2, a > float64x4(0.625))
        val = select(x, val, a < float64x4(1.0e-8))
        return val * sign
    
    mask = x > float64x4(0.5)
    arg = select(sqrt(float64x4(0.5) - 0.5 * x), x, mask)
    val = _asin(arg)
    return select(val * 2.0, (float64x4(7.85398163397448309616E-1) - val + float64x4(6.123233995736765886130E-17)) + float64x4(7.85398163397448309616E-1), mask)
"""

register_kernel('acos', (('x', float64x4()),), acos_f64x4, optimize=True)


asin_f64x8 = """
def asin(x: float64x8) -> float64x8:

    sign = copysign(float64x8(1.0), x)
    a = x * sign

    zz1 = float64x8(1.0) - a 
    p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x8(-5.634242780008963776856E-1)) * zz1 + float64x8(6.968710824104713396794E0)) * zz1 + float64x8(-2.556901049652824852289E1)) * zz1 +
            float64x8(2.853665548261061424989E1)) / ((((zz1 + float64x8(-2.194779531642920639778E1)) * zz1 + float64x8(1.470656354026814941758E2)) * zz1 + float64x8(-3.838770957603691357202E2)) * zz1 + float64x8(3.424398657913078477438E2))
    zz1 = sqrt(zz1 + zz1)
    z1 = ((float64x8(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x8(6.123233995736765886130E-17))) + float64x8(7.85398163397448309616E-1)

    zz2 = a * a
    z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x8(-6.019598008014123785661E-1)) * zz2 + float64x8(5.444622390564711410273E0)) * zz2 +
                    float64x8(-1.626247967210700244449E1)) * zz2 + float64x8(1.956261983317594739197E1)) * zz2 + float64x8(-8.198089802484824371615E0)) / (((((zz2 + float64x8(-1.474091372988853791896E1)) * zz2 +
                    float64x8(7.049610280856842141659E1)) * zz2 + float64x8(-1.471791292232726029859E2)) * zz2 + float64x8(1.395105614657485689735E2)) * zz2 + float64x8(-4.918853881490881290097E1))
    z2 = a * z2 + a

    val = select(z1, z2, a > float64x8(0.625))
    val = select(x, val, a < float64x8(1.0e-8))
    return val * sign
"""

register_kernel('asin', (('x', float64x8()),), asin_f64x8, optimize=True)


acos_f64x8 = """
def acos(x: float64x8) -> float64x8:

    def _asin(x: float64x8) -> float64x8:
    
        sign = copysign(float64x8(1.0), x)
        a = x * sign
    
        zz1 = float64x8(1.0) - a 
        p1 = zz1 * ((((2.967721961301243206100E-3 * zz1 + float64x8(-5.634242780008963776856E-1)) * zz1 + float64x8(6.968710824104713396794E0)) * zz1 + float64x8(-2.556901049652824852289E1)) * zz1 +
                float64x8(2.853665548261061424989E1)) / ((((zz1 + float64x8(-2.194779531642920639778E1)) * zz1 + float64x8(1.470656354026814941758E2)) * zz1 + float64x8(-3.838770957603691357202E2)) * zz1 + float64x8(3.424398657913078477438E2))
        zz1 = sqrt(zz1 + zz1)
        z1 = ((float64x8(7.85398163397448309616E-1) - zz1) - (zz1 * p1 - float64x8(6.123233995736765886130E-17))) + float64x8(7.85398163397448309616E-1)
    
        zz2 = a * a
        z2 = zz2 * (((((4.253011369004428248960E-3 * zz2 + float64x8(-6.019598008014123785661E-1)) * zz2 + float64x8(5.444622390564711410273E0)) * zz2 +
                        float64x8(-1.626247967210700244449E1)) * zz2 + float64x8(1.956261983317594739197E1)) * zz2 + float64x8(-8.198089802484824371615E0)) / (((((zz2 + float64x8(-1.474091372988853791896E1)) * zz2 +
                        float64x8(7.049610280856842141659E1)) * zz2 + float64x8(-1.471791292232726029859E2)) * zz2 + float64x8(1.395105614657485689735E2)) * zz2 + float64x8(-4.918853881490881290097E1))
        z2 = a * z2 + a
    
        val = select(z1, z2, a > float64x8(0.625))
        val = select(x, val, a < float64x8(1.0e-8))
        return val * sign
    
    mask = x > float64x8(0.5)
    arg = select(sqrt(float64x8(0.5) - 0.5 * x), x, mask)
    val = _asin(arg)
    return select(val * 2.0, (float64x8(7.85398163397448309616E-1) - val + float64x8(6.123233995736765886130E-17)) + float64x8(7.85398163397448309616E-1), mask)
"""

register_kernel('acos', (('x', float64x8()),), acos_f64x8, optimize=True)


asin_f32 = """
def asin(x: float32) -> float32:

    if x > 0:
        sign = 1.0
        a = x
    else:
        sign = -1.0
        a = -x
    
    if a < 1.0e-4:
        z = a
        if sign < 0:
            z = -z
        return z
    
    if a > 0.5:
        z = 0.5 * (1.0 - a)
        x = sqrt(z)
        flag = 1
    else:
        x = a
        z = x * x
        flag = 0

    z = ((((4.2163199048E-2 * z + 2.4181311049E-2) * z + 4.5470025998E-2) * z + 7.4953002686E-2) * z + 1.6666752422E-1) * z * x + x

    if flag:
        z = 1.5707963267948966192 - (z + z)
    
    if sign < 0:
        z = -z
    return z
"""

register_kernel('asin', (('x', float32()),), asin_f32, optimize=True)


acos_f32 = """
def acos(x: float32) -> float32:

    def _asin(x: float32) -> float32:
    
        if x > 0:
            sign = 1.0
            a = x
        else:
            sign = -1.0
            a = -x
        
        if a < 1.0e-4:
            z = a
            if sign < 0:
                z = -z
            return z
        
        if a > 0.5:
            z = 0.5 * (1.0 - a)
            x = sqrt(z)
            flag = 1
        else:
            x = a
            z = x * x
            flag = 0
    
        z = ((((4.2163199048E-2 * z + 2.4181311049E-2) * z + 4.5470025998E-2) * z + 7.4953002686E-2) * z + 1.6666752422E-1) * z * x + x
    
        if flag:
            z = 1.5707963267948966192 - (z + z)
        
        if sign < 0:
            z = -z
        return z

    if x < -0.5:
        arg = sqrt(0.5 * (1.0 + x))
    elif x > 0.5:
        arg = sqrt(0.5 * (1.0 - x))
    else:
        arg = x
    
    val = _asin(arg)
    
    if x < -0.5:
        return 3.141592653589793238 - 2.0 * val
     
    if x > 0.5:
       return 2.0 * val
    
    return 1.5707963267948966192 - val
"""

register_kernel('acos', (('x', float32()),), acos_f32, optimize=True)


asin_f32x2 = """
def asin(x: float32x2) -> float32x2:

    sign = copysign(float32x2(1.0), x)
    a = x * sign
    
    mask = a > float32x2(0.5)
    z = select(0.5 * (float32x2(1.0) - a), a * a, mask)
    x = select(sqrt(z), a, mask)
    
    z = ((((4.2163199048E-2 * z + float32x2(2.4181311049E-2)) * z + float32x2(4.5470025998E-2)) * z + float32x2(7.4953002686E-2)) * z + float32x2(1.6666752422E-1)) * z * x + x
    
    z = select(float32x2(1.5707963267948966192) - (z + z), z, mask)
    
    z = select(a, z, a < float32x2(1.0e-4))
    return z * sign
"""

register_kernel('asin', (('x', float32x2()),), asin_f32x2, optimize=True)


acos_f32x2 = """
def acos(x: float32x2) -> float32x2:

    def _asin(x: float32x2) -> float32x2:
    
        sign = copysign(float32x2(1.0), x)
        a = x * sign
        
        mask = a > float32x2(0.5)
        z = select(0.5 * (float32x2(1.0) - a), a * a, mask)
        x = select(sqrt(z), a, mask)
        
        z = ((((4.2163199048E-2 * z + float32x2(2.4181311049E-2)) * z + float32x2(4.5470025998E-2)) * z + float32x2(7.4953002686E-2)) * z + float32x2(1.6666752422E-1)) * z * x + x
        
        z = select(float32x2(1.5707963267948966192) - (z + z), z, mask)
        
        z = select(a, z, a < float32x2(1.0e-4))
        return z * sign

    arg = select(sqrt(0.5 * (float32x2(1.0) + x)), x, x < float32x2(-0.5))
    arg = select(sqrt(0.5 * (float32x2(1.0) - x)), arg, x > float32x2(0.5))
    
    val = _asin(arg)
    
    result = select(float32x2(3.141592653589793238) - 2.0 * val, float32x2(1.5707963267948966192) - val, x < float32x2(-0.5))
    result = select(2.0 * val, result, x > float32x2(0.5))
    return result
"""

register_kernel('acos', (('x', float32x2()),), acos_f32x2, optimize=True)

asin_f32x3 = """
def asin(x: float32x3) -> float32x3:

    sign = copysign(float32x3(1.0), x)
    a = x * sign

    mask = a > float32x3(0.5)
    z = select(0.5 * (float32x3(1.0) - a), a * a, mask)
    x = select(sqrt(z), a, mask)

    z = ((((4.2163199048E-2 * z + float32x3(2.4181311049E-2)) * z + float32x3(4.5470025998E-2)) * z + float32x3(7.4953002686E-2)) * z + float32x3(1.6666752422E-1)) * z * x + x

    z = select(float32x3(1.5707963267948966192) - (z + z), z, mask)

    z = select(a, z, a < float32x3(1.0e-4))
    return z * sign
"""

register_kernel('asin', (('x', float32x3()),), asin_f32x3, optimize=True)


acos_f32x3 = """
def acos(x: float32x3) -> float32x3:

    def _asin(x: float32x3) -> float32x3:
    
        sign = copysign(float32x3(1.0), x)
        a = x * sign
    
        mask = a > float32x3(0.5)
        z = select(0.5 * (float32x3(1.0) - a), a * a, mask)
        x = select(sqrt(z), a, mask)
    
        z = ((((4.2163199048E-2 * z + float32x3(2.4181311049E-2)) * z + float32x3(4.5470025998E-2)) * z + float32x3(7.4953002686E-2)) * z + float32x3(1.6666752422E-1)) * z * x + x
    
        z = select(float32x3(1.5707963267948966192) - (z + z), z, mask)
    
        z = select(a, z, a < float32x3(1.0e-4))
        return z * sign

    arg = select(sqrt(0.5 * (float32x3(1.0) + x)), x, x < float32x3(-0.5))
    arg = select(sqrt(0.5 * (float32x3(1.0) - x)), arg, x > float32x3(0.5))
    
    val = _asin(arg)
    
    result = select(float32x3(3.141592653589793238) - 2.0 * val, float32x3(1.5707963267948966192) - val, x < float32x3(-0.5))
    result = select(2.0 * val, result, x > float32x3(0.5))
    return result
"""

register_kernel('acos', (('x', float32x3()),), acos_f32x3, optimize=True)


asin_f32x4 = """
def asin(x: float32x4) -> float32x4:

    sign = copysign(float32x4(1.0), x)
    a = x * sign

    mask = a > float32x4(0.5)
    z = select(0.5 * (float32x4(1.0) - a), a * a, mask)
    x = select(sqrt(z), a, mask)

    z = ((((4.2163199048E-2 * z + float32x4(2.4181311049E-2)) * z + float32x4(4.5470025998E-2)) * z + float32x4(7.4953002686E-2)) * z + float32x4(1.6666752422E-1)) * z * x + x

    z = select(float32x4(1.5707963267948966192) - (z + z), z, mask)

    z = select(a, z, a < float32x4(1.0e-4))
    return z * sign
"""

register_kernel('asin', (('x', float32x4()),), asin_f32x4, optimize=True)


acos_f32x4 = """
def acos(x: float32x4) -> float32x4:

    def _asin(x: float32x4) -> float32x4:
    
        sign = copysign(float32x4(1.0), x)
        a = x * sign
    
        mask = a > float32x4(0.5)
        z = select(0.5 * (float32x4(1.0) - a), a * a, mask)
        x = select(sqrt(z), a, mask)
    
        z = ((((4.2163199048E-2 * z + float32x4(2.4181311049E-2)) * z + float32x4(4.5470025998E-2)) * z + float32x4(7.4953002686E-2)) * z + float32x4(1.6666752422E-1)) * z * x + x
    
        z = select(float32x4(1.5707963267948966192) - (z + z), z, mask)
    
        z = select(a, z, a < float32x4(1.0e-4))
        return z * sign


    arg = select(sqrt(0.5 * (float32x4(1.0) + x)), x, x < float32x4(-0.5))
    arg = select(sqrt(0.5 * (float32x4(1.0) - x)), arg, x > float32x4(0.5))

    val = _asin(arg)

    result = select(float32x4(3.141592653589793238) - 2.0 * val, float32x4(1.5707963267948966192) - val, x < float32x4(-0.5))
    result = select(2.0 * val, result, x > float32x4(0.5))
    return result
"""

register_kernel('acos', (('x', float32x4()),), acos_f32x4, optimize=True)


asin_f32x8 = """
def asin(x: float32x8) -> float32x8:

    sign = copysign(float32x8(1.0), x)
    a = x * sign

    mask = a > float32x8(0.5)
    z = select(0.5 * (float32x8(1.0) - a), a * a, mask)
    x = select(sqrt(z), a, mask)

    z = ((((4.2163199048E-2 * z + float32x8(2.4181311049E-2)) * z + float32x8(4.5470025998E-2)) * z + float32x8(7.4953002686E-2)) * z + float32x8(1.6666752422E-1)) * z * x + x

    z = select(float32x8(1.5707963267948966192) - (z + z), z, mask)

    z = select(a, z, a < float32x8(1.0e-4))
    return z * sign
"""

register_kernel('asin', (('x', float32x8()),), asin_f32x8, optimize=True)


acos_f32x8 = """
def acos(x: float32x8) -> float32x8:

    def _asin(x: float32x8) -> float32x8:
    
        sign = copysign(float32x8(1.0), x)
        a = x * sign
    
        mask = a > float32x8(0.5)
        z = select(0.5 * (float32x8(1.0) - a), a * a, mask)
        x = select(sqrt(z), a, mask)
    
        z = ((((4.2163199048E-2 * z + float32x8(2.4181311049E-2)) * z + float32x8(4.5470025998E-2)) * z + float32x8(7.4953002686E-2)) * z + float32x8(1.6666752422E-1)) * z * x + x
    
        z = select(float32x8(1.5707963267948966192) - (z + z), z, mask)
    
        z = select(a, z, a < float32x8(1.0e-4))
        return z * sign

    arg = select(sqrt(0.5 * (float32x8(1.0) + x)), x, x < float32x8(-0.5))
    arg = select(sqrt(0.5 * (float32x8(1.0) - x)), arg, x > float32x8(0.5))

    val = _asin(arg)

    result = select(float32x8(3.141592653589793238) - 2.0 * val, float32x8(1.5707963267948966192) - val, x < float32x8(-0.5))
    result = select(2.0 * val, result, x > float32x8(0.5))
    return result
"""

register_kernel('acos', (('x', float32x8()),), acos_f32x8, optimize=True)


asin_f32x16 = """
def asin(x: float32x16) -> float32x16:

    sign = copysign(float32x16(1.0), x)
    a = x * sign

    mask = a > float32x16(0.5)
    z = select(0.5 * (float32x16(1.0) - a), a * a, mask)
    x = select(sqrt(z), a, mask)

    z = ((((4.2163199048E-2 * z + float32x16(2.4181311049E-2)) * z + float32x16(4.5470025998E-2)) * z + float32x16(7.4953002686E-2)) * z + float32x16(1.6666752422E-1)) * z * x + x

    z = select(float32x16(1.5707963267948966192) - (z + z), z, mask)

    z = select(a, z, a < float32x16(1.0e-4))
    return z * sign
"""

register_kernel('asin', (('x', float32x16()),), asin_f32x16, optimize=True)


acos_f32x16 = """
def acos(x: float32x16) -> float32x16:

    def _asin(x: float32x16) -> float32x16:
    
        sign = copysign(float32x16(1.0), x)
        a = x * sign
    
        mask = a > float32x16(0.5)
        z = select(0.5 * (float32x16(1.0) - a), a * a, mask)
        x = select(sqrt(z), a, mask)
    
        z = ((((4.2163199048E-2 * z + float32x16(2.4181311049E-2)) * z + float32x16(4.5470025998E-2)) * z + float32x16(7.4953002686E-2)) * z + float32x16(1.6666752422E-1)) * z * x + x
    
        z = select(float32x16(1.5707963267948966192) - (z + z), z, mask)
    
        z = select(a, z, a < float32x16(1.0e-4))
        return z * sign

    arg = select(sqrt(0.5 * (float32x16(1.0) + x)), x, x < float32x16(-0.5))
    arg = select(sqrt(0.5 * (float32x16(1.0) - x)), arg, x > float32x16(0.5))

    val = _asin(arg)

    result = select(float32x16(3.141592653589793238) - 2.0 * val, float32x16(1.5707963267948966192) - val, x < float32x16(-0.5))
    result = select(2.0 * val, result, x > float32x16(0.5))
    return result
"""

register_kernel('acos', (('x', float32x16()),), acos_f32x16, optimize=True)
