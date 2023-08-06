from .dbl_arg import float64
from .flt_arg import float32
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16
from .cgen import register_kernel

__all__ = []

atan_f64 = """
def atan(x: float64) -> float64:
    
    if x == 0.0:
        return x

    sign = 1.0
    if x < 0:
        x = -x
        sign = -1.0

    flag = 0
    if x > 2.41421356237309504880:
        y = 1.57079632679489661923
        flag = 1
        x = -1.0 / x
    elif x <= 0.66:
        y = 0.0
    else:
        y = 7.85398163397448309616E-1
        flag = 2
        x = (x - 1.0) / (x + 1.0)
    
    z = x * x
     
    z = z * ((((-8.750608600031904122785E-1 * z + -1.615753718733365076637E1) * z + -7.500855792314704667340E1) * z +
        -1.228866684490136173410E2) * z + -6.485021904942025371773E1) /  (((((z + 2.485846490142306297962E1) * z +
        1.650270098316988542046E2) * z + 4.328810604912902668951E2) * z + 4.853903996359136964868E2) * z + 1.945506571482613964425E2)
        
    z = x * z + x
    
    if flag == 2:
        z += 0.5 * 6.123233995736765886130E-17
    elif flag == 1:
        z += 6.123233995736765886130E-17
    
    y = y + z
    if sign < 0:
        y = -y

    return y

"""

register_kernel('atan', (('x', float64()),), atan_f64, optimize=True)


atan_f64x2 = """
def atan(x: float64x2) -> float64x2:

    sign = copysign(float64x2(1.0), x)
    x = abs(x)
    
    mask1 = x > float64x2(2.41421356237309504880)
    mask2 = x <= float64x2(0.66)
    flag = select(int32x2(0), select(int32x2(1), int32x2(2), mask1), mask2)
    y = select(float64x2(0), select(float64x2(1.57079632679489661923), float64x2(7.85398163397448309616E-1), mask1), mask2)
    x = select(x, select(float64x2(-1.0) / x, (x - float64x2(1.0)) / (x + float64x2(1.0)), mask1), mask2)

    z = x * x

    z = z * ((((-8.750608600031904122785E-1 * z + float64x2(-1.615753718733365076637E1)) * z + float64x2(-7.500855792314704667340E1)) * z +
        float64x2(-1.228866684490136173410E2)) * z + float64x2(-6.485021904942025371773E1)) /  (((((z + float64x2(2.485846490142306297962E1)) * z +
        float64x2(1.650270098316988542046E2)) * z + float64x2(4.328810604912902668951E2)) * z + float64x2(4.853903996359136964868E2)) * z + float64x2(1.945506571482613964425E2))

    z = x * z + x

    z = select(z + float64x2(0.5 * 6.123233995736765886130E-17), z, flag == int32x2(2))
    z = select(z + float64x2(6.123233995736765886130E-17), z, flag == int32x2(1))
    
    y = y + z
    return y * sign
"""

register_kernel('atan', (('x', float64x2()),), atan_f64x2, optimize=True)


atan_f64x3 = """
def atan(x: float64x3) -> float64x3:

    sign = copysign(float64x3(1.0), x)
    x = abs(x)

    mask1 = x > float64x3(2.41421356237309504880)
    mask2 = x <= float64x3(0.66)
    flag = select(int32x3(0), select(int32x3(1), int32x3(2), mask1), mask2)
    y = select(float64x3(0), select(float64x3(1.57079632679489661923), float64x3(7.85398163397448309616E-1), mask1), mask2)
    x = select(x, select(float64x3(-1.0) / x, (x - float64x3(1.0)) / (x + float64x3(1.0)), mask1), mask2)

    z = x * x

    z = z * ((((-8.750608600031904122785E-1 * z + float64x3(-1.615753718733365076637E1)) * z + float64x3(-7.500855792314704667340E1)) * z +
        float64x3(-1.228866684490136173410E2)) * z + float64x3(-6.485021904942025371773E1)) /  (((((z + float64x3(2.485846490142306297962E1)) * z +
        float64x3(1.650270098316988542046E2)) * z + float64x3(4.328810604912902668951E2)) * z + float64x3(4.853903996359136964868E2)) * z + float64x3(1.945506571482613964425E2))

    z = x * z + x

    z = select(z + float64x3(0.5 * 6.123233995736765886130E-17), z, flag == int32x3(2))
    z = select(z + float64x3(6.123233995736765886130E-17), z, flag == int32x3(1))

    y = y + z
    return y * sign
"""

