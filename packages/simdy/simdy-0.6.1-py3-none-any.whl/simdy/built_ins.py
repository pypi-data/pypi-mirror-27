
from .holders import Name, Const
from .cgen import register_built_in
from .int_arg import Int32Arg, Int64Arg, int32, int64
from .flt_arg import Float32Arg, float32
from .dbl_arg import Float64Arg, float64
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8,\
    Float64x4Arg, Float64x2Arg, Float64x3Arg, Float64x8Arg
from .flt_vec_arg import float32x2, float32x3, float32x4, float32x8, float32x16,\
    Float32x2Arg, Float32x3Arg, Float32x4Arg, Float32x8Arg, Float32x16Arg
from .int_vec_arg import int32x2, int32x3, int32x4, int32x8, int32x16, int64x2,\
    int64x3, int64x4, int64x8, Int32x4Arg, Int64x4Arg, Int64x2Arg, Int32x3Arg,\
    Int32x2Arg, Int32x8Arg, Int32x16Arg, Int64x3Arg, Int64x8Arg
from .arr import stack_array, ArrayArg, StackedArrayArg
from .ptr import PointerArg
from .util import generate_name
from .usr_typ import get_user_type_factory


__all__ = []


def abs_i32(cgen, reg):
    # tmp = cgen.register('xmm')
    # code = 'movd %s, %s\n' % (tmp, reg)
    # code += "vpabsd %s, %s\n" % (tmp, tmp)
    # code += 'movd %s, %s\n' % (reg, tmp)
    # cgen.release_reg(tmp)
    # return code, reg, Int32Arg
    #
    reg2 = cgen.register('general')
    code = 'mov %s, %s\n' % (reg2, reg)
    code += 'neg %s\n' % reg
    code += 'cmovl %s, %s\n' % (reg, reg2)
    cgen.release_reg(reg2)
    return code, reg, Int32Arg


def abs_i64(cgen, reg):
    reg2 = cgen.register('general64')
    code = 'mov %s, %s\n' % (reg2, reg)
    code += 'neg %s\n' % reg
    code += 'cmovl %s, %s\n' % (reg, reg2)
    cgen.release_reg(reg2)
    return code, reg, Int64Arg


def abs_f32(cgen, xmm):
    tmp_xmm = cgen.register('xmm')
    code = cgen.gen.abs_f32(xmm, tmp_xmm)
    cgen.release_reg(tmp_xmm)
    return code, xmm, Float32Arg


def abs_f64(cgen, xmm):
    tmp_xmm = cgen.register('xmm')
    code = cgen.gen.abs_f64(xmm, tmp_xmm)
    cgen.release_reg(tmp_xmm)
    return code, xmm, Float64Arg


def abs_f64x2(cgen, xmm):
    tmp_xmm = cgen.register('xmm')
    code = cgen.gen.abs_f64x2(xmm, tmp_xmm)
    cgen.release_reg(tmp_xmm)
    return code, xmm, Float64x2Arg


def abs_f64x3(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        tmp_ymm = cgen.register('ymm')
        code = cgen.gen.abs_f64x3(reg, tmp_ymm)
        cgen.release_reg(tmp_ymm)
        return code, reg, Float64x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        tmp_xmm = cgen.register('xmm')
        code = cgen.gen.abs_f64x2_x2(xmm1, xmm2, tmp_xmm, reg)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2), Float64x3Arg


def abs_f64x4(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        tmp_ymm = cgen.register('ymm')
        code = cgen.gen.abs_f64x4(reg, tmp_ymm)
        cgen.release_reg(tmp_ymm)
        return code, reg, Float64x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        tmp_xmm = cgen.register('xmm')
        code = cgen.gen.abs_f64x2_x2(xmm1, xmm2, tmp_xmm, reg)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2), Float64x4Arg


def abs_f64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        code = 'vpsllq %s, %s, 1\n' % (reg, reg)
        code += 'vpsrlq %s, %s, 1\n' % (reg, reg)
        return code, reg, Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        tmp_ymm = cgen.register('ymm')
        code = cgen.gen.abs_f64x4_x2(ymm1, ymm2, tmp_ymm, reg)
        cgen.release_reg(tmp_ymm)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        tmp_xmm = cgen.register('xmm')
        code = cgen.gen.abs_f64x2_x4(xmm1, xmm2, xmm3, xmm4, tmp_xmm, reg)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def abs_f32x4(cgen, xmm, ret_type):
    tmp_xmm = cgen.register('xmm')
    code = cgen.gen.abs_f32x4(xmm, tmp_xmm)
    cgen.release_reg(tmp_xmm)
    return code, xmm, ret_type


def abs_f32x8(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        tmp_ymm = cgen.register('ymm')
        code = cgen.gen.abs_f32x8(reg, tmp_ymm)
        cgen.release_reg(tmp_ymm)
        return code, reg, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        tmp_xmm = cgen.register('xmm')
        code = cgen.gen.abs_f32x4_x2(xmm1, xmm2, tmp_xmm, reg)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2), Float32x8Arg


def abs_f32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        code = 'vpslld %s, %s, 1\n' % (reg, reg)
        code += 'vpsrld %s, %s, 1\n' % (reg, reg)
        return code, reg, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        tmp_ymm = cgen.register('ymm')
        code = cgen.gen.abs_f32x8_x2(ymm1, ymm2, tmp_ymm, reg)
        cgen.release_reg(tmp_ymm)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        tmp_xmm = cgen.register('xmm')
        code = cgen.gen.abs_f32x4_x4(xmm1, xmm2, xmm3, xmm4, tmp_xmm, reg)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def abs_i32x4(cgen, xmm, ret_type):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpabsd %s, %s\n' % (xmm, xmm)
    else:
        code = 'pabsd %s, %s\n' % (xmm, xmm)
    return code, xmm, ret_type


def abs_i32x8(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        code = 'vpabsd %s, %s\n' % (reg, reg)
        return code, reg, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vpabsd %s, oword [%s]\n' % (xmm1, reg)
        code += 'vpabsd %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pabsd %s, oword [%s]\n' % (xmm1, reg)
        code += 'pabsd %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int32x8Arg


def abs_i32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        code = 'vpabsd %s, %s\n' % (reg, reg)
        return code, reg, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vpabsd %s, yword [%s]\n' % (ymm1, reg)
        code += 'vpabsd %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vpabsd %s, oword [%s]\n' % (xmm1, reg)
        code += 'vpabsd %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'vpabsd %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'vpabsd %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pabsd %s, oword [%s]\n' % (xmm1, reg)
        code += 'pabsd %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'pabsd %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'pabsd %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


register_built_in('abs', (Int32Arg,), abs_i32)
register_built_in('abs', (Int64Arg,), abs_i64)
register_built_in('abs', (Float32Arg,), abs_f32)
register_built_in('abs', (Float64Arg,), abs_f64)
register_built_in('abs', (Float64x2Arg,), abs_f64x2)
register_built_in('abs', (Float64x3Arg,), abs_f64x3)
register_built_in('abs', (Float64x4Arg,), abs_f64x4)
register_built_in('abs', (Float64x8Arg,), abs_f64x8)

register_built_in('abs', (Float32x2Arg,), lambda cgen, xmm1: abs_f32x4(cgen, xmm1, Float32x2Arg))
register_built_in('abs', (Float32x3Arg,), lambda cgen, xmm1: abs_f32x4(cgen, xmm1, Float32x3Arg))
register_built_in('abs', (Float32x4Arg,), lambda cgen, xmm1: abs_f32x4(cgen, xmm1, Float32x4Arg))
register_built_in('abs', (Float32x8Arg,), abs_f32x8)
register_built_in('abs', (Float32x16Arg,), abs_f32x16)

register_built_in('abs', (Int32x2Arg,), lambda cgen, xmm1: abs_i32x4(cgen, xmm1, Int32x2Arg))
register_built_in('abs', (Int32x3Arg,), lambda cgen, xmm1: abs_i32x4(cgen, xmm1, Int32x3Arg))
register_built_in('abs', (Int32x4Arg,), lambda cgen, xmm1: abs_i32x4(cgen, xmm1, Int32x4Arg))
register_built_in('abs', (Int32x8Arg,), abs_i32x8)
register_built_in('abs', (Int32x16Arg,), abs_i32x16)


def copysign_f64x2_f64x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        code = 'vpsllq %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrlq %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrlq %s, %s, 63\n' % (xmm2, xmm2)
        code += 'vpsllq %s, %s, 63\n' % (xmm2, xmm2)
        code += 'vorpd %s, %s, %s\n' % (xmm1, xmm1, xmm2)
        return code, xmm1, Float64x2Arg

    xmm3 = cgen.register('xmm')
    code = cgen.gen.copysign_f64x2(xmm1, xmm2, xmm3)
    cgen.release_reg(xmm3)
    return code, xmm2, Float64x2Arg


def copysign_f64x3_f64x3(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        code = 'vpsllq %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrlq %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrlq %s, %s, 63\n' % (reg2, reg2)
        code += 'vpsllq %s, %s, 63\n' % (reg2, reg2)
        code += 'vorpd %s, %s, %s\n' % (reg1, reg1, reg2)
        return code, reg1, Float64x3Arg


    if cgen.cpu.AVX:
        ymm3 = cgen.register('ymm')
        code = cgen.gen.copysign_f64x4(reg1, reg2, ymm3)
        cgen.release_reg(ymm3)
        return code, reg2, Float64x3Arg
    else:
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        xmm5, xmm6 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm4, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm4, xmm6)
        code += 'movsd %s, qword [%s + 16]\n' % (xmm3, reg1)
        code += 'movsd %s, qword [%s + 16]\n' % (xmm5, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm5, xmm6)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm6)
        return code, (xmm4, xmm5), Float64x3Arg


def copysign_f64x4_f64x4(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        code = 'vpsllq %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrlq %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrlq %s, %s, 63\n' % (reg2, reg2)
        code += 'vpsllq %s, %s, 63\n' % (reg2, reg2)
        code += 'vorpd %s, %s, %s\n' % (reg1, reg1, reg2)
        return code, reg1, Float64x4Arg

    if cgen.cpu.AVX:
        ymm3 = cgen.register('ymm')
        code = cgen.gen.copysign_f64x4(reg1, reg2, ymm3)
        cgen.release_reg(ymm3)
        return code, reg2, Float64x4Arg
    else:
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        xmm5, xmm6 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm4, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm4, xmm6)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm5, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm5, xmm6)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm6)
        return code, (xmm4, xmm5), Float64x4Arg


def copysign_f64x8_f64x8(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        code = 'vpsllq %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrlq %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrlq %s, %s, 63\n' % (reg2, reg2)
        code += 'vpsllq %s, %s, 63\n' % (reg2, reg2)
        code += 'vorpd %s, %s, %s\n' % (reg1, reg1, reg2)
        return code, reg1, Float64x8Arg

    if cgen.cpu.AVX:
        ymm3, ymm4 = cgen.register('ymm'), cgen.register('ymm')
        ymm5, ymm6 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm3, reg1)
        code += 'vmovaps %s, yword [%s]\n' % (ymm4, reg2)
        code += cgen.gen.copysign_f64x4(ymm3, ymm4, ymm6)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm3, reg1)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm5, reg2)
        code += cgen.gen.copysign_f64x4(ymm3, ymm5, ymm6)
        cgen.release_reg(ymm3)
        cgen.release_reg(ymm6)
        return code, (ymm4, ymm5), Float64x8Arg
    else:
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        xmm5, xmm6 = cgen.register('xmm'), cgen.register('xmm')
        xmm7, xmm8 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm4, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm4, xmm8)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm5, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm5, xmm8)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm6, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm6, xmm8)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm7, reg2)
        code += cgen.gen.copysign_f64x2(xmm3, xmm7, xmm8)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm8)
        return code, (xmm4, xmm5, xmm6, xmm7), Float64x8Arg


def copysign_f32x2_f32x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        code = 'vpslld %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrld %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrld %s, %s, 31\n' % (xmm2, xmm2)
        code += 'vpslld %s, %s, 31\n' % (xmm2, xmm2)
        code += 'vorps %s, %s, %s\n' % (xmm1, xmm1, xmm2)
        return code, xmm1, Float32x2Arg

    xmm3 = cgen.register('xmm')
    code = cgen.gen.copysign_f32x4(xmm1, xmm2, xmm3)
    cgen.release_reg(xmm3)
    return code, xmm2, Float32x2Arg


def copysign_f32x3_f32x3(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        code = 'vpslld %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrld %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrld %s, %s, 31\n' % (xmm2, xmm2)
        code += 'vpslld %s, %s, 31\n' % (xmm2, xmm2)
        code += 'vorps %s, %s, %s\n' % (xmm1, xmm1, xmm2)
        return code, xmm1, Float32x3Arg

    xmm3 = cgen.register('xmm')
    code = cgen.gen.copysign_f32x4(xmm1, xmm2, xmm3)
    cgen.release_reg(xmm3)
    return code, xmm2, Float32x3Arg


def copysign_f32x4_f32x4(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        code = 'vpslld %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrld %s, %s, 1\n' % (xmm1, xmm1)
        code += 'vpsrld %s, %s, 31\n' % (xmm2, xmm2)
        code += 'vpslld %s, %s, 31\n' % (xmm2, xmm2)
        code += 'vorps %s, %s, %s\n' % (xmm1, xmm1, xmm2)
        return code, xmm1, Float32x4Arg

    xmm3 = cgen.register('xmm')
    code = cgen.gen.copysign_f32x4(xmm1, xmm2, xmm3)
    cgen.release_reg(xmm3)
    return code, xmm2, Float32x4Arg


def copysign_f32x8_f32x8(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        code = 'vpslld %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrld %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrld %s, %s, 31\n' % (reg2, reg2)
        code += 'vpslld %s, %s, 31\n' % (reg2, reg2)
        code += 'vorps %s, %s, %s\n' % (reg1, reg1, reg2)
        return code, reg1, Float32x8Arg

    if cgen.cpu.AVX:
        ymm3 = cgen.register('ymm')
        code = cgen.gen.copysign_f32x8(reg1, reg2, ymm3)
        cgen.release_reg(ymm3)
        return code, reg2, Float32x8Arg
    else:
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        xmm5, xmm6 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm4, reg2)
        code += cgen.gen.copysign_f32x4(xmm3, xmm4, xmm6)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm5, reg2)
        code += cgen.gen.copysign_f32x4(xmm3, xmm5, xmm6)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm6)
        return code, (xmm4, xmm5), Float32x8Arg


def copysign_f32x16_f32x16(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        code = 'vpslld %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrld %s, %s, 1\n' % (reg1, reg1)
        code += 'vpsrld %s, %s, 31\n' % (reg2, reg2)
        code += 'vpslld %s, %s, 31\n' % (reg2, reg2)
        code += 'vorps %s, %s, %s\n' % (reg1, reg1, reg2)
        return code, reg1, Float32x16Arg

    if cgen.cpu.AVX:
        ymm3, ymm4 = cgen.register('ymm'), cgen.register('ymm')
        ymm5, ymm6 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm3, reg1)
        code += 'vmovaps %s, yword [%s]\n' % (ymm4, reg2)
        code += cgen.gen.copysign_f32x8(ymm3, ymm4, ymm6)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm3, reg1)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm5, reg2)
        code += cgen.gen.copysign_f32x8(ymm3, ymm5, ymm6)
        cgen.release_reg(ymm3)
        cgen.release_reg(ymm6)
        return code, (ymm4, ymm5), Float32x16Arg
    else:
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        xmm5, xmm6 = cgen.register('xmm'), cgen.register('xmm')
        xmm7, xmm8 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm4, reg2)
        code += cgen.gen.copysign_f32x4(xmm3, xmm4, xmm8)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm5, reg2)
        code += cgen.gen.copysign_f32x4(xmm3, xmm5, xmm8)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm6, reg2)
        code += cgen.gen.copysign_f32x4(xmm3, xmm6, xmm8)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm3, reg1)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm7, reg2)
        code += cgen.gen.copysign_f32x4(xmm3, xmm7, xmm8)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm8)
        return code, (xmm4, xmm5, xmm6, xmm7), Float32x16Arg


register_built_in('copysign', (Float64x2Arg, Float64x2Arg), copysign_f64x2_f64x2)
register_built_in('copysign', (Float64x3Arg, Float64x3Arg), copysign_f64x3_f64x3)
register_built_in('copysign', (Float64x4Arg, Float64x4Arg), copysign_f64x4_f64x4)
register_built_in('copysign', (Float64x8Arg, Float64x8Arg), copysign_f64x8_f64x8)
register_built_in('copysign', (Float32x2Arg, Float32x2Arg), copysign_f32x2_f32x2)
register_built_in('copysign', (Float32x3Arg, Float32x3Arg), copysign_f32x3_f32x3)
register_built_in('copysign', (Float32x4Arg, Float32x4Arg), copysign_f32x4_f32x4)
register_built_in('copysign', (Float32x8Arg, Float32x8Arg), copysign_f32x8_f32x8)
register_built_in('copysign', (Float32x16Arg, Float32x16Arg), copysign_f32x16_f32x16)


