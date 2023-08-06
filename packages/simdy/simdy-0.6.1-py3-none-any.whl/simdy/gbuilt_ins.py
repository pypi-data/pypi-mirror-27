
from .dbl_arg import float64
from .cgen import register_kernel


sinus_f64 = """
def sinus(x: float64) -> float64:
    sign = copysign(1.0, x)
    x = abs(x)
    y = floor(x * 1.2732395447351628)

    z = y - ((y >> 4) << 4)

    if z & 1:
        z += 1
        y += 1

    z = z & 7
    if z > 3:
        sign = sign * -1.0
        z = z - 4

    yd = float64(y)
    zd = ((x - yd * 7.85398125648498535156E-1) - yd * 3.77489470793079817668E-8) - yd * 2.69515142907905952645E-15
    zz = zd * zd

    if z == 1 or z == 2:
        val = qhorner(zz,
                     -1.13585365213876817300E-11, 2.08757008419747316778E-9, -2.75573141792967388112E-7,
                     2.48015872888517045348E-5, -1.38888888888730564116E-3, 4.16666666666665929218E-2, -0.5, 1.0)
    else:
        val = zd * qhorner(zz, 1.58962301576546568060E-10, -2.50507477628578072866E-8, 2.75573136213857245213E-6,
                        -1.98412698295895385996E-4, 8.33333333332211858878E-3, -1.66666666666666307295E-1, 1.0)

    if sign < 0.0:
        val = val * -1.0
    return val
"""
register_kernel('sinus', (('x', float64()),), sinus_f64)