register_kernel('atan', (('x', float64x3()),), atan_f64x3, optimize=True)


atan_f64x4 = """
def atan(x: float64x4) -> float64x4:

    sign = copysign(float64x4(1.0), x)
    x = abs(x)

    mask1 = x > float64x4(2.41421356237309504880)
    mask2 = x <= float64x4(0.66)
    flag = select(int32x4(0), select(int32x4(1), int32x4(2), mask1), mask2)
    y = select(float64x4(0), select(float64x4(1.57079632679489661923), float64x4(7.85398163397448309616E-1), mask1), mask2)
    x = select(x, select(float64x4(-1.0) / x, (x - float64x4(1.0)) / (x + float64x4(1.0)), mask1), mask2)

    z = x * x

    z = z * ((((-8.750608600031904122785E-1 * z + float64x4(-1.615753718733365076637E1)) * z + float64x4(-7.500855792314704667340E1)) * z +
        float64x4(-1.228866684490136173410E2)) * z + float64x4(-6.485021904942025371773E1)) /  (((((z + float64x4(2.485846490142306297962E1)) * z +
        float64x4(1.650270098316988542046E2)) * z + float64x4(4.328810604912902668951E2)) * z + float64x4(4.853903996359136964868E2)) * z + float64x4(1.945506571482613964425E2))

    z = x * z + x

    z = select(z + float64x4(0.5 * 6.123233995736765886130E-17), z, flag == int32x4(2))
    z = select(z + float64x4(6.123233995736765886130E-17), z, flag == int32x4(1))

    y = y + z
    return y * sign
"""

register_kernel('atan', (('x', float64x4()),), atan_f64x4, optimize=True)


atan_f64x8 = """
def atan(x: float64x8) -> float64x8:

    sign = copysign(float64x8(1.0), x)
    x = abs(x)

    mask1 = x > float64x8(2.41421356237309504880)
    mask2 = x <= float64x8(0.66)
    flag = select(int32x8(0), select(int32x8(1), int32x8(2), mask1), mask2)
    y = select(float64x8(0), select(float64x8(1.57079632679489661923), float64x8(7.85398163397448309616E-1), mask1), mask2)
    x = select(x, select(float64x8(-1.0) / x, (x - float64x8(1.0)) / (x + float64x8(1.0)), mask1), mask2)

    z = x * x

    z = z * ((((-8.750608600031904122785E-1 * z + float64x8(-1.615753718733365076637E1)) * z + float64x8(-7.500855792314704667340E1)) * z +
        float64x8(-1.228866684490136173410E2)) * z + float64x8(-6.485021904942025371773E1)) /  (((((z + float64x8(2.485846490142306297962E1)) * z +
        float64x8(1.650270098316988542046E2)) * z + float64x8(4.328810604912902668951E2)) * z + float64x8(4.853903996359136964868E2)) * z + float64x8(1.945506571482613964425E2))

    z = x * z + x

    z = select(z + float64x8(0.5 * 6.123233995736765886130E-17), z, flag == int32x8(2))
    z = select(z + float64x8(6.123233995736765886130E-17), z, flag == int32x8(1))

    y = y + z
    return y * sign
"""

register_kernel('atan', (('x', float64x8()),), atan_f64x8, optimize=True)


atan_f32 = """
def atan(x: float32) -> float32:

    sign = float32(1.0)
    if x < 0:
        x = -x
        sign = float32(-1.0)

    if x > 2.414213562373095:
        y = float32(1.5707963267948966192)
        x = float32(-1.0) / x
    elif x > 0.4142135623730950:
        y = float32(0.7853981633974483096)
        x = (x - 1.0) / (x + 1.0)
    else:
        y = float32(0.0)

    z = x * x
    
    y += ((( 8.05374449538e-2 * z - 1.38776856032E-1) * z + 1.99777106478E-1) * z - 3.33329491539E-1) * z * x + x
    if sign < 0:
        y = -y

    return y

"""

register_kernel('atan', (('x', float32()),), atan_f32, optimize=True)