def round_f64(cgen, xmm, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscalesd %s, %s, %s, %i\n' % (xmm, xmm, xmm, ctrl)
    elif cgen.cpu.AVX:
        code = 'vroundsd %s, %s, %s, %i\n' % (xmm, xmm, xmm, ctrl)
    else:
        code = 'roundsd %s, %s, %i\n' % (xmm, xmm, ctrl)
    return code, xmm, Float64Arg


def round_f32(cgen, xmm, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscaless %s, %s, %s, %i\n' % (xmm, xmm, xmm, ctrl)
    elif cgen.cpu.AVX:
        code = 'vroundss %s, %s, %s, %i\n' % (xmm, xmm, xmm, ctrl)
    else:
        code = 'roundss %s, %s, %i\n' % (xmm, xmm, ctrl)
    return code, xmm, Float32Arg


def round_f64x2(cgen, xmm, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscalepd %s, %s, %i\n' % (xmm, xmm, ctrl)
    elif cgen.cpu.AVX:
        code = 'vroundpd %s, %s, %i\n' % (xmm, xmm, ctrl)
    else:
        code = 'roundpd %s, %s, %i\n' % (xmm, xmm, ctrl)
    return code, xmm, Float64x2Arg


def round_f64x3(cgen, reg, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscalepd %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float64x3Arg
    elif cgen.cpu.AVX:
        code = 'vroundpd %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float64x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'roundpd %s, oword [%s], %i\n' % (xmm1, reg, ctrl)
        code += 'roundsd %s, qword [%s + 16], %i\n' % (xmm2, reg, ctrl)
        return code, (xmm1, xmm2), Float64x3Arg


def round_f64x4(cgen, reg, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscalepd %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float64x4Arg
    if cgen.cpu.AVX:
        code = 'vroundpd %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float64x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'roundpd %s, oword [%s], %i\n' % (xmm1, reg, ctrl)
        code += 'roundpd %s, oword [%s + 16], %i\n' % (xmm2, reg, ctrl)
        return code, (xmm1, xmm2), Float64x4Arg


def round_f64x8(cgen, reg, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscalepd %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float64x8Arg
    if cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vroundpd %s, yword [%s], %i\n' % (ymm1, reg, ctrl)
        code += 'vroundpd %s, yword [%s + 32], %i\n' % (ymm2, reg, ctrl)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'roundpd %s, oword [%s], %i\n' % (xmm1, reg, ctrl)
        code += 'roundpd %s, oword [%s + 16], %i\n' % (xmm2, reg, ctrl)
        code += 'roundpd %s, oword [%s + 32], %i\n' % (xmm3, reg, ctrl)
        code += 'roundpd %s, oword [%s + 48], %i\n' % (xmm4, reg, ctrl)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def round_f32x2(cgen, xmm, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscaleps %s, %s, %i\n' % (xmm, xmm, ctrl)
    elif cgen.cpu.AVX:
        code = 'vroundps %s, %s, %i\n' % (xmm, xmm, ctrl)
    else:
        code = 'roundps %s, %s, %i\n' % (xmm, xmm, ctrl)
    return code, xmm, Float32x2Arg


def round_f32x3(cgen, xmm, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscaleps %s, %s, %i\n' % (xmm, xmm, ctrl)
    elif cgen.cpu.AVX:
        code = 'vroundps %s, %s, %i\n' % (xmm, xmm, ctrl)
    else:
        code = 'roundps %s, %s, %i\n' % (xmm, xmm, ctrl)
    return code, xmm, Float32x3Arg


def round_f32x4(cgen, xmm, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscaleps %s, %s, %i\n' % (xmm, xmm, ctrl)
    elif cgen.cpu.AVX:
        code = 'vroundps %s, %s, %i\n' % (xmm, xmm, ctrl)
    else:
        code = 'roundps %s, %s, %i\n' % (xmm, xmm, ctrl)
    return code, xmm, Float32x4Arg


def round_f32x8(cgen, reg, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscaleps %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float32x8Arg
    elif cgen.cpu.AVX:
        code = 'vroundps %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'roundps %s, oword [%s], %i\n' % (xmm1, reg, ctrl)
        code += 'roundps %s, oword [%s + 16], %i\n' % (xmm2, reg, ctrl)
        return code, (xmm1, xmm2), Float32x8Arg


def round_f32x16(cgen, reg, ctrl):
    if cgen.cpu.AVX512F:
        code = 'vrndscaleps %s, %s, %i\n' % (reg, reg, ctrl)
        return code, reg, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vroundps %s, yword [%s], %i\n' % (ymm1, reg, ctrl)
        code += 'vroundps %s, yword [%s + 32], %i\n' % (ymm2, reg, ctrl)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'roundps %s, oword [%s], %i\n' % (xmm1, reg, ctrl)
        code += 'roundps %s, oword [%s + 16], %i\n' % (xmm2, reg, ctrl)
        code += 'roundps %s, oword [%s + 32], %i\n' % (xmm3, reg, ctrl)
        code += 'roundps %s, oword [%s + 48], %i\n' % (xmm4, reg, ctrl)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def round_name(cgen, op_name, ctrl):
    arg = cgen.get_arg(op_name)
    if isinstance(arg, Float32Arg):
        dst_reg = cgen.register("xmm")
        if cgen.cpu.AVX512F:
            code = 'vrndscaless %s, %s, dword [%s], %i\n' % (dst_reg, dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            code = 'vroundss %s, %s, dword [%s], %i\n' % (dst_reg, dst_reg, arg.name, ctrl)
        else:
            code = 'roundss %s, dword [%s], %i\n' % (dst_reg, arg.name, ctrl)
    elif isinstance(arg, Float64Arg):
        dst_reg = cgen.register("xmm")
        if cgen.cpu.AVX512F:
            code = 'vrndscalesd %s, %s, qword [%s], %i\n' % (dst_reg, dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            code = 'vroundsd %s, %s, qword [%s], %i\n' % (dst_reg, dst_reg, arg.name, ctrl)
        else:
            code = 'roundsd %s, qword [%s], %i\n' % (dst_reg, arg.name, ctrl)
    elif isinstance(arg, Float64x2Arg):
        dst_reg = cgen.register("xmm")
        if cgen.cpu.AVX512F:
            code = 'vrndscalepd %s, oword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            code = 'vroundpd %s, oword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        else:
            code = 'roundpd %s, oword [%s], %i\n' % (dst_reg, arg.name, ctrl)
    elif isinstance(arg, (Float64x3Arg, Float64x4Arg)):
        if cgen.cpu.AVX512F:
            dst_reg = cgen.register("ymm")
            code = 'vrndscalepd %s, yword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            dst_reg = cgen.register("ymm")
            code = 'vroundpd %s, yword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'roundpd %s, oword [%s], %i\n' % (dst_reg[0], arg.name, ctrl)
            code += 'roundpd %s, oword [%s + 16], %i\n' % (dst_reg[1], arg.name, ctrl)
    elif isinstance(arg, Float64x8Arg):
        if cgen.cpu.AVX512F:
            dst_reg = cgen.register("zmm")
            code = 'vrndscalepd %s, zword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            dst_reg = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vroundpd %s, yword [%s], %i\n' % (dst_reg[0], arg.name, ctrl)
            code += 'vroundpd %s, yword [%s + 32], %i\n' % (dst_reg[1], arg.name, ctrl)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
            code = 'roundpd %s, oword [%s], %i\n' % (dst_reg[0], arg.name, ctrl)
            code += 'roundpd %s, oword [%s + 16], %i\n' % (dst_reg[1], arg.name, ctrl)
            code += 'roundpd %s, oword [%s + 32], %i\n' % (dst_reg[2], arg.name, ctrl)
            code += 'roundpd %s, oword [%s + 48], %i\n' % (dst_reg[3], arg.name, ctrl)
    elif isinstance(arg, (Float32x2Arg, Float32x3Arg, Float32x4Arg)):
        dst_reg = cgen.register("xmm")
        if cgen.cpu.AVX512F:
            code = 'vrndscaleps %s, oword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            code = 'vroundps %s, oword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        else:
            code = 'roundps %s, oword [%s], %i\n' % (dst_reg, arg.name, ctrl)
    elif isinstance(arg, Float32x8Arg):
        if cgen.cpu.AVX512F:
            dst_reg = cgen.register("ymm")
            code = 'vrndscaleps %s, yword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            dst_reg = cgen.register("ymm")
            code = 'vroundps %s, yword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'roundps %s, oword [%s], %i\n' % (dst_reg[0], arg.name, ctrl)
            code += 'roundps %s, oword [%s + 16], %i\n' % (dst_reg[1], arg.name, ctrl)
    elif isinstance(arg, Float32x16Arg):
        if cgen.cpu.AVX512F:
            dst_reg = cgen.register("zmm")
            code = 'vrndscaleps %s, zword [%s], %i\n' % (dst_reg, arg.name, ctrl)
        elif cgen.cpu.AVX:
            dst_reg = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vroundps %s, yword [%s], %i\n' % (dst_reg[0], arg.name, ctrl)
            code += 'vroundps %s, yword [%s + 32], %i\n' % (dst_reg[1], arg.name, ctrl)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
            code = 'roundps %s, oword [%s], %i\n' % (dst_reg[0], arg.name, ctrl)
            code += 'roundps %s, oword [%s + 16], %i\n' % (dst_reg[1], arg.name, ctrl)
            code += 'roundps %s, oword [%s + 32], %i\n' % (dst_reg[2], arg.name, ctrl)
            code += 'roundps %s, oword [%s + 48], %i\n' % (dst_reg[3], arg.name, ctrl)
    else:
        raise TypeError("Callable round/ceil/floor doesn't support argument ", arg, op_name.name)
    return code, dst_reg, type(arg)


register_built_in('round', (Float64Arg,), lambda cgen, xmm: round_f64(cgen, xmm, 0))
register_built_in('floor', (Float64Arg,), lambda cgen, xmm: round_f64(cgen, xmm, 1))
register_built_in('ceil', (Float64Arg,), lambda cgen, xmm: round_f64(cgen, xmm, 2))
register_built_in('round', (Float32Arg,), lambda cgen, xmm: round_f32(cgen, xmm, 0))
register_built_in('floor', (Float32Arg,), lambda cgen, xmm: round_f32(cgen, xmm, 1))
register_built_in('ceil', (Float32Arg,), lambda cgen, xmm: round_f32(cgen, xmm, 2))
register_built_in('round', (Float64x2Arg,), lambda cgen, xmm: round_f64x2(cgen, xmm, 0))
register_built_in('floor', (Float64x2Arg,), lambda cgen, xmm: round_f64x2(cgen, xmm, 1))
register_built_in('ceil', (Float64x2Arg,), lambda cgen, xmm: round_f64x2(cgen, xmm, 2))
register_built_in('round', (Float64x3Arg,), lambda cgen, reg: round_f64x3(cgen, reg, 0))
register_built_in('floor', (Float64x3Arg,), lambda cgen, reg: round_f64x3(cgen, reg, 1))
register_built_in('ceil', (Float64x3Arg,), lambda cgen, reg: round_f64x3(cgen, reg, 2))
register_built_in('round', (Float64x4Arg,), lambda cgen, reg: round_f64x4(cgen, reg, 0))
register_built_in('floor', (Float64x4Arg,), lambda cgen, reg: round_f64x4(cgen, reg, 1))
register_built_in('ceil', (Float64x4Arg,), lambda cgen, reg: round_f64x4(cgen, reg, 2))
register_built_in('round', (Float64x8Arg,), lambda cgen, reg: round_f64x8(cgen, reg, 0))
register_built_in('floor', (Float64x8Arg,), lambda cgen, reg: round_f64x8(cgen, reg, 1))
register_built_in('ceil', (Float64x8Arg,), lambda cgen, reg: round_f64x8(cgen, reg, 2))
register_built_in('round', (Float32x2Arg,), lambda cgen, xmm: round_f32x2(cgen, xmm, 0))
register_built_in('floor', (Float32x2Arg,), lambda cgen, xmm: round_f32x2(cgen, xmm, 1))
register_built_in('ceil', (Float32x2Arg,), lambda cgen, xmm: round_f32x2(cgen, xmm, 2))
register_built_in('round', (Float32x3Arg,), lambda cgen, xmm: round_f32x3(cgen, xmm, 0))
register_built_in('floor', (Float32x3Arg,), lambda cgen, xmm: round_f32x3(cgen, xmm, 1))
register_built_in('ceil', (Float32x3Arg,), lambda cgen, xmm: round_f32x3(cgen, xmm, 2))
register_built_in('round', (Float32x4Arg,), lambda cgen, xmm: round_f32x4(cgen, xmm, 0))
register_built_in('floor', (Float32x4Arg,), lambda cgen, xmm: round_f32x4(cgen, xmm, 1))
register_built_in('ceil', (Float32x4Arg,), lambda cgen, xmm: round_f32x4(cgen, xmm, 2))
register_built_in('round', (Float32x8Arg,), lambda cgen, xmm: round_f32x8(cgen, xmm, 0))
register_built_in('floor', (Float32x8Arg,), lambda cgen, xmm: round_f32x8(cgen, xmm, 1))
register_built_in('ceil', (Float32x8Arg,), lambda cgen, xmm: round_f32x8(cgen, xmm, 2))
register_built_in('round', (Float32x16Arg,), lambda cgen, xmm: round_f32x16(cgen, xmm, 0))
register_built_in('floor', (Float32x16Arg,), lambda cgen, xmm: round_f32x16(cgen, xmm, 1))
register_built_in('ceil', (Float32x16Arg,), lambda cgen, xmm: round_f32x16(cgen, xmm, 2))
register_built_in('round', (Name,), lambda cgen, name: round_name(cgen, name, 0))
register_built_in('floor', (Name,), lambda cgen, name: round_name(cgen, name, 1))
register_built_in('ceil', (Name,), lambda cgen, name: round_name(cgen, name, 2))


def len_array(cgen, obj):
    ptr_reg, arg = obj
    if not arg.is_pointer():
        raise ValueError("In len callable PointerArg is expected!", arg)
    if isinstance(arg.arg, ArrayArg):
        reg = cgen.register('general64')
        code = "mov %s, qword[%s + Array.size]\n" % (reg, ptr_reg)
        return code, reg, Int64Arg
    elif isinstance(arg.arg, StackedArrayArg):
        reg = cgen.register('general64')
        code = "mov %s, %i\n" % (reg, len(arg.arg.value))
        return code, reg, Int64Arg
    else:
        raise ValueError("Unknown array in len callable!", arg.arg)


register_built_in('len', (PointerArg,), len_array)


def sqrt_name(cgen, op_name):
    arg = cgen.get_arg(op_name)
    if isinstance(arg, Float32Arg):
        dst_reg = cgen.register("xmm")
        code = cgen.gen.sqrt_f32(dst_reg, name=arg.name)
    elif isinstance(arg, Float64Arg):
        dst_reg = cgen.register("xmm")
        code = cgen.gen.sqrt_f64(dst_reg, name=arg.name)
    elif isinstance(arg, Float64x2Arg):
        dst_reg = cgen.register("xmm")
        code = cgen.gen.sqrt_f64x2(dst_reg, name=arg.name)
    elif isinstance(arg, (Float64x3Arg, Float64x4Arg)):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            dst_reg = cgen.register("ymm")
            code = 'vsqrtpd %s, yword [%s]\n' % (dst_reg, arg.name)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'sqrtpd %s, oword [%s]\n' % (dst_reg[0], arg.name)
            code += 'sqrtpd %s, oword [%s + 16]\n' % (dst_reg[1], arg.name)
    elif isinstance(arg, Float64x8Arg):
        if cgen.cpu.AVX512F:
            dst_reg = cgen.register('zmm')
            code = 'vsqrtpd %s, zword [%s]\n' % (dst_reg, arg.name)
        elif cgen.cpu.AVX:
            dst_reg = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vsqrtpd %s, yword [%s]\n' % (dst_reg[0], arg.name)
            code += 'vsqrtpd %s, yword [%s + 32]\n' % (dst_reg[1], arg.name)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
            code = 'sqrtpd %s, oword [%s]\n' % (dst_reg[0], arg.name)
            code += 'sqrtpd %s, oword [%s + 16]\n' % (dst_reg[1], arg.name)
            code += 'sqrtpd %s, oword [%s + 32]\n' % (dst_reg[2], arg.name)
            code += 'sqrtpd %s, oword [%s + 48]\n' % (dst_reg[3], arg.name)
    elif isinstance(arg, (Float32x2Arg, Float32x3Arg, Float32x4Arg)):
        dst_reg = cgen.register("xmm")
        code = cgen.gen.sqrt_f32x4(dst_reg, name=arg.name)
    elif isinstance(arg, Float32x8Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            dst_reg = cgen.register("ymm")
            code = 'vsqrtps %s, yword [%s]\n' % (dst_reg, arg.name)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'sqrtps %s, oword [%s]\n' % (dst_reg[0], arg.name)
            code += 'sqrtps %s, oword [%s + 16]\n' % (dst_reg[1], arg.name)
    elif isinstance(arg, Float32x16Arg):
        if cgen.cpu.AVX512F:
            dst_reg = cgen.register("zmm")
            code = 'vsqrtps %s, zword [%s]\n' % (dst_reg, arg.name)
        elif cgen.cpu.AVX:
            dst_reg = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vsqrtps %s, yword [%s]\n' % (dst_reg[0], arg.name)
            code += 'vsqrtps %s, yword [%s + 32]\n' % (dst_reg[1], arg.name)
        else:
            dst_reg = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
            code = 'sqrtps %s, oword [%s]\n' % (dst_reg[0], arg.name)
            code += 'sqrtps %s, oword [%s + 16]\n' % (dst_reg[1], arg.name)
            code += 'sqrtps %s, oword [%s + 32]\n' % (dst_reg[2], arg.name)
            code += 'sqrtps %s, oword [%s + 48]\n' % (dst_reg[3], arg.name)
    else:
        raise TypeError("Callable sqrt doesn't support argument ", arg, op_name.name)
    return code, dst_reg, type(arg)


def sqrt_f64(cgen, xmm):
    code = cgen.gen.sqrt_f64(xmm)
    return code, xmm, Float64Arg


def sqrt_f32(cgen, xmm):
    code = cgen.gen.sqrt_f32(xmm)
    return code, xmm, Float32Arg


def sqrt_f64x2(cgen, xmm):
    code = cgen.gen.sqrt_f64x2(xmm)
    return code, xmm, Float64x2Arg


def sqrt_f64x3(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vsqrtpd %s, %s\n' % (reg, reg)
        return code, reg, Float64x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'sqrtpd %s, oword [%s]\n' % (xmm1, reg)
        code += 'sqrtsd %s, qword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float64x3Arg


def sqrt_f64x4(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vsqrtpd %s, %s\n' % (reg, reg)
        return code, reg, Float64x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'sqrtpd %s, oword [%s]\n' % (xmm1, reg)
        code += 'sqrtpd %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float64x4Arg


def sqrt_f64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        code = 'vsqrtpd %s, %s\n' % (reg, reg)
        return code, reg, Float64x8Arg
    if cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vsqrtpd %s, yword [%s]\n' % (ymm1, reg)
        code += 'vsqrtpd %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'sqrtpd %s, oword [%s]\n' % (xmm1, reg)
        code += 'sqrtpd %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'sqrtpd %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'sqrtpd %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def sqrt_f32x2(cgen, xmm):
    code = cgen.gen.sqrt_f32x4(xmm)
    return code, xmm, Float32x2Arg


def sqrt_f32x3(cgen, xmm):
    code = cgen.gen.sqrt_f32x4(xmm)
    return code, xmm, Float32x3Arg


def sqrt_f32x4(cgen, xmm):
    code = cgen.gen.sqrt_f32x4(xmm)
    return code, xmm, Float32x4Arg


def sqrt_f32x8(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vsqrtps %s, %s\n' % (reg, reg)
        return code, reg, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'sqrtps %s, oword [%s]\n' % (xmm1, reg)
        code += 'sqrtps %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float32x8Arg


def sqrt_f32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        code = 'vsqrtps %s, %s\n' % (reg, reg)
        return code, reg, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vsqrtps %s, yword [%s]\n' % (ymm1, reg)
        code += 'vsqrtps %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'sqrtps %s, oword [%s]\n' % (xmm1, reg)
        code += 'sqrtps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'sqrtps %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'sqrtps %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


register_built_in('sqrt', (Name,), sqrt_name)
register_built_in('sqrt', (Float64Arg,), sqrt_f64)
register_built_in('sqrt', (Float32Arg,), sqrt_f32)
register_built_in('sqrt', (Float64x2Arg,), sqrt_f64x2)
register_built_in('sqrt', (Float64x3Arg,), sqrt_f64x3)
register_built_in('sqrt', (Float64x4Arg,), sqrt_f64x4)
register_built_in('sqrt', (Float64x8Arg,), sqrt_f64x8)
register_built_in('sqrt', (Float32x2Arg,), sqrt_f32x2)
register_built_in('sqrt', (Float32x3Arg,), sqrt_f32x3)
register_built_in('sqrt', (Float32x4Arg,), sqrt_f32x4)
register_built_in('sqrt', (Float32x8Arg,), sqrt_f32x8)
register_built_in('sqrt', (Float32x16Arg,), sqrt_f32x16)


def gen_qhorner_fma_f64(*args):
    code = ''
    xmm1 = args[0]
    xmm2 = args[1]
    for xmm in args[2:]:
        code += 'vfmadd213sd %s, %s, %s\n' % (xmm2, xmm1, xmm)
    return code


def gen_qhorner_avx_f64(*args):
    code = ''
    xmm1 = args[0]
    xmm2 = args[1]
    for xmm in args[2:]:
        code += "vmulsd %s, %s, %s\n" % (xmm2, xmm2, xmm1)
        code += "vaddsd %s, %s, %s\n" % (xmm2, xmm2, xmm)
    return code


def gen_qhorner_sse_f64(*args):
    code = ''
    xmm1 = args[0]
    xmm2 = args[1]
    for xmm in args[2:]:
        code += "mulsd %s, %s\n" % (xmm2, xmm1)
        code += "addsd %s, %s\n" % (xmm2, xmm)
    return code


def qhorner_f64(*args):
    cgen = args[0]
    if cgen.cpu.FMA:
        code = gen_qhorner_fma_f64(*args[1:])
    elif cgen.cpu.AVX:
        code = gen_qhorner_avx_f64(*args[1:])
    else:
        code = gen_qhorner_sse_f64(*args[1:])
    return code, args[2], Float64Arg


register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg), qhorner_f64)
register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg, Float64Arg), qhorner_f64)
register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg), qhorner_f64)
register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg), qhorner_f64)
register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg), qhorner_f64)
register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg), qhorner_f64)
register_built_in('qhorner', (Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg, Float64Arg), qhorner_f64)


def frexp_f64(cgen, xmm):
    reg = cgen.register('general')
    reg2 = cgen.register('general')
    xmm2 = cgen.register('xmm')
    xmm3 = cgen.register('xmm')
    xmm4 = cgen.register('xmm')

    if cgen.cpu.AVX:
        code = 'vpcmpeqw %s, %s, %s\n' % (xmm3, xmm3, xmm3)
        code += 'vpsrlq %s, %s, 53\n' % (xmm4, xmm3)
        code += 'vpsllq %s, %s, 1\n' % (xmm2, xmm)
        code += 'vpsrlq %s, %s, 53\n' % (xmm2, xmm2)
        code += 'vpsllq %s, %s, 52\n' % (xmm4, xmm4)
        code += 'vmovd %s, %s\n' % (reg, xmm2)
        code += 'vandnpd %s, %s, %s\n' % (xmm4, xmm4, xmm)
        code += 'vpsrlq %s, %s, 55\n' % (xmm3, xmm3)
        code += 'vpsllq %s, %s, 53\n' % (xmm3, xmm3)
        code += 'vorpd %s, %s, %s\n' % (xmm4, xmm4, xmm3)
        code += 'sub %s, 1022\n' % reg

        # NOTE handling of 0.0 case
        code += 'vpxor %s, %s, %s\n' % (xmm2, xmm2, xmm2)
        code += 'vcmpsd %s, %s, %s, 0\n' % (xmm2, xmm2, xmm)
        code += 'vmovd %s, %s\n' % (reg2, xmm2)
        code += 'not %s\n' % reg2
        code += 'and %s, %s\n' % (reg, reg2)
        code += 'vandnpd %s, %s, %s\n' % (xmm2, xmm2, xmm4)
    else:
        code = 'pcmpeqw %s, %s\n' % (xmm3, xmm3)
        code += 'movaps %s, %s\n' % (xmm4, xmm3)
        code += 'psrlq %s, 53\n' % xmm4
        code += 'movaps %s, %s\n' % (xmm2, xmm)
        code += 'psllq %s, 52\n' % xmm4
        code += 'psllq %s, 1\n' % xmm2
        code += 'psrlq %s, 53\n' % xmm2
        code += 'movd %s, %s\n' % (reg, xmm2)
        code += 'andnpd %s, %s\n' % (xmm4, xmm)
        code += 'psrlq %s, 55\n' % xmm3
        code += 'psllq %s, 53\n' % xmm3
        code += 'orpd %s, %s\n' % (xmm4, xmm3)
        code += 'sub %s, 1022\n' % reg

        # NOTE handling of 0.0 case
        code += 'pxor %s, %s\n' % (xmm2, xmm2)
        code += 'cmpsd %s, %s, 0\n' % (xmm2, xmm)
        code += 'movd %s, %s\n' % (reg2, xmm2)
        code += 'not %s\n' % reg2
        code += 'and %s, %s\n' % (reg, reg2)
        code += 'andnpd %s, %s\n' % (xmm2, xmm4)

    cgen.release_reg(xmm3)
    cgen.release_reg(xmm4)
    cgen.release_reg(reg2)
    return code, (xmm2, reg), (Float64Arg, Int32Arg)


def frexp_f32(cgen, xmm):
    reg = cgen.register('general')
    reg2 = cgen.register('general')
    xmm2 = cgen.register('xmm')
    xmm3 = cgen.register('xmm')
    xmm4 = cgen.register('xmm')

    if cgen.cpu.AVX:
        code = 'vpcmpeqw %s, %s, %s\n' % (xmm3, xmm3, xmm3)
        code += 'vpsrld %s, %s, 24\n' % (xmm4, xmm3)
        code += 'vpslld %s, %s, 1\n' % (xmm2, xmm)
        code += 'vpsrld %s, %s, 24\n' % (xmm2, xmm2)
        code += 'vpslld %s, %s, 23\n' % (xmm4, xmm4)
        code += 'vmovd %s, %s\n' % (reg, xmm2)
        code += 'vandnps %s, %s, %s\n' % (xmm4, xmm4, xmm)
        code += 'vpsrld %s, %s, 26\n' % (xmm3, xmm3)
        code += 'vpslld %s, %s, 24\n' % (xmm3, xmm3)
        code += 'vorps %s, %s, %s\n' % (xmm4, xmm4, xmm3)
        code += 'sub %s, 126\n' % reg

        # NOTE handling of 0.0 case
        code += 'vpxor %s, %s, %s\n' % (xmm2, xmm2, xmm2)
        code += 'vcmpss %s, %s, %s, 0\n' % (xmm2, xmm2, xmm)
        code += 'vmovd %s, %s\n' % (reg2, xmm2)
        code += 'not %s\n' % reg2
        code += 'and %s, %s\n' % (reg, reg2)
        code += 'vandnps %s, %s, %s\n' % (xmm2, xmm2, xmm4)
    else:
        code = 'pcmpeqw %s, %s\n' % (xmm3, xmm3)
        code += 'movaps %s, %s\n' % (xmm4, xmm3)
        code += 'psrld %s, 24\n' % xmm4
        code += 'movaps %s, %s\n' % (xmm2, xmm)
        code += 'pslld %s, 23\n' % xmm4
        code += 'pslld %s, 1\n' % xmm2
        code += 'psrld %s, 24\n' % xmm2
        code += 'movd %s, %s\n' % (reg, xmm2)
        code += 'andnps %s, %s\n' % (xmm4, xmm)
        code += 'psrld %s, 26\n' % xmm3
        code += 'pslld %s, 24\n' % xmm3
        code += 'orps %s, %s\n' % (xmm4, xmm3)
        code += 'sub %s, 126\n' % reg

        # NOTE handling of 0.0 case
        code += 'pxor %s, %s\n' % (xmm2, xmm2)
        code += 'cmpss %s, %s, 0\n' % (xmm2, xmm)
        code += 'movd %s, %s\n' % (reg2, xmm2)
        code += 'not %s\n' % reg2
        code += 'and %s, %s\n' % (reg, reg2)
        code += 'andnps %s, %s\n' % (xmm2, xmm4)

    cgen.release_reg(xmm3)
    cgen.release_reg(xmm4)
    cgen.release_reg(reg2)
    return code, (xmm2, reg), (Float32Arg, Int32Arg)

register_built_in('frexp', (Float32Arg,), frexp_f32)
register_built_in('frexp', (Float64Arg,), frexp_f64)


def ldexp_f32_i32(cgen, xmm, reg):
    if cgen.cpu.AVX512F:
        xmm2 = cgen.register('xmm')
        code = 'vcvtsi2ss %s, %s, %s\n' % (xmm2, xmm2, reg)
        code += "vscalefss %s, %s, %s\n" % (xmm, xmm, xmm2)
        cgen.release_reg(xmm2)
        return code, xmm, Float32Arg

    xmm2 = cgen.register('xmm')
    code = 'add %s, 127\n' % reg
    code += 'shl %s, 7\n' % reg
    if cgen.cpu.AVX:
        code += 'vpxor %s, %s, %s\n' % (xmm2, xmm2, xmm2)
        code += 'vpinsrw %s, %s, %s, 1\n' % (xmm2, xmm2, reg)
        code += 'vmulss %s, %s, %s\n' % (xmm, xmm, xmm2)
    else:
        code += 'pxor %s, %s\n' % (xmm2, xmm2)
        code += 'pinsrw %s, %s, 1\n' % (xmm2, reg)
        code += 'mulss %s, %s\n' % (xmm, xmm2)
    cgen.release_reg(xmm2)
    return code, xmm, Float32Arg


def _ldexp_f32x4_i32x4(cgen, xmm, reg, ret_type):
    if cgen.cpu.AVX512F:
        xmm2 = cgen.register('xmm')
        code = 'vcvtdq2ps %s, %s\n' % (xmm2, reg)
        code += "vscalefps %s, %s, %s\n" % (xmm, xmm, xmm2)
        cgen.release_reg(xmm2)
        return code, xmm, ret_type

    tmp_xmm = cgen.register('xmm')
    if cgen.cpu.AVX:
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpsrld %s, %s, 25\n' % (tmp_xmm, tmp_xmm)
        code += 'vpaddd %s, %s, %s\n' % (reg, reg, tmp_xmm)
        code += 'vpslld %s, %s, 23\n' % (reg, reg)
        code += 'vmulps %s, %s, %s\n' % (xmm, xmm, reg)
    else:
        code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, %s\n' % (reg, tmp_xmm)
        code += 'pslld %s, 23\n' % reg
        code += 'mulps %s, %s\n' % (xmm, reg)
    cgen.release_reg(tmp_xmm)
    return code, xmm, ret_type


def ldexp_f32x2_i32x2(cgen, xmm, reg):
    return _ldexp_f32x4_i32x4(cgen, xmm, reg, Float32x2Arg)


def ldexp_f32x3_i32x3(cgen, xmm, reg):
    return _ldexp_f32x4_i32x4(cgen, xmm, reg, Float32x3Arg)


def ldexp_f32x4_i32x4(cgen, xmm, reg):
    return _ldexp_f32x4_i32x4(cgen, xmm, reg, Float32x4Arg)


def ldexp_f32x8_i32x8(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        ymm2 = cgen.register('ymm')
        code = 'vcvtdq2ps %s, %s\n' % (ymm2, reg2)
        code += "vscalefps %s, %s, %s\n" % (reg1, reg1, ymm2)
        cgen.release_reg(ymm2)
        return code, reg1, Float32x8Arg
    elif cgen.cpu.AVX2:
        tmp_ymm = cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
        code += 'vpsrld %s, %s, 25\n' % (tmp_ymm, tmp_ymm)
        code += 'vpaddd %s, %s, %s\n' % (reg2, reg2, tmp_ymm)
        code += 'vpslld %s, %s, 23\n' % (reg2, reg2)
        code += 'vmulps %s, %s, %s\n' % (reg1, reg1, reg2)
        cgen.release_reg(tmp_ymm)
        return code, reg1, Float32x8Arg
    elif cgen.cpu.AVX:
        tmp_xmm, tmp_xmm2 = cgen.register('xmm'), cgen.register('xmm')
        v127_xmm = cgen.register('xmm')
        tmp_ymm2 = cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (v127_xmm, v127_xmm, v127_xmm)
        code += 'vpsrld %s, %s, 25\n' % (v127_xmm, v127_xmm)
        code += 'vpaddd %s, %s, oword[%s]\n' % (tmp_xmm, v127_xmm, reg2)
        code += 'vpaddd %s, %s, oword[%s + 16]\n' % (tmp_xmm2, v127_xmm, reg2)
        code += 'vpslld %s, %s, 23\n' % (tmp_xmm, tmp_xmm)
        code += 'vpslld %s, %s, 23\n' % (tmp_xmm2, tmp_xmm2)
        code += "vperm2f128 %s, %s, %s, 0x20\n" % (tmp_ymm2, 'y' + tmp_xmm[1:], 'y' + tmp_xmm2[1:])
        code += 'vmulps %s, %s, %s\n' % (reg1, reg1, tmp_ymm2)
        cgen.release_reg(tmp_xmm)
        cgen.release_reg(tmp_xmm2)
        cgen.release_reg(v127_xmm)
        cgen.release_reg(tmp_ymm2)
        return code, reg1, Float32x8Arg
    else:
        tmp_xmm = cgen.register('xmm')
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, oword [%s]\n' % (tmp_xmm, reg2)
        code += 'pslld %s, 23\n' % tmp_xmm
        code += 'xorps %s, %s\n' % (xmm1, xmm1)
        code += 'orps %s, %s\n' % (xmm1, tmp_xmm)
        code += 'mulps %s, oword [%s]\n' % (xmm1, reg1)

        code += 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, oword [%s + 16]\n' % (tmp_xmm, reg2)
        code += 'pslld %s, 23\n' % tmp_xmm
        code += 'xorps %s, %s\n' % (xmm2, xmm2)
        code += 'orps %s, %s\n' % (xmm2, tmp_xmm)
        code += 'mulps %s, oword [%s + 16]\n' % (xmm2, reg1)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2), Float32x8Arg


def ldexp_f32x16_i32x16(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        zmm2 = cgen.register('zmm')
        code = 'vcvtdq2ps %s, %s\n' % (zmm2, reg2)
        code += "vscalefps %s, %s, %s\n" % (reg1, reg1, zmm2)
        cgen.release_reg(zmm2)
        return code, reg1, Float32x16Arg
    elif cgen.cpu.AVX2:
        tmp_ymm = cgen.register('ymm')
        v127_ymm = cgen.register('ymm')
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (v127_ymm, v127_ymm, v127_ymm)
        code += 'vpsrld %s, %s, 25\n' % (v127_ymm, v127_ymm)
        code += 'vpaddd %s, %s, yword [%s]\n' % (tmp_ymm, v127_ymm, reg2)
        code += 'vpslld %s, %s, 23\n' % (tmp_ymm, tmp_ymm)
        code += 'vmulps %s, %s, yword [%s]\n' % (ymm1, tmp_ymm, reg1)
        code += 'vpaddd %s, %s, yword [%s + 32]\n' % (tmp_ymm, v127_ymm, reg2)
        code += 'vpslld %s, %s, 23\n' % (tmp_ymm, tmp_ymm)
        code += 'vmulps %s, %s, yword [%s + 32]\n' % (ymm2, tmp_ymm, reg1)
        cgen.release_reg(tmp_ymm)
        cgen.release_reg(v127_ymm)
        return code, (ymm1, ymm2), Float32x16Arg
    elif cgen.cpu.AVX:
        tmp_xmm, tmp_xmm2 = cgen.register('xmm'), cgen.register('xmm')
        tmp_ymm = cgen.register('ymm')
        v127_xmm = cgen.register('xmm')
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (v127_xmm, v127_xmm, v127_xmm)
        code += 'vpsrld %s, %s, 25\n' % (v127_xmm, v127_xmm)
        code += 'vpaddd %s, %s, oword[%s]\n' % (tmp_xmm, v127_xmm, reg2)
        code += 'vpaddd %s, %s, oword[%s + 16]\n' % (tmp_xmm2, v127_xmm, reg2)
        code += 'vpslld %s, %s, 23\n' % (tmp_xmm, tmp_xmm)
        code += 'vpslld %s, %s, 23\n' % (tmp_xmm2, tmp_xmm2)
        code += "vperm2f128 %s, %s, %s, 0x20\n" % (tmp_ymm, 'y' + tmp_xmm[1:], 'y' + tmp_xmm2[1:])
        code += 'vmulps %s, %s, yword [%s]\n' % (ymm1, tmp_ymm, reg1)
        code += 'vpaddd %s, %s, oword[%s + 32]\n' % (tmp_xmm, v127_xmm, reg2)
        code += 'vpaddd %s, %s, oword[%s + 48]\n' % (tmp_xmm2, v127_xmm, reg2)
        code += 'vpslld %s, %s, 23\n' % (tmp_xmm, tmp_xmm)
        code += 'vpslld %s, %s, 23\n' % (tmp_xmm2, tmp_xmm2)
        code += "vperm2f128 %s, %s, %s, 0x20\n" % (tmp_ymm, 'y' + tmp_xmm[1:], 'y' + tmp_xmm2[1:])
        code += 'vmulps %s, %s, yword [%s + 32]\n' % (ymm2, tmp_ymm, reg1)
        cgen.release_reg(tmp_xmm)
        cgen.release_reg(tmp_xmm2)
        cgen.release_reg(tmp_ymm)
        cgen.release_reg(v127_xmm)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        tmp_xmm = cgen.register('xmm')
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, oword [%s]\n' % (tmp_xmm, reg2)
        code += 'pslld %s, 23\n' % tmp_xmm
        code += 'movaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'mulps %s, %s\n' % (xmm1, tmp_xmm)

        code += 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, oword [%s + 16]\n' % (tmp_xmm, reg2)
        code += 'pslld %s, 23\n' % tmp_xmm
        code += 'movaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'mulps %s, %s\n' % (xmm2, tmp_xmm)

        code += 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, oword [%s + 32]\n' % (tmp_xmm, reg2)
        code += 'pslld %s, 23\n' % tmp_xmm
        code += 'movaps %s, oword[%s + 32]\n' % (xmm3, reg1)
        code += 'mulps %s, %s\n' % (xmm3, tmp_xmm)

        code += 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 25\n' % tmp_xmm
        code += 'paddd %s, oword [%s + 48]\n' % (tmp_xmm, reg2)
        code += 'pslld %s, 23\n' % tmp_xmm
        code += 'movaps %s, oword[%s + 48]\n' % (xmm4, reg1)
        code += 'mulps %s, %s\n' % (xmm4, tmp_xmm)

        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def ldexp_f64_i32(cgen, xmm, reg):
    if cgen.cpu.AVX512F:
        xmm2 = cgen.register('xmm')
        code = 'vcvtsi2sd %s, %s, %s\n' % (xmm2, xmm2, reg)
        code += "vscalefsd %s, %s, %s\n" % (xmm, xmm, xmm2)
        cgen.release_reg(xmm2)
        return code, xmm, Float64Arg

    xmm2 = cgen.register('xmm')
    code = 'add %s, 1023\n' % reg
    code += 'shl %s, 4\n' % reg
    if cgen.cpu.AVX:
        code += 'vpxor %s, %s, %s\n' % (xmm2, xmm2, xmm2)
        code += 'vpinsrw %s, %s, %s, 3\n' % (xmm2, xmm2, reg)
        code += 'vmulsd %s, %s, %s\n' % (xmm, xmm, xmm2)
    else:
        code += 'pxor %s, %s\n' % (xmm2, xmm2)
        code += 'pinsrw %s, %s, 3\n' % (xmm2, reg)
        code += 'mulsd %s, %s\n' % (xmm, xmm2)
    cgen.release_reg(xmm2)
    return code, xmm, Float64Arg


def ldexp_f64x2_i32x2(cgen, xmm, reg):
    if cgen.cpu.AVX512F:
        xmm2 = cgen.register('xmm')
        code = 'vcvtdq2pd %s, %s\n' % (xmm2, reg)
        code += "vscalefpd %s, %s, %s\n" % (xmm, xmm, xmm2)
        cgen.release_reg(xmm2)
        return code, xmm, Float64x2Arg

    tmp_xmm = cgen.register('xmm')
    if cgen.cpu.AVX:
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpsrld %s, %s, 22\n' % (tmp_xmm, tmp_xmm)
        code += 'vpaddd %s, %s, %s\n' % (reg, reg, tmp_xmm)
        code += 'vpmovzxdq %s, %s\n' % (reg, reg)
        code += 'vpsllq %s, %s, 52\n' % (reg, reg)
        code += 'vmulpd %s, %s, %s\n' % (xmm, xmm, reg)
    else:
        code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 22\n' % tmp_xmm
        code += 'paddd %s, %s\n' % (reg, tmp_xmm)
        code += 'pmovzxdq %s, %s\n' % (reg, reg)
        code += 'psllq %s, 52\n' % reg
        code += 'mulpd %s, %s\n' % (xmm, reg)
    cgen.release_reg(tmp_xmm)
    return code, xmm, Float64x2Arg


def _ldexp_f64x4_i32x4(cgen, reg1, xmm, ret_type):
    if cgen.cpu.AVX512F:
        ymm2 = cgen.register('ymm')
        code = 'vcvtdq2pd %s, %s\n' % (ymm2, xmm)
        code += "vscalefpd %s, %s, %s\n" % (reg1, reg1, ymm2)
        cgen.release_reg(ymm2)
        return code, reg1, ret_type
    elif cgen.cpu.AVX2:
        tmp_xmm = cgen.register('xmm')
        tmp_ymm = cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpsrld %s, %s, 22\n' % (tmp_xmm, tmp_xmm)
        code += 'vpaddd %s, %s, %s\n' % (tmp_xmm, tmp_xmm, xmm)
        code += 'vpmovzxdq %s, %s\n' % (tmp_ymm, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (tmp_ymm, tmp_ymm)
        code += 'vmulpd %s, %s, %s\n' % (reg1, reg1, tmp_ymm)
        cgen.release_reg(tmp_xmm)
        cgen.release_reg(tmp_ymm)
        return code, reg1, ret_type
    elif cgen.cpu.AVX:
        tmp_xmm = cgen.register('xmm')
        tmp_ymm = cgen.register('ymm')
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpsrld %s, %s, 22\n' % (tmp_xmm, tmp_xmm)
        code += 'vpaddd %s, %s, %s\n' % (tmp_xmm, tmp_xmm, xmm)
        code += 'vpmovzxdq %s, %s\n' % (xmm1, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (xmm1, xmm1)
        code += 'vmovhlps %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpmovzxdq %s, %s\n' % (xmm2, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (xmm2, xmm2)
        code += "vperm2f128 %s, %s, %s, 0x20\n" % (tmp_ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        code += 'vmulpd %s, %s, %s\n' % (reg1, reg1, tmp_ymm)
        cgen.release_reg(tmp_xmm)
        cgen.release_reg(tmp_ymm)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, reg1, ret_type
    else:
        tmp_xmm = cgen.register('xmm')
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 22\n' % tmp_xmm
        code += 'paddd %s, %s\n' % (xmm, tmp_xmm)
        code += 'pmovzxdq %s, %s\n' % (xmm1, xmm)
        code += 'psllq %s, 52\n' % xmm1
        code += 'mulpd %s, oword[%s]\n' % (xmm1, reg1)
        code += 'movhlps %s, %s\n' % (xmm, xmm)
        code += 'pmovzxdq %s, %s\n' % (xmm2, xmm)
        code += 'psllq %s, 52\n' % xmm2
        code += 'mulpd %s, oword[%s + 16]\n' % (xmm2, reg1)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2), ret_type


def ldexp_f64x3_i32x3(cgen, reg1, xmm):
    return _ldexp_f64x4_i32x4(cgen, reg1, xmm, Float64x3Arg)


def ldexp_f64x4_i32x4(cgen, reg1, xmm):
    return _ldexp_f64x4_i32x4(cgen, reg1, xmm, Float64x4Arg)


def ldexp_f64x8_i32x8(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        zmm2 = cgen.register('zmm')
        code = 'vcvtdq2pd %s, %s\n' % (zmm2, reg2)
        code += "vscalefpd %s, %s, %s\n" % (reg1, reg1, zmm2)
        cgen.release_reg(zmm2)
        return code, reg1, Float64x8Arg
    elif cgen.cpu.AVX2:
        tmp_ymm = cgen.register('ymm')
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
        code += 'vpsrld %s, %s, 22\n' % (tmp_ymm, tmp_ymm)
        code += 'vpaddd %s, %s, %s\n' % (tmp_ymm, tmp_ymm, reg2)
        code += 'vpmovzxdq %s, %s\n' % (ymm1, 'x' + tmp_ymm[1:])
        code += 'vpsllq %s, %s, 52\n' % (ymm1, ymm1)
        code += 'vmulpd %s, %s, yword[%s]\n' % (ymm1, ymm1, reg1)
        code += 'vperm2i128 %s, %s, %s, 0x3\n' % (tmp_ymm, tmp_ymm, tmp_ymm)
        code += 'vpmovzxdq %s, %s\n' % (ymm2, 'x' + tmp_ymm[1:])
        code += 'vpsllq %s, %s, 52\n' % (ymm2, ymm2)
        code += 'vmulpd %s, %s, yword[%s + 32]\n' % (ymm2, ymm2, reg1)
        cgen.release_reg(tmp_ymm)
        return code, (ymm1, ymm2), Float64x8Arg
    elif cgen.cpu.AVX:
        tmp_xmm = cgen.register('xmm')
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpsrld %s, %s, 22\n' % (tmp_xmm, tmp_xmm)
        code += 'vpaddd %s, %s, oword [%s]\n' % (tmp_xmm, tmp_xmm, reg2)
        code += 'vpmovzxdq %s, %s\n' % (xmm1, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (xmm1, xmm1)
        code += 'vmovhlps %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpmovzxdq %s, %s\n' % (xmm2, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (xmm2, xmm2)
        code += "vperm2f128 %s, %s, %s, 0x20\n" % (ymm1, 'y' + xmm1[1:], 'y' + xmm2[1:])
        code += 'vmulpd %s, %s, yword[%s]\n' % (ymm1, ymm1, reg1)
        code += 'vpcmpeqw %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpsrld %s, %s, 22\n' % (tmp_xmm, tmp_xmm)
        code += 'vpaddd %s, %s, oword [%s + 16]\n' % (tmp_xmm, tmp_xmm, reg2)
        code += 'vpmovzxdq %s, %s\n' % (xmm1, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (xmm1, xmm1)
        code += 'vmovhlps %s, %s, %s\n' % (tmp_xmm, tmp_xmm, tmp_xmm)
        code += 'vpmovzxdq %s, %s\n' % (xmm2, tmp_xmm)
        code += 'vpsllq %s, %s, 52\n' % (xmm2, xmm2)
        code += "vperm2f128 %s, %s, %s, 0x20\n" % (ymm2, 'y' + xmm1[1:], 'y' + xmm2[1:])
        code += 'vmulpd %s, %s, yword[%s + 32]\n' % (ymm2, ymm2, reg1)
        cgen.release_reg(tmp_xmm)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        tmp_xmm = cgen.register('xmm')
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 22\n' % tmp_xmm
        code += 'paddd %s, oword[%s]\n' % (tmp_xmm, reg2)
        code += 'pmovzxdq %s, %s\n' % (xmm1, tmp_xmm)
        code += 'psllq %s, 52\n' % xmm1
        code += 'mulpd %s, oword[%s]\n' % (xmm1, reg1)
        code += 'movhlps %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'pmovzxdq %s, %s\n' % (xmm2, tmp_xmm)
        code += 'psllq %s, 52\n' % xmm2
        code += 'mulpd %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'pcmpeqw %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'psrld %s, 22\n' % tmp_xmm
        code += 'paddd %s, oword[%s + 16]\n' % (tmp_xmm, reg2)
        code += 'pmovzxdq %s, %s\n' % (xmm3, tmp_xmm)
        code += 'psllq %s, 52\n' % xmm3
        code += 'mulpd %s, oword[%s + 32]\n' % (xmm3, reg1)
        code += 'movhlps %s, %s\n' % (tmp_xmm, tmp_xmm)
        code += 'pmovzxdq %s, %s\n' % (xmm4, tmp_xmm)
        code += 'psllq %s, 52\n' % xmm4
        code += 'mulpd %s, oword[%s + 48]\n' % (xmm4, reg1)
        cgen.release_reg(tmp_xmm)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


register_built_in('ldexp', (Float32Arg, Int32Arg), ldexp_f32_i32)
register_built_in('ldexp', (Float32x2Arg, Int32x2Arg), ldexp_f32x2_i32x2)
register_built_in('ldexp', (Float32x3Arg, Int32x3Arg), ldexp_f32x3_i32x3)
register_built_in('ldexp', (Float32x4Arg, Int32x4Arg), ldexp_f32x4_i32x4)
register_built_in('ldexp', (Float32x8Arg, Int32x8Arg), ldexp_f32x8_i32x8)
register_built_in('ldexp', (Float32x16Arg, Int32x16Arg), ldexp_f32x16_i32x16)
register_built_in('ldexp', (Float64Arg, Int32Arg), ldexp_f64_i32)
register_built_in('ldexp', (Float64x2Arg, Int32x2Arg), ldexp_f64x2_i32x2)
register_built_in('ldexp', (Float64x3Arg, Int32x3Arg), ldexp_f64x3_i32x3)
register_built_in('ldexp', (Float64x4Arg, Int32x4Arg), ldexp_f64x4_i32x4)
register_built_in('ldexp', (Float64x8Arg, Int32x8Arg), ldexp_f64x8_i32x8)


def rshift_i64_con(cgen, reg, con):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    code = 'shr %s, %i\n' % (reg, con.value)
    return code, reg, Int64Arg


def rshift_i64_i32(cgen, reg1, reg2):
    tmp = cgen.register('general64')
    if tmp == 'rcx':
        code = 'mov ecx, %s\n' % reg2
        code += 'shr %s, cl\n' % reg1
    elif reg1 == 'rcx' and reg2 == 'ecx':
        code = 'shr %s, cl\n' % reg1
    elif reg1 == 'rcx':
        code = 'mov %s, rcx\n' % tmp
        code += 'mov ecx, %s\n' % reg2
        code += 'shr %s, cl\n' % tmp
        code += 'mov rcx, %s\n' % tmp
    elif reg2 == 'ecx':
        code = 'shr %s, cl\n' % reg1
    else:
        code = 'mov %s, rcx\n' % tmp
        code += 'mov ecx, %s\n' % reg2
        code += 'shr %s, cl\n' % reg1
        code += 'mov rcx, %s\n' % tmp

    cgen.release_reg(tmp)
    return code, reg1, Int64Arg


def rshift_i32_con(cgen, reg, con):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    code = 'shr %s, %i\n' % (reg, con.value)
    return code, reg, Int32Arg


def rshift_i32_i32(cgen, reg1, reg2):
    tmp = cgen.register('general')
    if tmp == 'ecx':
        code = 'mov ecx, %s\n' % reg2
        code += 'shr %s, cl\n' % reg1
    elif reg1 == 'ecx' and reg2 == 'ecx':
        code = 'shr %s, cl\n' % reg1
    elif reg1 == 'ecx':
        code = 'mov %s, ecx\n' % tmp
        code += 'mov ecx, %s\n' % reg2
        code += 'shr %s, cl\n' % tmp
        code += 'mov ecx, %s\n' % tmp
    elif reg2 == 'ecx':
        code = 'shr %s, cl\n' % reg1
    else:
        code = 'mov %s, ecx\n' % tmp
        code += 'mov ecx, %s\n' % reg2
        code += 'shr %s, cl\n' % reg1
        code += 'mov ecx, %s\n' % tmp

    cgen.release_reg(tmp)
    return code, reg1, Int32Arg


def _rshift_i32x4_con(cgen, xmm, con, ret_type):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpsrld %s, %s, %i\n' % (xmm, xmm, con.value)
    else:
        code = 'psrld %s, %i\n' % (xmm, con.value)
    return code, xmm, ret_type


def rshift_i32x2_con(cgen, xmm, con):
    return _rshift_i32x4_con(cgen, xmm, con, Int32x2Arg)


def rshift_i32x3_con(cgen, xmm, con):
    return _rshift_i32x4_con(cgen, xmm, con, Int32x3Arg)


def rshift_i32x4_con(cgen, xmm, con):
    return _rshift_i32x4_con(cgen, xmm, con, Int32x4Arg)


def rshift_i32x8_con(cgen, reg, con):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        code = 'vpsrld %s, %s, %i\n' % (reg, reg, con.value)
        return code, reg, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'vpsrld %s, %s, %i\n' % (xmm1, xmm1, con.value)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'vpsrld %s, %s, %i\n' % (xmm2, xmm2, con.value)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'psrld %s, %i\n' % (xmm1, con.value)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'psrld %s, %i\n' % (xmm2, con.value)
        return code, (xmm1, xmm2), Int32x8Arg


def rshift_i32x16_con(cgen, reg, con):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    if cgen.cpu.AVX512F:
        code = 'vpsrld %s, %s, %i\n' % (reg, reg, con.value)
        return code, reg, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovdqa %s, yword[%s]\n' % (ymm1, reg)
        code += 'vpsrld %s, %s, %i\n' % (ymm1, ymm1, con.value)
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm2, reg)
        code += 'vpsrld %s, %s, %i\n' % (ymm2, ymm2, con.value)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'vpsrld %s, %s, %i\n' % (xmm1, xmm1, con.value)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'vpsrld %s, %s, %i\n' % (xmm2, xmm2, con.value)
        code += 'vmovdqa %s, oword[%s + 32]\n' % (xmm3, reg)
        code += 'vpsrld %s, %s, %i\n' % (xmm3, xmm3, con.value)
        code += 'vmovdqa %s, oword[%s + 48]\n' % (xmm4, reg)
        code += 'vpsrld %s, %s, %i\n' % (xmm4, xmm4, con.value)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'psrld %s, %i\n' % (xmm1, con.value)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'psrld %s, %i\n' % (xmm2, con.value)
        code += 'movdqa %s, oword[%s + 32]\n' % (xmm3, reg)
        code += 'psrld %s, %i\n' % (xmm3, con.value)
        code += 'movdqa %s, oword[%s + 48]\n' % (xmm4, reg)
        code += 'psrld %s, %i\n' % (xmm4, con.value)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


def rshift_i64x2_con(cgen, xmm, con):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpsrlq %s, %s, %i\n' % (xmm, xmm, con.value)
    else:
        code = 'psrlq %s, %i\n' % (xmm, con.value)
    return code, xmm, Int64x2Arg


def _rshift_i64x4_con(cgen, reg, con, ret_type):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        code = 'vpsrlq %s, %s, %i\n' % (reg, reg, con.value)
        return code, reg, ret_type
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'vpsrlq %s, %s, %i\n' % (xmm1, xmm1, con.value)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'vpsrlq %s, %s, %i\n' % (xmm2, xmm2, con.value)
        return code, (xmm1, xmm2), ret_type
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'psrlq %s, %i\n' % (xmm1, con.value)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'psrlq %s, %i\n' % (xmm2, con.value)
        return code, (xmm1, xmm2), ret_type


def rshift_i64x3_con(cgen, reg, con):
    return _rshift_i64x4_con(cgen, reg, con, Int64x3Arg)


def rshift_i64x4_con(cgen, reg, con):
    return _rshift_i64x4_con(cgen, reg, con, Int64x4Arg)


def rshift_i64x8_con(cgen, reg, con):
    if not isinstance(con.value, int):
        raise TypeError("Integer constant expected in rshift callable.", con.value)
    if cgen.cpu.AVX512F:
        code = 'vpsrlq %s, %s, %i\n' % (reg, reg, con.value)
        return code, reg, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovdqa %s, yword[%s]\n' % (ymm1, reg)
        code += 'vpsrlq %s, %s, %i\n' % (ymm1, ymm1, con.value)
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm2, reg)
        code += 'vpsrlq %s, %s, %i\n' % (ymm2, ymm2, con.value)
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'vpsrlq %s, %s, %i\n' % (xmm1, xmm1, con.value)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'vpsrlq %s, %s, %i\n' % (xmm2, xmm2, con.value)
        code += 'vmovdqa %s, oword[%s + 32]\n' % (xmm3, reg)
        code += 'vpsrlq %s, %s, %i\n' % (xmm3, xmm3, con.value)
        code += 'vmovdqa %s, oword[%s + 48]\n' % (xmm4, reg)
        code += 'vpsrlq %s, %s, %i\n' % (xmm4, xmm4, con.value)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword[%s]\n' % (xmm1, reg)
        code += 'psrlq %s, %i\n' % (xmm1, con.value)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm2, reg)
        code += 'psrlq %s, %i\n' % (xmm2, con.value)
        code += 'movdqa %s, oword[%s + 32]\n' % (xmm3, reg)
        code += 'psrlq %s, %i\n' % (xmm3, con.value)
        code += 'movdqa %s, oword[%s + 48]\n' % (xmm4, reg)
        code += 'psrlq %s, %i\n' % (xmm4, con.value)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg


register_built_in('rshift', (Int32Arg, Const), rshift_i32_con)
register_built_in('rshift', (Int32Arg, Int32Arg), rshift_i32_i32)
register_built_in('rshift', (Int64Arg, Const), rshift_i64_con)
register_built_in('rshift', (Int64Arg, Int32Arg), rshift_i64_i32)

register_built_in('rshift', (Int32x2Arg, Const), rshift_i32x2_con)
register_built_in('rshift', (Int32x3Arg, Const), rshift_i32x3_con)
register_built_in('rshift', (Int32x4Arg, Const), rshift_i32x4_con)
register_built_in('rshift', (Int32x8Arg, Const), rshift_i32x8_con)
register_built_in('rshift', (Int32x16Arg, Const), rshift_i32x16_con)

register_built_in('rshift', (Int64x2Arg, Const), rshift_i64x2_con)
register_built_in('rshift', (Int64x3Arg, Const), rshift_i64x3_con)
register_built_in('rshift', (Int64x4Arg, Const), rshift_i64x4_con)
register_built_in('rshift', (Int64x8Arg, Const), rshift_i64x8_con)


def rright_i32_i32(cgen, reg1, reg2):
    tmp = cgen.register('general')
    if tmp == 'ecx':
        code = 'mov ecx, %s\n' % reg2
        code += 'ror %s, cl\n' % reg1
    elif reg1 == 'ecx' and reg2 == 'ecx':
        code = 'ror %s, cl\n' % reg1
    elif reg1 == 'ecx':
        code = 'mov %s, ecx\n' % tmp
        code += 'mov ecx, %s\n' % reg2
        code += 'ror %s, cl\n' % tmp
        code += 'mov ecx, %s\n' % tmp
    elif reg2 == 'ecx':
        code = 'ror %s, cl\n' % reg1
    else:
        code = 'mov %s, ecx\n' % tmp
        code += 'mov ecx, %s\n' % reg2
        code += 'ror %s, cl\n' % reg1
        code += 'mov ecx, %s\n' % tmp

    cgen.release_reg(tmp)
    return code, reg1, Int32Arg


register_built_in('rotright', (Int32Arg, Int32Arg), rright_i32_i32)


def typecast_i32(cgen, reg, operand):
    if operand.name != 'float32':
        raise TypeError('int32 can only be typecast to float32!', operand.name)
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (xmm, reg)
    else:
        code = 'movd %s, %s\n' % (xmm, reg)
    return code, xmm, Float32Arg


def typecast_i32x2(cgen, xmm, operand):
    if operand.name != 'float32x2':
        raise TypeError('int32x2 can only be typecast to float32x2!', operand.name)
    return '', xmm, Float32x2Arg


def typecast_i32x3(cgen, xmm, operand):
    if operand.name != 'float32x3':
        raise TypeError('int32x3 can only be typecast to float32x3!', operand.name)
    return '', xmm, Float32x3Arg


def typecast_i32x4(cgen, xmm, operand):
    if operand.name != 'float32x4':
        raise TypeError('int32x4 can only be typecast to float32x4!', operand.name)
    return '', xmm, Float32x4Arg


def typecast_i32x8(cgen, reg, operand):
    if operand.name != 'float32x8':
        raise TypeError('int32x8 can only be typecast to float32x8!', operand.name)
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Float32x8Arg

    if cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm, reg)
        return code, ymm, Float32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float32x8Arg


def typecast_i32x16(cgen, reg, operand):
    if operand.name != 'float32x16':
        raise TypeError('int32x16 can only be typecast to float32x16!', operand.name)
    if cgen.cpu.AVX512F:
        return '', reg, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm1, reg)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def typecast_f32(cgen, xmm, operand):
    if operand.name != 'int32':
        raise TypeError('float32 can only be typecast to int32!', operand.name)
    reg = cgen.register('general')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (reg, xmm)
    else:
        code = 'movd %s, %s\n' % (reg, xmm)
    return code, reg, Int32Arg


def typecast_f32x2(cgen, xmm, operand):
    if operand.name != 'int32x2':
        raise TypeError('float32x2 can only be typecast to int32x2!', operand.name)
    return '', xmm, Int32x2Arg


def typecast_f32x3(cgen, xmm, operand):
    if operand.name != 'int32x3':
        raise TypeError('float32x3 can only be typecast to int32x3!', operand.name)
    return '', xmm, Int32x3Arg


def typecast_f32x4(cgen, xmm, operand):
    if operand.name != 'int32x4':
        raise TypeError('float32x4 can only be typecast to int32x4!', operand.name)
    return '', xmm, Int32x4Arg


def typecast_f32x8(cgen, reg, operand):
    if operand.name != 'int32x8':
        raise TypeError('float32x8 can only be typecast to int32x8!', operand.name)

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, %s\n' % ('y' + xmm1[1:], reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int32x8Arg


def typecast_f32x16(cgen, reg, operand):
    if operand.name != 'int32x16':
        raise TypeError('float16x8 can only be typecast to int16x8!', operand.name)

    if cgen.cpu.AVX512F:
        return '', reg, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovdqa %s, yword [%s]\n' % (ymm1, reg)
        code += 'vmovdqa %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'movdqa %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'movdqa %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


def typecast_i64(cgen, reg, operand):
    if operand.name != 'float64':
        raise TypeError('int64 can only be typecast to float64!', operand.name)
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovq %s, %s\n' % (xmm, reg)
    else:
        code = 'movq %s, %s\n' % (xmm, reg)
    return code, xmm, Float64Arg


def typecast_i64x2(cgen, xmm, operand):
    if operand.name != 'float64x2':
        raise TypeError('int64x2 can only be typecast to float64x2!', operand.name)
    return '', xmm, Float64x2Arg


def typecast_i64x3(cgen, reg, operand):
    if operand.name != 'float64x3':
        raise TypeError('int64x3 can only be typecast to float64x3!', operand.name)
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Float64x3Arg

    if cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm, reg)
        return code, ymm, Float64x3Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float64x3Arg


def typecast_i64x4(cgen, reg, operand):
    if operand.name != 'float64x4':
        raise TypeError('int64x4 can only be typecast to float64x4!', operand.name)
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Float64x4Arg

    if cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm, reg)
        return code, ymm, Float64x4Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float64x4Arg


def typecast_i64x8(cgen, reg, operand):
    if operand.name != 'float64x8':
        raise TypeError('int64x8 can only be typecast to float64x8!', operand.name)
    if cgen.cpu.AVX512F:
        return '', reg, Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm1, reg)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def typecast_f64(cgen, xmm, operand):
    if operand.name != 'int64':
        raise TypeError('float64 can only be typecast to int64!', operand.name)
    reg = cgen.register('general64')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovq %s, %s\n' % (reg, xmm)
    else:
        code = 'movq %s, %s\n' % (reg, xmm)
    return code, reg, Int64Arg


def typecast_f64x2(cgen, xmm, operand):
    if operand.name != 'int64x2':
        raise TypeError('float64x2 can only be typecast to int64x2!', operand.name)
    return '', xmm, Int64x2Arg


def typecast_f64x3(cgen, reg, operand):
    if operand.name != 'int64x3':
        raise TypeError('float64x3 can only be typecast to int64x3!', operand.name)

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Int64x3Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, %s\n' % ('y' + xmm1[1:], reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int64x3Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int64x3Arg


def typecast_f64x4(cgen, reg, operand):
    if operand.name != 'int64x4':
        raise TypeError('float64x4 can only be typecast to int64x4!', operand.name)

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Int64x4Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, %s\n' % ('y' + xmm1[1:], reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int64x4Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int64x4Arg


def typecast_f64x8(cgen, reg, operand):
    if operand.name != 'int64x8':
        raise TypeError('float64x8 can only be typecast to int64x8!', operand.name)

    if cgen.cpu.AVX512F:
        return '', reg, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovdqa %s, yword [%s]\n' % (ymm1, reg)
        code += 'vmovdqa %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'movdqa %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'movdqa %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg


register_built_in('typecast', (Int32Arg, Name), typecast_i32)
register_built_in('typecast', (Int32x2Arg, Name), typecast_i32x2)
register_built_in('typecast', (Int32x3Arg, Name), typecast_i32x3)
register_built_in('typecast', (Int32x4Arg, Name), typecast_i32x4)
register_built_in('typecast', (Int32x8Arg, Name), typecast_i32x8)
register_built_in('typecast', (Int32x16Arg, Name), typecast_i32x16)

register_built_in('typecast', (Float32Arg, Name), typecast_f32)
register_built_in('typecast', (Float32x2Arg, Name), typecast_f32x2)
register_built_in('typecast', (Float32x3Arg, Name), typecast_f32x3)
register_built_in('typecast', (Float32x4Arg, Name), typecast_f32x4)
register_built_in('typecast', (Float32x8Arg, Name), typecast_f32x8)
register_built_in('typecast', (Float32x16Arg, Name), typecast_f32x16)

register_built_in('typecast', (Int64Arg, Name), typecast_i64)
register_built_in('typecast', (Int64x2Arg, Name), typecast_i64x2)
register_built_in('typecast', (Int64x3Arg, Name), typecast_i64x3)
register_built_in('typecast', (Int64x4Arg, Name), typecast_i64x4)
register_built_in('typecast', (Int64x8Arg, Name), typecast_i64x8)

register_built_in('typecast', (Float64Arg, Name), typecast_f64)
register_built_in('typecast', (Float64x2Arg, Name), typecast_f64x2)
register_built_in('typecast', (Float64x3Arg, Name), typecast_f64x3)
register_built_in('typecast', (Float64x4Arg, Name), typecast_f64x4)
register_built_in('typecast', (Float64x8Arg, Name), typecast_f64x8)


def _create_local_array(cgen, operand, con):
    if not isinstance(operand, Name):
        raise TypeError("First argument is expected name of array. ", operand)
    if not isinstance(con, Const):
        raise TypeError("Second argument in array callable must be constant. ", con)

    factory = get_user_type_factory(operand.name)
    simple_types = {'int32': int32, 'int64': int64, 'float64': float64, 'float32': float32,
                    'int32x2': int32x2, 'int32x3': int32x3, 'int32x4': int32x4,
                    'int32x8': int32x8, 'int32x16': int32x16,
                    'int64x2': int64x2, 'int64x3': int64x3, 'int64x4': int64x4, 'int64x8': int64x8,
                    'float32x2': float32x2, 'float32x3': float32x3, 'float32x4': float32x4,
                    'float32x8': float32x8, 'float32x16': float32x16,
                    'float64x2': float64x2, 'float64x3': float64x3, 'float64x4': float64x4, 'float64x8': float64x8,
                    }
    if factory is None and operand.name in simple_types:
        factory = simple_types[operand.name]

    if factory is None:
        raise ValueError("Local array of type %s cannot be created." % operand.name)

    arr = stack_array(factory, int(con.value))
    arg = StackedArrayArg(name=generate_name('array_'), value=arr)
    arg = cgen.add_local_array(arg)
    return arg.load_cmd(cgen)


register_built_in('array', (Name, Const), _create_local_array)


def min_i32_i32(cgen, reg1, reg2):
    code = 'cmp %s, %s\n' % (reg1, reg2)
    code += 'cmovle %s, %s\n' % (reg2, reg1)
    return code, reg2, Int32Arg


def min_i64_i64(cgen, reg1, reg2):
    code = 'cmp %s, %s\n' % (reg1, reg2)
    code += 'cmovle %s, %s\n' % (reg2, reg1)
    return code, reg2, Int64Arg


def max_i32_i32(cgen, reg1, reg2):
    code = 'cmp %s, %s\n' % (reg1, reg2)
    code += 'cmovge %s, %s\n' % (reg2, reg1)
    return code, reg2, Int32Arg


def max_i64_i64(cgen, reg1, reg2):
    code = 'cmp %s, %s\n' % (reg1, reg2)
    code += 'cmovge %s, %s\n' % (reg2, reg1)
    return code, reg2, Int64Arg


def min_max_f32_f32(cgen, xmm1, xmm2, is_min):
    inst = 'minss' if is_min else 'maxss'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, xmm1, xmm1, xmm2)
    else:
        code = '%s %s, %s\n' % (inst, xmm1, xmm2)
    return code, xmm1, Float32Arg


def min_max_f64_f64(cgen, xmm1, xmm2, is_min):
    inst = 'minsd' if is_min else 'maxsd'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, xmm1, xmm1, xmm2)
    else:
        code = '%s %s, %s\n' % (inst, xmm1, xmm2)
    return code, xmm1, Float64Arg


def min_max_f32x4_f32x4(cgen, xmm1, xmm2, is_min, ret_type):
    inst = 'minps' if is_min else 'maxps'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, xmm1, xmm1, xmm2)
    else:
        code = '%s %s, %s\n' % (inst, xmm1, xmm2)
    return code, xmm1, ret_type


def min_max_f32x8_f32x8(cgen, reg1, reg2, is_min):
    inst = 'minps' if is_min else 'maxps'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, reg1, reg1, reg2)
        return code, reg1, Float32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += '%s %s, oword [%s]\n' % (inst, xmm1, reg2)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += '%s %s, oword [%s + 16]\n' % (inst, xmm2, reg2)
        return code, (xmm1, xmm2), Float32x8Arg