atan_f32x2 = """
def atan(x: float32x2) -> float32x2:
     
    sign = copysign(float32x2(1.0), x)
    x = abs(x)

    mask1 = x > float32x2(2.414213562373095)
    mask2 = x > float32x2(0.4142135623730950)
    
    y = select(float32x2(1.5707963267948966192), select(float32x2(0.7853981633974483096), float32x2(0.0), mask2), mask1)
    x = select(float32x2(-1.0) / x, select((x - float32x2(1.0)) / (x + float32x2(1.0)), x, mask2), mask1)
    
    z = x * x
    y += (((8.05374449538e-2 * z - float32x2(1.38776856032E-1)) * z + float32x2(1.99777106478E-1)) * z - float32x2(3.33329491539E-1)) * z * x + x
    return y * sign
"""

register_kernel('atan', (('x', float32x2()),), atan_f32x2, optimize=True)


atan_f32x3 = """
def atan(x: float32x3) -> float32x3:

    sign = copysign(float32x3(1.0), x)
    x = abs(x)

    mask1 = x > float32x3(2.414213562373095)
    mask2 = x > float32x3(0.4142135623730950)

    y = select(float32x3(1.5707963267948966192), select(float32x3(0.7853981633974483096), float32x3(0.0), mask2), mask1)
    x = select(float32x3(-1.0) / x, select((x - float32x3(1.0)) / (x + float32x3(1.0)), x, mask2), mask1)

    z = x * x
    y += (((8.05374449538e-2 * z - float32x3(1.38776856032E-1)) * z + float32x3(1.99777106478E-1)) * z - float32x3(3.33329491539E-1)) * z * x + x
    return y * sign
"""

register_kernel('atan', (('x', float32x3()),), atan_f32x3, optimize=True)


atan_f32x4 = """
def atan(x: float32x4) -> float32x4:

    sign = copysign(float32x4(1.0), x)
    x = abs(x)

    mask1 = x > float32x4(2.414213562373095)
    mask2 = x > float32x4(0.4142135623730950)

    y = select(float32x4(1.5707963267948966192), select(float32x4(0.7853981633974483096), float32x4(0.0), mask2), mask1)
    x = select(float32x4(-1.0) / x, select((x - float32x4(1.0)) / (x + float32x4(1.0)), x, mask2), mask1)

    z = x * x
    y += (((8.05374449538e-2 * z - float32x4(1.38776856032E-1)) * z + float32x4(1.99777106478E-1)) * z - float32x4(3.33329491539E-1)) * z * x + x
    return y * sign
"""

register_kernel('atan', (('x', float32x4()),), atan_f32x4, optimize=True)


atan_f32x8 = """
def atan(x: float32x8) -> float32x8:

    sign = copysign(float32x8(1.0), x)
    x = abs(x)

    mask1 = x > float32x8(2.414213562373095)
    mask2 = x > float32x8(0.4142135623730950)

    y = select(float32x8(1.5707963267948966192), select(float32x8(0.7853981633974483096), float32x8(0.0), mask2), mask1)
    x = select(float32x8(-1.0) / x, select((x - float32x8(1.0)) / (x + float32x8(1.0)), x, mask2), mask1)

    z = x * x
    y += (((8.05374449538e-2 * z - float32x8(1.38776856032E-1)) * z + float32x8(1.99777106478E-1)) * z - float32x8(3.33329491539E-1)) * z * x + x
    return y * sign
"""

register_kernel('atan', (('x', float32x8()),), atan_f32x8, optimize=True)


atan_f32x16 = """
def atan(x: float32x16) -> float32x16:

    sign = copysign(float32x16(1.0), x)
    x = abs(x)

    mask1 = x > float32x16(2.414213562373095)
    mask2 = x > float32x16(0.4142135623730950)

    y = select(float32x16(1.5707963267948966192), select(float32x16(0.7853981633974483096), float32x16(0.0), mask2), mask1)
    x = select(float32x16(-1.0) / x, select((x - float32x16(1.0)) / (x + float32x16(1.0)), x, mask2), mask1)

    z = x * x
    y += (((8.05374449538e-2 * z - float32x16(1.38776856032E-1)) * z + float32x16(1.99777106478E-1)) * z - float32x16(3.33329491539E-1)) * z * x + x
    return y * sign
"""

register_kernel('atan', (('x', float32x16()),), atan_f32x16, optimize=True)