def min_max_f32x16_f32x16(cgen, reg1, reg2, is_min):
    inst = 'minps' if is_min else 'maxps'
    if cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, reg1, reg1, reg2)
        return code, reg1, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm1, reg1)
        code += 'v%s %s, %s, yword [%s]\n' % (inst, ymm1, ymm1, reg2)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm2, reg1)
        code += 'v%s %s, %s, yword [%s + 32]\n' % (inst, ymm2, ymm2, reg2)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += '%s %s, oword [%s]\n' % (inst, xmm1, reg2)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += '%s %s, oword [%s + 16]\n' % (inst, xmm2, reg2)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += '%s %s, oword [%s + 32]\n' % (inst, xmm3, reg2)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += '%s %s, oword [%s + 48]\n' % (inst, xmm4, reg2)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def min_max_f64x2_f64x2(cgen, xmm1, xmm2, is_min):
    inst = 'minpd' if is_min else 'maxpd'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, xmm1, xmm1, xmm2)
    else:
        code = '%s %s, %s\n' % (inst, xmm1, xmm2)
    return code, xmm1, Float64x2Arg


def min_max_f64x4_f64x4(cgen, reg1, reg2, is_min, ret_type):
    inst = 'minpd' if is_min else 'maxpd'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, reg1, reg1, reg2)
        return code, reg1, ret_type
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += '%s %s, oword [%s]\n' % (inst, xmm1, reg2)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += '%s %s, oword [%s + 16]\n' % (inst, xmm2, reg2)
        return code, (xmm1, xmm2), ret_type