atan2_f64 = """
def atan2(y: float64, x: float64) -> float64:

    def _atan(x: float64) -> float64:
        
        if x == 0.0:
            return x
    
        sign = 1.0
        if x < 0:
            x = -x
            sign = -1.0
    
        flag = 0
        if x > 2.41421356237309504880:
            y = 1.57079632679489661923
            flag = 1
            x = -1.0 / x
        elif x <= 0.66:
            y = 0.0
        else:
            y = 7.85398163397448309616E-1
            flag = 2
            x = (x - 1.0) / (x + 1.0)
        
        z = x * x
         
        z = z * ((((-8.750608600031904122785E-1 * z + -1.615753718733365076637E1) * z + -7.500855792314704667340E1) * z +
            -1.228866684490136173410E2) * z + -6.485021904942025371773E1) /  (((((z + 2.485846490142306297962E1) * z +
            1.650270098316988542046E2) * z + 4.328810604912902668951E2) * z + 4.853903996359136964868E2) * z + 1.945506571482613964425E2)
            
        z = x * z + x
        
        if flag == 2:
            z += 0.5 * 6.123233995736765886130E-17
        elif flag == 1:
            z += 6.123233995736765886130E-17
        
        y = y + z
        if sign < 0:
            y = -y
    
        return y


    code = 0
    if x < 0:
        code = 2
    if y < 0:
        code |= 1
    
    if x == 0.0:
        if code & 1:
            return -1.57079632679489661923
        if y == 0.0:
            return 0.0
        return 1.57079632679489661923
    
    if y == 0.0:
        if code & 2:
            return 3.14159265358979323846
        return 0.0

    if code == 2:
        w = 3.14159265358979323846
    elif code == 3:
        w = -3.14159265358979323846
    else:
        w = 0.0

    z = w + _atan(y/x)
    return z
"""

register_kernel('atan2', (('y', float64()), ('x', float64())), atan2_f64, optimize=True)


atan2_f64x2 = """
def atan2(y: float64x2, x: float64x2) -> float64x2:

    def _atan(x: float64x2) -> float64x2:
    
        sign = copysign(float64x2(1.0), x)
        x = abs(x)
        
        mask1 = x > float64x2(2.41421356237309504880)
        mask2 = x <= float64x2(0.66)
        flag = select(int32x2(0), select(int32x2(1), int32x2(2), mask1), mask2)
        y = select(float64x2(0), select(float64x2(1.57079632679489661923), float64x2(7.85398163397448309616E-1), mask1), mask2)
        x = select(x, select(float64x2(-1.0) / x, (x - float64x2(1.0)) / (x + float64x2(1.0)), mask1), mask2)
    
        z = x * x
    
        z = z * ((((-8.750608600031904122785E-1 * z + float64x2(-1.615753718733365076637E1)) * z + float64x2(-7.500855792314704667340E1)) * z +
            float64x2(-1.228866684490136173410E2)) * z + float64x2(-6.485021904942025371773E1)) /  (((((z + float64x2(2.485846490142306297962E1)) * z +
            float64x2(1.650270098316988542046E2)) * z + float64x2(4.328810604912902668951E2)) * z + float64x2(4.853903996359136964868E2)) * z + float64x2(1.945506571482613964425E2))
    
        z = x * z + x
    
        z = select(z + float64x2(0.5 * 6.123233995736765886130E-17), z, flag == int32x2(2))
        z = select(z + float64x2(6.123233995736765886130E-17), z, flag == int32x2(1))
        
        y = y + z
        return y * sign

    code = int32x2(0)
    code = select(int32x2(2), code, x < float64x2(0))
    code = select(code | int32x2(1), code, y < float64x2(0))
    
    w = select(float64x2(3.14159265358979323846), float64x2(0), code == int32x2(2))
    w = select(float64x2(-3.14159265358979323846), w, code == int32x2(3))
    
    z = w + _atan(y/x)
    
    v1 = select(float64x2(1.57079632679489661923), float64x2(-1.57079632679489661923), (code & int32x2(1)) == int32x2(0))
    z = select(v1, z, x == float64x2(0.0))
    
    v1 = select(float64x2(0.0), float64x2(3.14159265358979323846), (code & int32x2(2)) == int32x2(0))
    z = select(v1, z, y == float64x2(0.0))

    return z
"""

register_kernel('atan2', (('y', float64x2()), ('x', float64x2())), atan2_f64x2, optimize=True)