def min_max_f64x8_f64x8(cgen, reg1, reg2, is_min):
    inst = 'minpd' if is_min else 'maxpd'
    if cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, reg1, reg1, reg2)
        return code, reg1, Float64x8Arg
    if cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm1, reg1)
        code += 'v%s %s, %s, yword [%s]\n' % (inst, ymm1, ymm1, reg2)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm2, reg1)
        code += 'v%s %s, %s, yword [%s + 32]\n' % (inst, ymm2, ymm2, reg2)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += '%s %s, oword [%s]\n' % (inst, xmm1, reg2)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += '%s %s, oword [%s + 16]\n' % (inst, xmm2, reg2)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += '%s %s, oword [%s + 32]\n' % (inst, xmm3, reg2)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += '%s %s, oword [%s + 48]\n' % (inst, xmm4, reg2)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def min_max_i32x4_i32x4(cgen, xmm1, xmm2, is_min, ret_type):
    inst = 'pminsd' if is_min else 'pmaxsd'
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, xmm1, xmm1, xmm2)
    else:
        code = '%s %s, %s\n' % (inst, xmm1, xmm2)
    return code, xmm1, ret_type


def min_max_i32x8_i32x8(cgen, reg1, reg2, is_min):
    inst = 'pminsd' if is_min else 'pmaxsd'

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, reg1, reg1, reg2)
        return code, reg1, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'v%s %s, %s, oword [%s]\n' % (inst, xmm1, xmm1, reg2)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'v%s %s, %s, oword [%s + 16]\n' % (inst, xmm2, xmm2, reg2)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += '%s %s, oword [%s]\n' % (inst, xmm1, reg2)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += '%s %s, oword [%s + 16]\n' % (inst, xmm2, reg2)
        return code, (xmm1, xmm2), Int32x8Arg


def min_max_i32x16_i32x16(cgen, reg1, reg2, is_min):
    inst = 'pminsd' if is_min else 'pmaxsd'

    if cgen.cpu.AVX512F:
        code = 'v%s %s, %s, %s\n' % (inst, reg1, reg1, reg2)
        return code, reg1, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovdqa %s, yword [%s]\n' % (ymm1, reg1)
        code += 'v%s %s, %s, yword [%s]\n' % (inst, ymm1, ymm1, reg2)
        code += 'vmovdqa %s, yword [%s + 32]\n' % (ymm2, reg1)
        code += 'v%s %s, %s, yword [%s + 32]\n' % (inst, ymm2, ymm2, reg2)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'v%s %s, %s, oword [%s]\n' % (inst, xmm1, xmm1, reg2)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'v%s %s, %s, oword [%s + 16]\n' % (inst, xmm2, xmm2, reg2)
        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'v%s %s, %s, oword [%s + 32]\n' % (inst, xmm3, xmm3, reg2)
        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += 'v%s %s, %s, oword [%s + 48]\n' % (inst, xmm4, xmm4, reg2)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += '%s %s, oword [%s]\n' % (inst, xmm1, reg2)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += '%s %s, oword [%s + 16]\n' % (inst, xmm2, reg2)
        code += 'movdqa %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += '%s %s, oword [%s + 32]\n' % (inst, xmm3, reg2)
        code += 'movdqa %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += '%s %s, oword [%s + 48]\n' % (inst, xmm4, reg2)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