atan2_f64x3 = """
def atan2(y: float64x3, x: float64x3) -> float64x3:

    def _atan(x: float64x3) -> float64x3:
    
        sign = copysign(float64x3(1.0), x)
        x = abs(x)
    
        mask1 = x > float64x3(2.41421356237309504880)
        mask2 = x <= float64x3(0.66)
        flag = select(int32x3(0), select(int32x3(1), int32x3(2), mask1), mask2)
        y = select(float64x3(0), select(float64x3(1.57079632679489661923), float64x3(7.85398163397448309616E-1), mask1), mask2)
        x = select(x, select(float64x3(-1.0) / x, (x - float64x3(1.0)) / (x + float64x3(1.0)), mask1), mask2)
    
        z = x * x
    
        z = z * ((((-8.750608600031904122785E-1 * z + float64x3(-1.615753718733365076637E1)) * z + float64x3(-7.500855792314704667340E1)) * z +
            float64x3(-1.228866684490136173410E2)) * z + float64x3(-6.485021904942025371773E1)) /  (((((z + float64x3(2.485846490142306297962E1)) * z +
            float64x3(1.650270098316988542046E2)) * z + float64x3(4.328810604912902668951E2)) * z + float64x3(4.853903996359136964868E2)) * z + float64x3(1.945506571482613964425E2))
    
        z = x * z + x
    
        z = select(z + float64x3(0.5 * 6.123233995736765886130E-17), z, flag == int32x3(2))
        z = select(z + float64x3(6.123233995736765886130E-17), z, flag == int32x3(1))
    
        y = y + z
        return y * sign
  
    code = int32x3(0)
    code = select(int32x3(2), code, x < float64x3(0))
    code = select(code | int32x3(1), code, y < float64x3(0))

    w = select(float64x3(3.14159265358979323846), float64x3(0), code == int32x3(2))
    w = select(float64x3(-3.14159265358979323846), w, code == int32x3(3))

    z = w + _atan(y/x)

    v1 = select(float64x3(1.57079632679489661923), float64x3(-1.57079632679489661923), (code & int32x3(1)) == int32x3(0))
    z = select(v1, z, x == float64x3(0.0))

    v1 = select(float64x3(0.0), float64x3(3.14159265358979323846), (code & int32x3(2)) == int32x3(0))
    z = select(v1, z, y == float64x3(0.0))

    return z
"""

register_kernel('atan2', (('y', float64x3()), ('x', float64x3())), atan2_f64x3, optimize=True)

atan2_f64x4 = """
def atan2(y: float64x4, x: float64x4) -> float64x4:

    def _atan(x: float64x4) -> float64x4:
    
        sign = copysign(float64x4(1.0), x)
        x = abs(x)
    
        mask1 = x > float64x4(2.41421356237309504880)
        mask2 = x <= float64x4(0.66)
        flag = select(int32x4(0), select(int32x4(1), int32x4(2), mask1), mask2)
        y = select(float64x4(0), select(float64x4(1.57079632679489661923), float64x4(7.85398163397448309616E-1), mask1), mask2)
        x = select(x, select(float64x4(-1.0) / x, (x - float64x4(1.0)) / (x + float64x4(1.0)), mask1), mask2)
    
        z = x * x
    
        z = z * ((((-8.750608600031904122785E-1 * z + float64x4(-1.615753718733365076637E1)) * z + float64x4(-7.500855792314704667340E1)) * z +
            float64x4(-1.228866684490136173410E2)) * z + float64x4(-6.485021904942025371773E1)) /  (((((z + float64x4(2.485846490142306297962E1)) * z +
            float64x4(1.650270098316988542046E2)) * z + float64x4(4.328810604912902668951E2)) * z + float64x4(4.853903996359136964868E2)) * z + float64x4(1.945506571482613964425E2))
    
        z = x * z + x
    
        z = select(z + float64x4(0.5 * 6.123233995736765886130E-17), z, flag == int32x4(2))
        z = select(z + float64x4(6.123233995736765886130E-17), z, flag == int32x4(1))
    
        y = y + z
        return y * sign

    code = int32x4(0)
    code = select(int32x4(2), code, x < float64x4(0))
    code = select(code | int32x4(1), code, y < float64x4(0))

    w = select(float64x4(3.14159265358979323846), float64x4(0), code == int32x4(2))
    w = select(float64x4(-3.14159265358979323846), w, code == int32x4(3))

    z = w + _atan(y/x)

    v1 = select(float64x4(1.57079632679489661923), float64x4(-1.57079632679489661923), (code & int32x4(1)) == int32x4(0))
    z = select(v1, z, x == float64x4(0.0))

    v1 = select(float64x4(0.0), float64x4(3.14159265358979323846), (code & int32x4(2)) == int32x4(0))
    z = select(v1, z, y == float64x4(0.0))

    return z
"""