register_built_in('max', (Int32Arg, Int32Arg), max_i32_i32)
register_built_in('max', (Int64Arg, Int64Arg), max_i64_i64)
register_built_in('min', (Int32Arg, Int32Arg), min_i32_i32)
register_built_in('min', (Int64Arg, Int64Arg), min_i64_i64)

register_built_in('min', (Float32Arg, Float32Arg), lambda cgen, xmm1, xmm2: min_max_f32_f32(cgen, xmm1, xmm2, True))
register_built_in('max', (Float32Arg, Float32Arg), lambda cgen, xmm1, xmm2: min_max_f32_f32(cgen, xmm1, xmm2, False))
register_built_in('min', (Float64Arg, Float64Arg), lambda cgen, xmm1, xmm2: min_max_f64_f64(cgen, xmm1, xmm2, True))
register_built_in('max', (Float64Arg, Float64Arg), lambda cgen, xmm1, xmm2: min_max_f64_f64(cgen, xmm1, xmm2, False))

register_built_in('min', (Float32x2Arg, Float32x2Arg), lambda cgen, xmm1, xmm2: min_max_f32x4_f32x4(cgen, xmm1, xmm2, True, Float32x2Arg))
register_built_in('max', (Float32x2Arg, Float32x2Arg), lambda cgen, xmm1, xmm2: min_max_f32x4_f32x4(cgen, xmm1, xmm2, False, Float32x2Arg))
register_built_in('min', (Float32x3Arg, Float32x3Arg), lambda cgen, xmm1, xmm2: min_max_f32x4_f32x4(cgen, xmm1, xmm2, True, Float32x3Arg))
register_built_in('max', (Float32x3Arg, Float32x3Arg), lambda cgen, xmm1, xmm2: min_max_f32x4_f32x4(cgen, xmm1, xmm2, False, Float32x3Arg))
register_built_in('min', (Float32x4Arg, Float32x4Arg), lambda cgen, xmm1, xmm2: min_max_f32x4_f32x4(cgen, xmm1, xmm2, True, Float32x4Arg))
register_built_in('max', (Float32x4Arg, Float32x4Arg), lambda cgen, xmm1, xmm2: min_max_f32x4_f32x4(cgen, xmm1, xmm2, False, Float32x4Arg))
register_built_in('min', (Float32x8Arg, Float32x8Arg), lambda cgen, reg1, reg2: min_max_f32x8_f32x8(cgen, reg1, reg2, True))
register_built_in('max', (Float32x8Arg, Float32x8Arg), lambda cgen, reg1, reg2: min_max_f32x8_f32x8(cgen, reg1, reg2, False))
register_built_in('min', (Float32x16Arg, Float32x16Arg), lambda cgen, reg1, reg2: min_max_f32x16_f32x16(cgen, reg1, reg2, True))
register_built_in('max', (Float32x16Arg, Float32x16Arg), lambda cgen, reg1, reg2: min_max_f32x16_f32x16(cgen, reg1, reg2, False))

register_built_in('min', (Float64x2Arg, Float64x2Arg), lambda cgen, xmm1, xmm2: min_max_f64x2_f64x2(cgen, xmm1, xmm2, True))
register_built_in('max', (Float64x2Arg, Float64x2Arg), lambda cgen, xmm1, xmm2: min_max_f64x2_f64x2(cgen, xmm1, xmm2, False))
register_built_in('min', (Float64x3Arg, Float64x3Arg), lambda cgen, xmm1, xmm2: min_max_f64x4_f64x4(cgen, xmm1, xmm2, True, Float64x3Arg))
register_built_in('max', (Float64x3Arg, Float64x3Arg), lambda cgen, xmm1, xmm2: min_max_f64x4_f64x4(cgen, xmm1, xmm2, False, Float64x3Arg))
register_built_in('min', (Float64x4Arg, Float64x4Arg), lambda cgen, xmm1, xmm2: min_max_f64x4_f64x4(cgen, xmm1, xmm2, True, Float64x4Arg))
register_built_in('max', (Float64x4Arg, Float64x4Arg), lambda cgen, xmm1, xmm2: min_max_f64x4_f64x4(cgen, xmm1, xmm2, False, Float64x4Arg))
register_built_in('min', (Float64x8Arg, Float64x8Arg), lambda cgen, reg1, reg2: min_max_f64x8_f64x8(cgen, reg1, reg2, True))
register_built_in('max', (Float64x8Arg, Float64x8Arg), lambda cgen, reg1, reg2: min_max_f64x8_f64x8(cgen, reg1, reg2, False))

register_built_in('min', (Int32x2Arg, Int32x2Arg), lambda cgen, xmm1, xmm2: min_max_i32x4_i32x4(cgen, xmm1, xmm2, True, Int32x2Arg))
register_built_in('max', (Int32x2Arg, Int32x2Arg), lambda cgen, xmm1, xmm2: min_max_i32x4_i32x4(cgen, xmm1, xmm2, False, Int32x2Arg))
register_built_in('min', (Int32x3Arg, Int32x3Arg), lambda cgen, xmm1, xmm2: min_max_i32x4_i32x4(cgen, xmm1, xmm2, True, Int32x3Arg))
register_built_in('max', (Int32x3Arg, Int32x3Arg), lambda cgen, xmm1, xmm2: min_max_i32x4_i32x4(cgen, xmm1, xmm2, False, Int32x3Arg))
register_built_in('min', (Int32x4Arg, Int32x4Arg), lambda cgen, xmm1, xmm2: min_max_i32x4_i32x4(cgen, xmm1, xmm2, True, Int32x4Arg))
register_built_in('max', (Int32x4Arg, Int32x4Arg), lambda cgen, xmm1, xmm2: min_max_i32x4_i32x4(cgen, xmm1, xmm2, False, Int32x4Arg))
register_built_in('min', (Int32x8Arg, Int32x8Arg), lambda cgen, reg1, reg2: min_max_i32x8_i32x8(cgen, reg1, reg2, True))
register_built_in('max', (Int32x8Arg, Int32x8Arg), lambda cgen, reg1, reg2: min_max_i32x8_i32x8(cgen, reg1, reg2, False))
register_built_in('min', (Int32x16Arg, Int32x16Arg), lambda cgen, reg1, reg2: min_max_i32x16_i32x16(cgen, reg1, reg2, True))
register_built_in('max', (Int32x16Arg, Int32x16Arg), lambda cgen, reg1, reg2: min_max_i32x16_i32x16(cgen, reg1, reg2, False))


def dot_f64x2_f64x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        xmm3 = cgen.register('xmm')
        code = "vmulpd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vmovhlps %s, %s, %s\n" % (xmm3, xmm3, xmm1)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        cgen.release_reg(xmm3)
    elif cgen.cpu.AVX:
        code = "vdppd %s, %s, %s, 0x31\n" % (xmm1, xmm1, xmm2)
    else:
        code = "dppd %s, %s, 0x31\n" % (xmm1, xmm2)

    return code, xmm1, Float64Arg


def dot_f64x3_f64x3(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        xmm2 = cgen.register('xmm')
        ymm1 = cgen.register('ymm')
        code = "vmulpd %s, %s, %s\n" % (ymm1, reg1, reg2)
        code += 'vextractf64x2 %s, %s, 1\n' % (xmm1, ymm1)
        code += "vmovhlps %s, %s, %s\n" % (xmm2, xmm2, 'x' + ymm1[1:])
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, 'x' + ymm1[1:])
        cgen.release_reg(ymm1)
        cgen.release_reg(xmm2)
    elif cgen.cpu.AVX:
        ymm1 = cgen.register('ymm')
        code = "vmulpd %s, %s, %s\n" % (ymm1, reg1, reg2)
        code += 'vextractf128 %s, %s, 1\n' % (xmm1, ymm1)
        code += "vdppd %s, %s, %s, 0x31\n" % ('x' + reg1[1:], 'x' + reg1[1:], 'x' + reg2[1:])
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, 'x' + reg1[1:])
        cgen.release_reg(ymm1)
    else:
        xmm2 = cgen.register('xmm')
        code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
        code += "dppd %s, oword[%s], 0x31\n" % (xmm1, reg2)
        code += "movsd %s, qword [%s + 16]\n" % (xmm2, reg1)
        code += "mulsd %s, qword [%s + 16]\n" % (xmm2, reg2)
        code += "addsd %s, %s\n" % (xmm1, xmm2)
        cgen.release_reg(xmm2)

    return code, xmm1, Float64Arg


def dot_f64x4_f64x4(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        xmm2 = cgen.register('xmm')
        ymm1 = cgen.register('ymm')
        code = "vmulpd %s, %s, %s\n" % (ymm1, reg1, reg2)
        code += "vextractf64x2 %s, %s, 1\n" % (xmm1, ymm1)
        code += "vaddpd %s, %s, %s\n" % (xmm1, xmm1, 'x' + ymm1[1:])
        code += "vmovhlps %s, %s, %s\n" % (xmm2, xmm2, xmm1)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        cgen.release_reg(xmm2)
        cgen.release_reg(ymm1)
    elif cgen.cpu.AVX:
        code = 'vmulpd %s, %s, %s\n' % (reg1, reg1, reg2)
        code += 'vhaddpd %s, %s, %s\n' % (reg1, reg1, reg1)
        code += 'vextractf128 %s, %s, 1\n' % (xmm1, reg1)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, 'x' + reg1[1:])
    else:
        xmm2 = cgen.register('xmm')
        code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
        code += "dppd %s, oword[%s], 0x31\n" % (xmm1, reg2)
        code += "movaps %s, oword [%s + 16]\n" % (xmm2, reg1)
        code += "dppd %s, oword [%s + 16], 0x31\n" % (xmm2, reg2)
        code += "addsd %s, %s\n" % (xmm1, xmm2)
        cgen.release_reg(xmm2)

    return code, xmm1, Float64Arg