register_kernel('atan2', (('y', float64x4()), ('x', float64x4())), atan2_f64x4, optimize=True)


atan2_f64x8 = """
def atan2(y: float64x8, x: float64x8) -> float64x8:

    def _atan(x: float64x8) -> float64x8:
    
        sign = copysign(float64x8(1.0), x)
        x = abs(x)
    
        mask1 = x > float64x8(2.41421356237309504880)
        mask2 = x <= float64x8(0.66)
        flag = select(int32x8(0), select(int32x8(1), int32x8(2), mask1), mask2)
        y = select(float64x8(0), select(float64x8(1.57079632679489661923), float64x8(7.85398163397448309616E-1), mask1), mask2)
        x = select(x, select(float64x8(-1.0) / x, (x - float64x8(1.0)) / (x + float64x8(1.0)), mask1), mask2)
    
        z = x * x
    
        z = z * ((((-8.750608600031904122785E-1 * z + float64x8(-1.615753718733365076637E1)) * z + float64x8(-7.500855792314704667340E1)) * z +
            float64x8(-1.228866684490136173410E2)) * z + float64x8(-6.485021904942025371773E1)) /  (((((z + float64x8(2.485846490142306297962E1)) * z +
            float64x8(1.650270098316988542046E2)) * z + float64x8(4.328810604912902668951E2)) * z + float64x8(4.853903996359136964868E2)) * z + float64x8(1.945506571482613964425E2))
    
        z = x * z + x
    
        z = select(z + float64x8(0.5 * 6.123233995736765886130E-17), z, flag == int32x8(2))
        z = select(z + float64x8(6.123233995736765886130E-17), z, flag == int32x8(1))
    
        y = y + z
        return y * sign


    code = int32x8(0)
    code = select(int32x8(2), code, x < float64x8(0))
    code = select(code | int32x8(1), code, y < float64x8(0))

    w = select(float64x8(3.14159265358979323846), float64x8(0), code == int32x8(2))
    w = select(float64x8(-3.14159265358979323846), w, code == int32x8(3))

    z = w + _atan(y/x)

    v1 = select(float64x8(1.57079632679489661923), float64x8(-1.57079632679489661923), (code & int32x8(1)) == int32x8(0))
    z = select(v1, z, x == float64x8(0.0))

    v1 = select(float64x8(0.0), float64x8(3.14159265358979323846), (code & int32x8(2)) == int32x8(0))
    z = select(v1, z, y == float64x8(0.0))

    return z
"""

register_kernel('atan2', (('y', float64x8()), ('x', float64x8())), atan2_f64x8, optimize=True)


atan2_f32 = """
def atan2(y: float32, x: float32) -> float32:

    def _atan(x: float32) -> float32:
    
        sign = float32(1.0)
        if x < 0:
            x = -x
            sign = float32(-1.0)
    
        if x > 2.414213562373095:
            y = float32(1.5707963267948966192)
            x = float32(-1.0) / x
        elif x > 0.4142135623730950:
            y = float32(0.7853981633974483096)
            x = (x - 1.0) / (x + 1.0)
        else:
            y = float32(0.0)
    
        z = x * x
        
        y += ((( 8.05374449538e-2 * z - 1.38776856032E-1) * z + 1.99777106478E-1) * z - 3.33329491539E-1) * z * x + x
        if sign < 0:
            y = -y
    
        return y


    code = 0
    if x < 0:
        code = 2
    if y < 0:
        code |= 1

    if x == 0.0:
        if code & 1:
            return float32(-1.5707963267948966192)
        if y == 0.0:
            return float32(0.0)
        return float32(1.5707963267948966192)

    if y == 0.0:
        if code & 2:
            return float32(3.141592653589793238)
        return float32(0.0)

    if code == 2:
        w = float32(3.141592653589793238)
    elif code == 3:
        w = float32(-3.141592653589793238)
    else:
        w = float32(0.0)

    z = w + _atan(y/x)
    return z
"""

register_kernel('atan2', (('y', float32()), ('x', float32())), atan2_f32, optimize=True)

atan2_f32x2 = """
def atan2(y: float32x2, x: float32x2) -> float32x2:

    def _atan(x: float32x2) -> float32x2:
         
        sign = copysign(float32x2(1.0), x)
        x = abs(x)
    
        mask1 = x > float32x2(2.414213562373095)
        mask2 = x > float32x2(0.4142135623730950)
        
        y = select(float32x2(1.5707963267948966192), select(float32x2(0.7853981633974483096), float32x2(0.0), mask2), mask1)
        x = select(float32x2(-1.0) / x, select((x - float32x2(1.0)) / (x + float32x2(1.0)), x, mask2), mask1)
        
        z = x * x
        y += (((8.05374449538e-2 * z - float32x2(1.38776856032E-1)) * z + float32x2(1.99777106478E-1)) * z - float32x2(3.33329491539E-1)) * z * x + x
        return y * sign

    code = int32x2(0)
    code = select(int32x2(2), code, x < float32x2(0))
    code = select(code | int32x2(1), code, y < float32x2(0))
    
    w = select(float32x2(3.141592653589793238), float32x2(0), code == int32x2(2))
    w = select(float32x2(-3.141592653589793238), w, code == int32x2(3))
    
    z = w + _atan(y/x)
    
    v1 = select(float32x2(1.5707963267948966192), float32x2(-1.5707963267948966192), (code & int32x2(1)) == int32x2(0))
    z = select(v1, z, x == float32x2(0.0))
    
    v1 = select(float32x2(0.0), float32x2(3.141592653589793238), (code & int32x2(2)) == int32x2(0))
    z = select(v1, z, y == float32x2(0.0))

    return z
"""

register_kernel('atan2', (('y', float32x2()), ('x', float32x2())), atan2_f32x2, optimize=True)


atan2_f32x3 = """
def atan2(y: float32x3, x: float32x3) -> float32x3:

    def _atan(x: float32x3) -> float32x3:
    
        sign = copysign(float32x3(1.0), x)
        x = abs(x)
    
        mask1 = x > float32x3(2.414213562373095)
        mask2 = x > float32x3(0.4142135623730950)
    
        y = select(float32x3(1.5707963267948966192), select(float32x3(0.7853981633974483096), float32x3(0.0), mask2), mask1)
        x = select(float32x3(-1.0) / x, select((x - float32x3(1.0)) / (x + float32x3(1.0)), x, mask2), mask1)
    
        z = x * x
        y += (((8.05374449538e-2 * z - float32x3(1.38776856032E-1)) * z + float32x3(1.99777106478E-1)) * z - float32x3(3.33329491539E-1)) * z * x + x
        return y * sign


    code = int32x3(0)
    code = select(int32x3(2), code, x < float32x3(0))
    code = select(code | int32x3(1), code, y < float32x3(0))

    w = select(float32x3(3.141592653589793238), float32x3(0), code == int32x3(2))
    w = select(float32x3(-3.141592653589793238), w, code == int32x3(3))

    z = w + _atan(y/x)

    v1 = select(float32x3(1.5707963267948966192), float32x3(-1.5707963267948966192), (code & int32x3(1)) == int32x3(0))
    z = select(v1, z, x == float32x3(0.0))

    v1 = select(float32x3(0.0), float32x3(3.141592653589793238), (code & int32x3(2)) == int32x3(0))
    z = select(v1, z, y == float32x3(0.0))

    return z
"""

register_kernel('atan2', (('y', float32x3()), ('x', float32x3())), atan2_f32x3, optimize=True)


atan2_f32x4 = """
def atan2(y: float32x4, x: float32x4) -> float32x4:

    def _atan(x: float32x4) -> float32x4:
    
        sign = copysign(float32x4(1.0), x)
        x = abs(x)
    
        mask1 = x > float32x4(2.414213562373095)
        mask2 = x > float32x4(0.4142135623730950)
    
        y = select(float32x4(1.5707963267948966192), select(float32x4(0.7853981633974483096), float32x4(0.0), mask2), mask1)
        x = select(float32x4(-1.0) / x, select((x - float32x4(1.0)) / (x + float32x4(1.0)), x, mask2), mask1)
    
        z = x * x
        y += (((8.05374449538e-2 * z - float32x4(1.38776856032E-1)) * z + float32x4(1.99777106478E-1)) * z - float32x4(3.33329491539E-1)) * z * x + x
        return y * sign


    code = int32x4(0)
    code = select(int32x4(2), code, x < float32x4(0))
    code = select(code | int32x4(1), code, y < float32x4(0))

    w = select(float32x4(3.141592653589793238), float32x4(0), code == int32x4(2))
    w = select(float32x4(-3.141592653589793238), w, code == int32x4(3))

    z = w + _atan(y/x)

    v1 = select(float32x4(1.5707963267948966192), float32x4(-1.5707963267948966192), (code & int32x4(1)) == int32x4(0))
    z = select(v1, z, x == float32x4(0.0))

    v1 = select(float32x4(0.0), float32x4(3.141592653589793238), (code & int32x4(2)) == int32x4(0))
    z = select(v1, z, y == float32x4(0.0))

    return z
"""