def dot_f64x8_f64x8(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        zmm1 = cgen.register('zmm')
        ymm1 = cgen.register('ymm')
        xmm2 = cgen.register('xmm')
        code = "vmulpd %s, %s, %s\n" % (zmm1, reg1, reg2)
        code += "vextractf64x4 %s, %s, 1\n" % (ymm1, zmm1)
        code += "vaddpd %s, %s, %s\n" % (ymm1, ymm1, 'y' + zmm1[1:])
        code += "vextractf64x2 %s, %s, 1\n" % (xmm1, ymm1)
        code += "vaddpd %s, %s, %s\n" % (xmm1, xmm1, 'x' + ymm1[1:])
        code += "vmovhlps %s, %s, %s\n" % (xmm2, xmm2, xmm1)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        cgen.release_reg(xmm2)
        cgen.release_reg(ymm1)
        cgen.release_reg(zmm1)
    elif cgen.cpu.AVX:
        xmm2 = cgen.register('xmm')
        code = "vmovaps %s, oword [%s]\n" % (xmm1, reg1)
        code += "vdppd %s, %s, oword[%s], 0x31\n" % (xmm1, xmm1, reg2)
        code += "vmovaps %s, oword [%s + 16]\n" % (xmm2, reg1)
        code += "vdppd %s, %s, oword [%s + 16], 0x31\n" % (xmm2, xmm2, reg2)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vmovaps %s, oword [%s + 32]\n" % (xmm2, reg1)
        code += "vdppd %s, %s, oword[%s + 32], 0x31\n" % (xmm2, xmm2, reg2)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vmovaps %s, oword [%s + 48]\n" % (xmm2, reg1)
        code += "vdppd %s, %s, oword[%s + 48], 0x31\n" % (xmm2, xmm2, reg2)
        code += "vaddsd %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        cgen.release_reg(xmm2)
    else:
        xmm2 = cgen.register('xmm')
        code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
        code += "dppd %s, oword[%s], 0x31\n" % (xmm1, reg2)
        code += "movaps %s, oword [%s + 16]\n" % (xmm2, reg1)
        code += "dppd %s, oword [%s + 16], 0x31\n" % (xmm2, reg2)
        code += "addsd %s, %s\n" % (xmm1, xmm2)
        code += "movaps %s, oword [%s + 32]\n" % (xmm2, reg1)
        code += "dppd %s, oword[%s + 32], 0x31\n" % (xmm2, reg2)
        code += "addsd %s, %s\n" % (xmm1, xmm2)
        code += "movaps %s, oword [%s + 48]\n" % (xmm2, reg1)
        code += "dppd %s, oword[%s + 48], 0x31\n" % (xmm2, reg2)
        code += "addsd %s, %s\n" % (xmm1, xmm2)
        cgen.release_reg(xmm2)

    return code, xmm1, Float64Arg


def dot_f32x2_f32x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        xmm3 = cgen.register('xmm')
        code = "vmulps %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vpshufd %s, %s, 1\n" % (xmm3, xmm1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        cgen.release_reg(xmm3)
    elif cgen.cpu.AVX:
        code = "vdpps %s, %s, %s, 0x31\n" % (xmm1, xmm1, xmm2)
    else:
        code = "dpps %s, %s, 0x31\n" % (xmm1, xmm2)

    return code, xmm1, Float32Arg


def dot_f32x3_f32x3(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        xmm3 = cgen.register('xmm')
        xmm4 = cgen.register('xmm')
        code = "vmulps %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vmovhlps %s, %s, %s\n" % (xmm3, xmm3, xmm1)
        code += "vpshufd %s, %s, 1\n" % (xmm4, xmm1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, xmm4)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm4)
    elif cgen.cpu.AVX:
        code = "vdpps %s, %s, %s, 0x71\n" % (xmm1, xmm1, xmm2)
    else:
        code = "dpps %s, %s, 0x71\n" % (xmm1, xmm2)

    return code, xmm1, Float32Arg


def dot_f32x4_f32x4(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        xmm3 = cgen.register('xmm')
        code = "vmulps %s, %s, %s\n" % (xmm1, xmm1, xmm2)
        code += "vmovhlps %s, %s, %s\n" % (xmm3, xmm3, xmm1)
        code += "vaddps %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        code += "vpshufd %s, %s, 1\n" % (xmm3, xmm1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        cgen.release_reg(xmm3)
    elif cgen.cpu.AVX:
        code = "vdpps %s, %s, %s, 0xF1\n" % (xmm1, xmm1, xmm2)
    else:
        code = "dpps %s, %s, 0xF1\n" % (xmm1, xmm2)

    return code, xmm1, Float32Arg


def dot_f32x8_f32x8(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        ymm1 = cgen.register('ymm')
        xmm3 = cgen.register('xmm')
        code = "vmulps %s, %s, %s\n" % (ymm1, reg1, reg2)
        code += 'vextractf32x4 %s, %s, 1\n' % (xmm1, ymm1)
        code += "vaddps %s, %s, %s\n" % (xmm1, xmm1, 'x' + ymm1[1:])
        code += "vmovhlps %s, %s, %s\n" % (xmm3, xmm3, xmm1)
        code += "vaddps %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        code += "vpshufd %s, %s, 1\n" % (xmm3, xmm1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        cgen.release_reg(ymm1)
        cgen.release_reg(xmm3)
    elif cgen.cpu.AVX:
        code = "vdpps %s, %s, %s, 0xF1\n" % (reg1, reg1, reg2)
        code += 'vextractf128 %s, %s, 1\n' % (xmm1, reg1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, 'x' + reg1[1:])
    else:
        xmm2 = cgen.register('xmm')
        code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
        code += "dpps %s, oword[%s], 0xF1\n" % (xmm1, reg2)
        code += "movaps %s, oword [%s + 16]\n" % (xmm2, reg1)
        code += "dpps %s, oword [%s + 16], 0xF1\n" % (xmm2, reg2)
        code += "addss %s, %s\n" % (xmm1, xmm2)
        cgen.release_reg(xmm2)

    return code, xmm1, Float32Arg


def dot_f32x16_f32x16(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        zmm1 = cgen.register('zmm')
        ymm1 = cgen.register('ymm')
        xmm3 = cgen.register('xmm')
        code = "vmulps %s, %s, %s\n" % (zmm1, reg1, reg2)
        code += 'vextractf32x8 %s, %s, 1\n' % (ymm1, zmm1)
        code += "vaddps %s, %s, %s\n" % (ymm1, ymm1, 'y' + zmm1[1:])
        code += 'vextractf32x4 %s, %s, 1\n' % (xmm1, ymm1)
        code += "vaddps %s, %s, %s\n" % (xmm1, xmm1, 'x' + ymm1[1:])
        code += "vmovhlps %s, %s, %s\n" % (xmm3, xmm3, xmm1)
        code += "vaddps %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        code += "vpshufd %s, %s, 1\n" % (xmm3, xmm1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, xmm3)
        cgen.release_reg(zmm1)
        cgen.release_reg(ymm1)
        cgen.release_reg(xmm3)
    elif cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm1, reg1)
        code += "vdpps %s, %s, yword[%s], 0xF1\n" % (ymm1, ymm1, reg2)
        code += 'vmovaps %s, yword [%s + 32]\n' % (ymm2, reg1)
        code += "vdpps %s, %s, yword[%s + 32], 0xF1\n" % (ymm2, ymm2, reg2)
        code += "vaddps %s, %s, %s\n" % (ymm1, ymm1, ymm2)
        code += 'vextractf128 %s, %s, 1\n' % (xmm1, ymm1)
        code += "vaddss %s, %s, %s\n" % (xmm1, xmm1, 'x' + ymm1[1:])
        cgen.release_reg(ymm1)
        cgen.release_reg(ymm2)
    else:
        xmm2 = cgen.register('xmm')
        code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
        code += "dpps %s, oword[%s], 0xF1\n" % (xmm1, reg2)
        code += "movaps %s, oword [%s + 16]\n" % (xmm2, reg1)
        code += "dpps %s, oword [%s + 16], 0xF1\n" % (xmm2, reg2)
        code += "addss %s, %s\n" % (xmm1, xmm2)
        code += "movaps %s, oword [%s + 32]\n" % (xmm2, reg1)
        code += "dpps %s, oword [%s + 32], 0xF1\n" % (xmm2, reg2)
        code += "addss %s, %s\n" % (xmm1, xmm2)
        code += "movaps %s, oword [%s + 48]\n" % (xmm2, reg1)
        code += "dpps %s, oword [%s + 48], 0xF1\n" % (xmm2, reg2)
        code += "addss %s, %s\n" % (xmm1, xmm2)
        cgen.release_reg(xmm2)

    return code, xmm1, Float32Arg


register_built_in('dot', (Float64x2Arg, Float64x2Arg), dot_f64x2_f64x2)
register_built_in('dot', (Float64x3Arg, Float64x3Arg), dot_f64x3_f64x3)
register_built_in('dot', (Float64x4Arg, Float64x4Arg), dot_f64x4_f64x4)
register_built_in('dot', (Float64x8Arg, Float64x8Arg), dot_f64x8_f64x8)
register_built_in('dot', (Float32x2Arg, Float32x2Arg), dot_f32x2_f32x2)
register_built_in('dot', (Float32x3Arg, Float32x3Arg), dot_f32x3_f32x3)
register_built_in('dot', (Float32x4Arg, Float32x4Arg), dot_f32x4_f32x4)
register_built_in('dot', (Float32x8Arg, Float32x8Arg), dot_f32x8_f32x8)
register_built_in('dot', (Float32x16Arg, Float32x16Arg), dot_f32x16_f32x16)


# def ddot_f32x8_f32x8(cgen, reg1, reg2):
#     if cgen.cpu.AVX:
#         code = "vdpps %s, %s, %s, 0xFF\n" % (reg1, reg1, reg2)
#         return code, reg1, Float32x8Arg
#     else:
#         xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
#         code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
#         code += "dpps %s, oword[%s], 0xFF\n" % (xmm1, reg2)
#         code += "movaps %s, oword [%s + 16]\n" % (xmm2, reg1)
#         code += "dpps %s, oword [%s + 16], 0xFF\n" % (xmm2, reg2)
#         return code, (xmm1, xmm2), Float32x8Arg
#
#
# def qdot_f32x16_f32x16(cgen, reg1, reg2):
#     if cgen.cpu.AVX:
#         ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
#         code = "vmovaps %s, yword [%s]\n" % (ymm1, reg1)
#         code += "vdpps %s, %s, yword[%s], 0xFF\n" % (ymm1, ymm1, reg2)
#         code += "vmovaps %s, yword [%s + 32]\n" % (ymm2, reg1)
#         code += "vdpps %s, %s, yword [%s + 16], 0xFF\n" % (ymm2, ymm2, reg2)
#         return code, (ymm1, ymm2), Float32x16Arg
#     else:
#         xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
#         xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
#         code = "movaps %s, oword [%s]\n" % (xmm1, reg1)
#         code += "dpps %s, oword[%s], 0xFF\n" % (xmm1, reg2)
#         code += "movaps %s, oword [%s + 16]\n" % (xmm2, reg1)
#         code += "dpps %s, oword [%s + 16], 0xFF\n" % (xmm2, reg2)
#         code += "movaps %s, oword [%s + 32]\n" % (xmm3, reg1)
#         code += "dpps %s, oword[%s + 32], 0xFF\n" % (xmm3, reg2)
#         code += "movaps %s, oword [%s + 48]\n" % (xmm4, reg1)
#         code += "dpps %s, oword [%s + 48], 0xFF\n" % (xmm4, reg2)
#         return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg
#
#
# register_built_in('ddot', (Float32x8Arg, Float32x8Arg), ddot_f32x8_f32x8)
# register_built_in('qdot', (Float32x16Arg, Float32x16Arg), qdot_f32x16_f32x16)


def random_int32(cgen):
    if cgen.rng_state is None:
        state = int64x2(-8846114313915602277, -2720673578348880933)
        cgen.rng_state = Int64x2Arg(value=state)

    reg_bck = cgen.register('general64')
    reg1 = cgen.register('general64')
    if reg1 == 'rcx':
        reg1, reg_bck = reg_bck, reg1
    reg2 = cgen.register('general64')
    if reg2 == 'rcx':
        reg2, reg_bck = reg_bck, reg2

    reg = cgen.register('general')

    code = 'mov %s, rcx\n' % reg_bck
    code += 'mov %s, qword[%s]\n' % (reg1, cgen.rng_state.name)
    code += 'mov %s, 6364136223846793005\n' % reg2
    code += 'imul %s, %s\n' % (reg2, reg1)
    code += 'add %s, qword[%s + 8]\n' % (reg2, cgen.rng_state.name)
    code += 'mov qword[%s], %s\n' % (cgen.rng_state.name, reg2)
    code += 'mov %s, %s\n' % (reg2, reg1)
    code += 'shr %s, 18\n' % reg2
    code += 'xor %s, %s\n' % (reg2, reg1)
    code += 'shr %s, 27\n' % reg2
    code += 'shr %s, 59\n' % reg1
    code += 'mov rcx, %s\n' % reg1
    code += 'ror %s, cl\n' % cgen.regs.t_64_to_32(reg2)
    code += 'mov rcx, %s\n' % reg_bck
    code += 'mov %s, %s\n' % (reg, cgen.regs.t_64_to_32(reg2))

    cgen.release_reg(reg_bck)
    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    return code, reg, Int32Arg


def random_int32x2(cgen):
    code1, reg1, typ = random_int32(cgen)
    code2, reg2, typ = random_int32(cgen)
    code = code1 + code2

    xmm1 = cgen.register('xmm')

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovd %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrd %s, %s, %s, 0x1\n' % (xmm1, xmm1, reg2)
    else:
        code += 'movd %s, %s\n' % (xmm1, reg1)
        code += 'pinsrd %s, %s, 0x1\n' % (xmm1, reg2)

    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    return code, xmm1, Int32x2Arg


def random_int32x3(cgen):
    code1, reg1, typ = random_int32(cgen)
    code2, reg2, typ = random_int32(cgen)
    code3, reg3, typ = random_int32(cgen)
    code = code1 + code2 + code3

    xmm1 = cgen.register('xmm')

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovd %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrd %s, %s, %s, 0x1\n' % (xmm1, xmm1, reg2)
        code += 'vpinsrd %s, %s, %s, 0x2\n' % (xmm1, xmm1, reg3)
    else:
        code += 'movd %s, %s\n' % (xmm1, reg1)
        code += 'pinsrd %s, %s, 0x1\n' % (xmm1, reg2)
        code += 'pinsrd %s, %s, 0x2\n' % (xmm1, reg3)

    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    cgen.release_reg(reg3)
    return code, xmm1, Int32x3Arg


def random_int32x4(cgen):
    code1, reg1, typ = random_int32(cgen)
    code2, reg2, typ = random_int32(cgen)
    code3, reg3, typ = random_int32(cgen)
    code4, reg4, typ = random_int32(cgen)
    code = code1 + code2 + code3 + code4

    xmm1 = cgen.register('xmm')

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovd %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrd %s, %s, %s, 0x1\n' % (xmm1, xmm1, reg2)
        code += 'vpinsrd %s, %s, %s, 0x2\n' % (xmm1, xmm1, reg3)
        code += 'vpinsrd %s, %s, %s, 0x3\n' % (xmm1, xmm1, reg4)
    else:
        code += 'movd %s, %s\n' % (xmm1, reg1)
        code += 'pinsrd %s, %s, 0x1\n' % (xmm1, reg2)
        code += 'pinsrd %s, %s, 0x2\n' % (xmm1, reg3)
        code += 'pinsrd %s, %s, 0x3\n' % (xmm1, reg4)

    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    cgen.release_reg(reg3)
    cgen.release_reg(reg4)
    return code, xmm1, Int32x4Arg


def random_int32x8(cgen):
    code1, xmm1, typ1 = random_int32x4(cgen)
    code2, xmm2, typ2 = random_int32x4(cgen)
    code = code1 + code2

    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code += 'vinserti32x4 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
        code += 'vinserti32x4 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX2:
        ymm = cgen.register('ymm')
        code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, ymm, Int32x8Arg
    else:
        return code, (xmm1, xmm2), Int32x8Arg


def random_int32x16(cgen):
    code1, reg1, typ1 = random_int32x8(cgen)
    code2, reg2, typ2 = random_int32x8(cgen)
    code = code1 + code2

    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code += 'vinserti32x8 %s, %s, %s, 0\n' % (zmm, zmm, reg1)
        code += 'vinserti32x8 %s, %s, %s, 1\n' % (zmm, zmm, reg2)
        cgen.release_reg(reg1)
        cgen.release_reg(reg2)
        return code, zmm, Int32x16Arg
    elif cgen.cpu.AVX2:
        return code, (reg1, reg2), Int32x16Arg
    else:
        return code, reg1 + reg2, Int32x16Arg


def random_int64(cgen):
    code1, reg1, typ = random_int32(cgen)
    code2, reg2, typ = random_int32(cgen)
    code = code1 + code2
    reg = cgen.register('general64')
    code += 'mov %s, %s\n' % (reg, cgen.regs.t_32_to_64(reg1))
    code += 'shl %s, 32\n' % reg
    code += 'add %s, %s\n' % (reg, cgen.regs.t_32_to_64(reg2))
    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    return code, reg, Int64Arg


def random_int64x2(cgen):
    code1, reg1, typ = random_int64(cgen)
    code2, reg2, typ = random_int64(cgen)
    code = code1 + code2

    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovq %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrq %s, %s, %s, 1\n' % (xmm1, xmm1, reg2)
    else:
        code += 'movq %s, %s\n' % (xmm1, reg1)
        code += 'pinsrq %s, %s, 1\n' % (xmm1, reg2)
    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    return code, xmm1, Int64x2Arg


def random_int64x3(cgen):
    code1, reg1, typ = random_int64x2(cgen)
    code2, reg2, typ = random_int64(cgen)
    code = code1 + code2

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        xmm = cgen.register('xmm')
        code += 'vmovq %s, %s\n' % (xmm, reg2)
        if cgen.cpu.AVX512F:
            code += 'vinserti64x2 %s, %s, %s, 0\n' % (ymm, ymm, reg1)
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        else:
            code += 'vinserti128 %s, %s, %s, 0\n' % (ymm, ymm, reg1)
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        cgen.release_reg(xmm)
        cgen.release_reg(reg1)
        cgen.release_reg(reg2)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX:
        xmm2 = cgen.register('xmm')
        code += 'vmovq %s, %s\n' % (xmm2, reg2)
        cgen.release_reg(reg2)
        return code, (reg1, xmm2), Int64x3Arg
    else:
        xmm2 = cgen.register('xmm')
        code += 'movq %s, %s\n' % (xmm2, reg2)
        cgen.release_reg(reg2)
        return code, (reg1, xmm2), Int64x3Arg


def random_int64x4(cgen):
    code1, xmm1, typ = random_int64x2(cgen)
    code2, xmm2, typ = random_int64x2(cgen)
    code = code1 + code2

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        if cgen.cpu.AVX512F:
            code += 'vmovdqa64 %s, %s\n' % ('x' + ymm[1:], xmm1)
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        else:
            code += 'vmovdqa %s, %s\n' % ('x' + ymm[1:], xmm1)
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, ymm, Int64x4Arg
    else:
        return code, (xmm1, xmm2), Int64x4Arg


def random_int64x8(cgen):
    code1, reg1, typ = random_int64x4(cgen)
    code2, reg2, typ = random_int64x4(cgen)
    code = code1 + code2

    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code += 'vinserti64x4 %s, %s, %s, 0\n' % (zmm, zmm, reg1)
        code += 'vinserti64x4 %s, %s, %s, 1\n' % (zmm, zmm, reg2)
        cgen.release_reg(reg1)
        cgen.release_reg(reg2)
        return code, zmm, Int64x8Arg
    elif cgen.cpu.AVX2:
        return code, (reg1, reg2), Int64x8Arg
    else:
        return code, reg1 + reg2, Int64x8Arg


def random_float32(cgen):
    code, reg, typ = random_int32(cgen)
    xmm = cgen.register('xmm')
    code += 'shr %s, 9\n' % reg
    code += 'or %s, 0x3F800000\n' % reg
    const_arg = cgen.create_const(Float32Arg(value=float32(1.0)))
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovd %s, %s\n' % (xmm, reg)
        code += 'vsubss %s, %s, dword[%s]\n' % (xmm, xmm, const_arg.name)
    else:
        code += 'movd %s, %s\n' % (xmm, reg)
        code += 'subss %s, dword[%s]\n' % (xmm, const_arg.name)
    cgen.release_reg(reg)
    return code, xmm, Float32Arg


def random_float32x2(cgen):
    code1, xmm1, typ1 = random_float32(cgen)
    code2, xmm2, typ2 = random_float32(cgen)
    code = code1 + code2

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, %s, 0x10\n' % (xmm1, xmm1, xmm2)
    else:
        code += 'insertps %s, %s, 0x10\n' % (xmm1, xmm2)

    cgen.release_reg(xmm2)
    return code, xmm1, Float32x2Arg


def random_float32x3(cgen):
    code1, xmm1, typ1 = random_float32(cgen)
    code2, xmm2, typ2 = random_float32(cgen)
    code3, xmm3, typ3 = random_float32(cgen)
    code = code1 + code2 + code3

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, %s, 0x10\n' % (xmm1, xmm1, xmm2)
        code += 'vinsertps %s, %s, %s, 0x20\n' % (xmm1, xmm1, xmm3)
    else:
        code += 'insertps %s, %s, 0x10\n' % (xmm1, xmm2)
        code += 'insertps %s, %s, 0x20\n' % (xmm1, xmm3)

    cgen.release_reg(xmm2)
    cgen.release_reg(xmm3)
    return code, xmm1, Float32x3Arg


def random_float32x4(cgen):
    code1, xmm1, typ1 = random_float32(cgen)
    code2, xmm2, typ2 = random_float32(cgen)
    code3, xmm3, typ3 = random_float32(cgen)
    code4, xmm4, typ4 = random_float32(cgen)
    code = code1 + code2 + code3 + code4

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, %s, 0x10\n' % (xmm1, xmm1, xmm2)
        code += 'vinsertps %s, %s, %s, 0x20\n' % (xmm1, xmm1, xmm3)
        code += 'vinsertps %s, %s, %s, 0x30\n' % (xmm1, xmm1, xmm4)
    else:
        code += 'insertps %s, %s, 0x10\n' % (xmm1, xmm2)
        code += 'insertps %s, %s, 0x20\n' % (xmm1, xmm3)
        code += 'insertps %s, %s, 0x30\n' % (xmm1, xmm4)

    cgen.release_reg(xmm2)
    cgen.release_reg(xmm3)
    cgen.release_reg(xmm4)
    return code, xmm1, Float32x4Arg


def random_float32x8(cgen):
    code1, xmm1, typ1 = random_float32x4(cgen)
    code2, xmm2, typ2 = random_float32x4(cgen)
    code = code1 + code2
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code += 'vinserti32x4 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
        code += 'vinserti32x4 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, ymm, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, ymm, Float32x8Arg
    else:
        return code, (xmm1, xmm2), Float32x8Arg


def random_float32x16(cgen):
    code1, xmms1, typ1 = random_float32x8(cgen)
    code2, xmms2, typ2 = random_float32x8(cgen)
    code = code1 + code2
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code += 'vinsertf32x8 %s, %s, %s, 0\n' % (zmm, zmm, xmms1)
        code += 'vinsertf32x8 %s, %s, %s, 1\n' % (zmm, zmm, xmms2)
        cgen.release_reg(xmms1)
        cgen.release_reg(xmms2)
        return code, zmm, Float32x16Arg
    elif cgen.cpu.AVX:
        return code, (xmms1, xmms2), Float32x16Arg
    else:
        return code, xmms1 + xmms2, Float32x16Arg


def random_float64(cgen):
    code1, reg1, typ = random_int32(cgen)
    code2, reg2, typ = random_int32(cgen)
    code = code1 + code2
    reg = cgen.register('general64')
    code += 'mov %s, %s\n' % (reg, cgen.regs.t_32_to_64(reg1))
    code += 'shl %s, 32\n' % reg
    code += 'add %s, %s\n' % (reg, cgen.regs.t_32_to_64(reg2))
    code += 'shr %s, 12\n' % reg
    code += 'mov %s, 0x3FF0000000000000\n' % cgen.regs.t_32_to_64(reg1)
    code += 'or %s, %s\n' % (reg, cgen.regs.t_32_to_64(reg1))
    const_arg = cgen.create_const(Float64Arg(value=float64(1.0)))
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vsubsd %s, %s, qword[%s]\n' % (xmm, xmm, const_arg.name)
    else:
        code += 'movq %s, %s\n' % (xmm, reg)
        code += 'subsd %s, qword[%s]\n' % (xmm, const_arg.name)
    cgen.release_reg(reg1)
    cgen.release_reg(reg2)
    cgen.release_reg(reg)
    return code, xmm, Float64Arg


def random_float64x2(cgen):
    code1, xmm1, typ1 = random_float64(cgen)
    code2, xmm2, typ2 = random_float64(cgen)
    code = code1 + code2
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovlhps %s, %s, %s\n' % (xmm1, xmm1, xmm2)
    else:
        code += 'movlhps %s, %s\n' % (xmm1, xmm2)

    cgen.release_reg(xmm2)
    return code, xmm1, Float64x2Arg


def random_float64x3(cgen):
    code1, xmm1, typ1 = random_float64(cgen)
    code2, xmm2, typ2 = random_float64(cgen)
    code3, xmm3, typ3 = random_float64(cgen)
    code = code1 + code2 + code3

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code += 'vmovlhps %s, %s, %s\n' % ('x' + ymm[1:], xmm1, xmm2)
        if cgen.cpu.AVX512F:
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        else:
            code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        cgen.release_reg(xmm3)
        return code, ymm, Float64x3Arg
    else:
        code += 'movlhps %s, %s\n' % (xmm1, xmm2)
        cgen.release_reg(xmm2)
        return code, (xmm1, xmm3), Float64x3Arg


def random_float64x4(cgen):
    code1, xmm1, typ1 = random_float64(cgen)
    code2, xmm2, typ2 = random_float64(cgen)
    code3, xmm3, typ3 = random_float64(cgen)
    code4, xmm4, typ4 = random_float64(cgen)
    code = code1 + code2 + code3 + code4

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code += 'vmovlhps %s, %s, %s\n' % ('x' + ymm[1:], xmm1, xmm2)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        if cgen.cpu.AVX512F:
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        else:
            code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        cgen.release_reg(xmm3)
        cgen.release_reg(xmm4)
        return code, ymm, Float64x4Arg
    else:
        code += 'movlhps %s, %s\n' % (xmm1, xmm2)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        cgen.release_reg(xmm2)
        cgen.release_reg(xmm4)
        return code, (xmm1, xmm3), Float64x4Arg


def random_float64x8(cgen):
    code1, xmms1, typ1 = random_float64x4(cgen)
    code2, xmms2, typ2 = random_float64x4(cgen)
    code = code1 + code2

    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code += 'vinsertf64x4 %s, %s, %s, 0\n' % (zmm, zmm, xmms1)
        code += 'vinsertf64x4 %s, %s, %s, 1\n' % (zmm, zmm, xmms2)
        cgen.release_reg(xmms1)
        cgen.release_reg(xmms2)
        return code, zmm, Float64x8Arg
    elif cgen.cpu.AVX:
        return code, (xmms1, xmms2), Float64x8Arg
    else:
        return code, xmms1 + xmms2, Float64x8Arg


register_built_in('random_int32', tuple(), random_int32)
register_built_in('random_int32x2', tuple(), random_int32x2)
register_built_in('random_int32x3', tuple(), random_int32x3)
register_built_in('random_int32x4', tuple(), random_int32x4)
register_built_in('random_int32x8', tuple(), random_int32x8)
register_built_in('random_int32x16', tuple(), random_int32x16)

register_built_in('random_int64', tuple(), random_int64)
register_built_in('random_int64x2', tuple(), random_int64x2)
register_built_in('random_int64x3', tuple(), random_int64x3)
register_built_in('random_int64x4', tuple(), random_int64x4)
register_built_in('random_int64x8', tuple(), random_int64x8)

register_built_in('random_float32', tuple(), random_float32)
register_built_in('random_float32x2', tuple(), random_float32x2)
register_built_in('random_float32x3', tuple(), random_float32x3)
register_built_in('random_float32x4', tuple(), random_float32x4)
register_built_in('random_float32x8', tuple(), random_float32x8)
register_built_in('random_float32x16', tuple(), random_float32x16)

register_built_in('random_float64', tuple(), random_float64)
register_built_in('random_float64x2', tuple(), random_float64x2)
register_built_in('random_float64x3', tuple(), random_float64x3)
register_built_in('random_float64x4', tuple(), random_float64x4)
register_built_in('random_float64x8', tuple(), random_float64x8)


def seed(cgen, reg):
    if cgen.rng_state is None:
        state = int64x2(-8846114313915602277, -2720673578348880933)
        cgen.rng_state = Int64x2Arg(value=state)

    code = 'mov qword[%s], 0\n' % cgen.rng_state.name
    code += 'shl %s, 1\n' % reg
    code += 'or %s, 1\n' % reg
    code += 'mov qword[%s + 8], %s\n' % (cgen.rng_state.name, reg)
    co, r, typ = random_int32(cgen)
    cgen.release_reg(r)
    code += co
    code += 'mov %s, -8846114313915602277\n' % reg
    code += 'add %s, qword[%s]\n' % (reg, cgen.rng_state.name)
    code += 'mov qword[%s], %s\n' % (cgen.rng_state.name, reg)
    co, r, typ = random_int32(cgen)
    cgen.release_reg(r)
    code += co
    return code, reg, Int64Arg


register_built_in('seed', (Int64Arg,), seed)


def thread_idx(cgen):
    if cgen.thread_idx is None:
        cgen.thread_idx = Int32Arg(value=int32(0))

    reg = cgen.register('general')
    code = 'mov %s, dword[%s]\n' % (reg, cgen.thread_idx.name)
    return code, reg, Int32Arg


register_built_in('thread_idx', tuple(), thread_idx)


def nthreads(cgen):
    reg = cgen.register('general')
    code = 'mov %s, %i\n' % (reg, cgen.nthreads)
    return code, reg, Int32Arg


register_built_in('nthreads', tuple(), nthreads)


def _check_extract8_con(con):
    val = con.value
    if not isinstance(val, int):
        raise ValueError("extract8 callable expect second argument integer constant. ", val)
    if val != 0 and val != 1:
        raise ValueError("extract8 callable expect second argument values of 0 or 1. ", val)


def extract8_f32x16_con(cgen, reg, con):
    _check_extract8_con(con)
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vextractf32x8 %s, %s, %i\n' % (ymm, reg, con.value)
        return code, ymm, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword [%s + %i]\n' % (ymm, reg, con.value * 32)
        return code, ymm, Float32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword [%s + %i]\n' % (xmm1, reg, con.value * 32)
        code += 'movaps %s, oword [%s + %i]\n' % (xmm2, reg, con.value * 32 + 16)
        return code, (xmm1, xmm2), Float32x8Arg


def extract8_i32x16_con(cgen, reg, con):
    _check_extract8_con(con)
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vextracti32x8 %s, %s, %i\n' % (ymm, reg, con.value)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX2:
        ymm = cgen.register('ymm')
        code = 'vmovdqa %s, yword [%s + %i]\n' % (ymm, reg, con.value * 32)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s + %i]\n' % (xmm1, reg, con.value * 32)
        code += 'vmovdqa %s, oword [%s + %i]\n' % (xmm2, reg, con.value * 32 + 16)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword [%s + %i]\n' % (xmm1, reg, con.value * 32)
        code += 'movdqa %s, oword [%s + %i]\n' % (xmm2, reg, con.value * 32 + 16)
        return code, (xmm1, xmm2), Int32x8Arg


def extract8_name_con(cgen, name, con):
    _check_extract8_con(con)
    arg = cgen.get_arg(name)
    if isinstance(arg, Float32x16Arg):
        if cgen.cpu.AVX512F or cgen.cpu.AVX:
            xmms = cgen.register('ymm')
            code = 'vmovaps %s, yword [%s + %i]\n' % (xmms, arg.name, con.value * 32)
        else:
            xmms = cgen.register('xmm'), cgen.register('xmm')
            code = 'movaps %s, oword [%s + %i]\n' % (xmms[0], arg.name, con.value * 32)
            code += 'movaps %s, oword [%s + %i]\n' % (xmms[1], arg.name, con.value * 32 + 16)
        arg_type = Float32x8Arg
    elif isinstance(arg, Int32x16Arg):
        if cgen.cpu.AVX512F:
            xmms = cgen.register('ymm')
            code = 'vmovdqa32 %s, yword [%s + %i]\n' % (xmms, arg.name, con.value * 32)
        elif cgen.cpu.AVX2:
            xmms = cgen.register('ymm')
            code = 'vmovdqa %s, yword [%s + %i]\n' % (xmms, arg.name, con.value * 32)
        elif cgen.cpu.AVX:
            xmms = cgen.register('xmm'), cgen.register('xmm')
            code = 'vmovdqa %s, oword [%s + %i]\n' % (xmms[0], arg.name, con.value * 32)
            code += 'vmovdqa %s, oword [%s + %i]\n' % (xmms[1], arg.name, con.value * 32 + 16)
        else:
            xmms = cgen.register('xmm'), cgen.register('xmm')
            code = 'movdqa %s, oword [%s + %i]\n' % (xmms[0], arg.name, con.value * 32)
            code += 'movdqa %s, oword [%s + %i]\n' % (xmms[1], arg.name, con.value * 32 + 16)
        arg_type = Int32x8Arg
    else:
        raise ValueError("extract8 callable first argument expect float32x16 or int32x16.", arg)

    return code, xmms, arg_type


register_built_in('extract8', (Float32x16Arg, Const), extract8_f32x16_con)
register_built_in('extract8', (Int32x16Arg, Const), extract8_i32x16_con)
register_built_in('extract8', (Name, Const), extract8_name_con)