register_kernel('atan2', (('y', float32x4()), ('x', float32x4())), atan2_f32x4, optimize=True)


atan2_f32x8 = """
def atan2(y: float32x8, x: float32x8) -> float32x8:

    def _atan(x: float32x8) -> float32x8:
    
        sign = copysign(float32x8(1.0), x)
        x = abs(x)
    
        mask1 = x > float32x8(2.414213562373095)
        mask2 = x > float32x8(0.4142135623730950)
    
        y = select(float32x8(1.5707963267948966192), select(float32x8(0.7853981633974483096), float32x8(0.0), mask2), mask1)
        x = select(float32x8(-1.0) / x, select((x - float32x8(1.0)) / (x + float32x8(1.0)), x, mask2), mask1)
    
        z = x * x
        y += (((8.05374449538e-2 * z - float32x8(1.38776856032E-1)) * z + float32x8(1.99777106478E-1)) * z - float32x8(3.33329491539E-1)) * z * x + x
        return y * sign
    

    code = int32x8(0)
    code = select(int32x8(2), code, x < float32x8(0))
    code = select(code | int32x8(1), code, y < float32x8(0))

    w = select(float32x8(3.141592653589793238), float32x8(0), code == int32x8(2))
    w = select(float32x8(-3.141592653589793238), w, code == int32x8(3))

    z = w + _atan(y/x)

    v1 = select(float32x8(1.5707963267948966192), float32x8(-1.5707963267948966192), (code & int32x8(1)) == int32x8(0))
    z = select(v1, z, x == float32x8(0.0))

    v1 = select(float32x8(0.0), float32x8(3.141592653589793238), (code & int32x8(2)) == int32x8(0))
    z = select(v1, z, y == float32x8(0.0))

    return z
"""

register_kernel('atan2', (('y', float32x8()), ('x', float32x8())), atan2_f32x8, optimize=True)


atan2_f32x16 = """
def atan2(y: float32x16, x: float32x16) -> float32x16:

    def _atan(x: float32x16) -> float32x16:
    
        sign = copysign(float32x16(1.0), x)
        x = abs(x)
    
        mask1 = x > float32x16(2.414213562373095)
        mask2 = x > float32x16(0.4142135623730950)
    
        y = select(float32x16(1.5707963267948966192), select(float32x16(0.7853981633974483096), float32x16(0.0), mask2), mask1)
        x = select(float32x16(-1.0) / x, select((x - float32x16(1.0)) / (x + float32x16(1.0)), x, mask2), mask1)
    
        z = x * x
        y += (((8.05374449538e-2 * z - float32x16(1.38776856032E-1)) * z + float32x16(1.99777106478E-1)) * z - float32x16(3.33329491539E-1)) * z * x + x
        return y * sign


    code = int32x16(0)
    code = select(int32x16(2), code, x < float32x16(0))
    code = select(code | int32x16(1), code, y < float32x16(0))

    w = select(float32x16(3.141592653589793238), float32x16(0), code == int32x16(2))
    w = select(float32x16(-3.141592653589793238), w, code == int32x16(3))

    z = w + _atan(y/x)

    v1 = select(float32x16(1.5707963267948966192), float32x16(-1.5707963267948966192), (code & int32x16(1)) == int32x16(0))
    z = select(v1, z, x == float32x16(0.0))

    v1 = select(float32x16(0.0), float32x16(3.141592653589793238), (code & int32x16(2)) == int32x16(0))
    z = select(v1, z, y == float32x16(0.0))

    return z
"""

register_kernel('atan2', (('y', float32x16()), ('x', float32x16())), atan2_f32x16, optimize=True)
