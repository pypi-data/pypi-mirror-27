
from .cgen import register_built_in
from .dbl_vec_arg import Float64x4Arg, Float64x2Arg, Float64x3Arg, Float64x8Arg
from .flt_vec_arg import Float32x2Arg, Float32x3Arg, Float32x4Arg, Float32x8Arg, Float32x16Arg
from .int_vec_arg import Int32x4Arg, Int64x4Arg, Int64x2Arg, Int64x3Arg,\
    Int32x3Arg, Int32x2Arg, Int32x8Arg, Int32x16Arg, Int64x8Arg
from .mask import MaskI32x2Arg, MaskI32x3Arg, MaskI32x4Arg, MaskI32x8Arg, MaskI32x16Arg,\
    MaskI64x2Arg, MaskI64x3Arg, MaskI64x4Arg, MaskI64x8Arg, MaskF32x2Arg, MaskF32x3Arg,\
    MaskF32x4Arg, MaskF32x8Arg, MaskF32x16Arg, MaskF64x2Arg, MaskF64x3Arg, MaskF64x4Arg, MaskF64x8Arg


__all__ = []


def _select_i32x4_i32x4_mi32x4(cgen, xmm1, xmm2, xmm3, ret_type):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, ret_type
    elif cgen.cpu.AVX:
        code = 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
    return code, xmm1, ret_type


def select_i32x2_i32x2_mi32x2(cgen, xmm1, xmm2, xmm3):
    return _select_i32x4_i32x4_mi32x4(cgen, xmm1, xmm2, xmm3, Int32x2Arg)


def select_i32x2_i32x2_mf64x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Int32x2Arg
    elif cgen.cpu.AVX:
        code = "vshufps %s, %s, %s, 0x08\n" % (xmm3, xmm3, xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = "shufps %s, %s, 0x08\n" % (xmm3, xmm3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)

    return code, xmm1, Int32x2Arg


def select_i32x2_i32x2_mi64x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Int32x2Arg
    elif cgen.cpu.AVX:
        code = "vpshufd %s, %s, 0x08\n" % (xmm3, xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = "pshufd %s, %s, 0x08\n" % (xmm3, xmm3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)

    return code, xmm1, Int32x2Arg


def select_i32x3_i32x3_mi32x3(cgen, xmm1, xmm2, xmm3):
    return _select_i32x4_i32x4_mi32x4(cgen, xmm1, xmm2, xmm3, Int32x3Arg)


def select_i32x3_i32x3_mf64x3(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Int32x3Arg

    xmm3 = cgen.register('xmm')
    if cgen.cpu.AVX:
        code = 'vshufps %s, %s, %s, 0x08\n' % (reg, reg, reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm3, reg)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + reg[1:], 'x' + reg[1:], xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    else:
        code = 'movaps %s, oword[%s]\n' % (xmm3, reg)
        code += 'shufps %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movhpd %s, qword [%s + 16]\n' % (xmm3, reg)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
    cgen.release_reg(xmm3)
    return code, xmm1, Int32x3Arg


def select_i32x3_i32x3_mi64x3(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Int32x3Arg

    xmm3 = cgen.register('xmm')
    if cgen.cpu.AVX2:
        code = 'vpshufd %s, %s, 0x08\n' % (reg, reg)
        code += 'vextracti128 %s, %s, 1\n' % (xmm3, reg)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + reg[1:], 'x' + reg[1:], xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    elif cgen.cpu.AVX:
        code = 'vmovdqa %s, oword[%s]\n' % (xmm3, reg)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'vpinsrd %s, %s, dword [%s + 16], 0x2\n' % (xmm3, xmm3, reg)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'movdqa %s, oword[%s]\n' % (xmm3, reg)
        code += 'pshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'pinsrd %s, dword [%s + 16], 0x2\n' % (xmm3, reg)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
    cgen.release_reg(xmm3)
    return code, xmm1, Int32x3Arg


def select_i32x4_i32x4_mi32x4(cgen, xmm1, xmm2, xmm3):
    return _select_i32x4_i32x4_mi32x4(cgen, xmm1, xmm2, xmm3, Int32x4Arg)


def select_i32x4_i32x4_mf64x4(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Int32x4Arg

    xmm3 = cgen.register('xmm')
    if cgen.cpu.AVX:
        code = 'vshufps %s, %s, %s, 0x08\n' % (reg, reg, reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm3, reg)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + reg[1:], 'x' + reg[1:], xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    else:
        xmm4 = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (xmm3, reg)
        code += 'shufps %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm4, reg)
        code += 'shufps %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
        cgen.release_reg(xmm4)
    cgen.release_reg(xmm3)
    return code, xmm1, Int32x4Arg


def select_i32x4_i32x4_mi64x4(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Int32x4Arg

    xmm3 = cgen.register('xmm')
    if cgen.cpu.AVX2:
        code = 'vpshufd %s, %s, 0x08\n' % (reg, reg)
        code += 'vextracti128 %s, %s, 1\n' % (xmm3, reg)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + reg[1:], 'x' + reg[1:], xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    elif cgen.cpu.AVX:
        xmm4 = cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (xmm3, reg)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm4, reg)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
        cgen.release_reg(xmm4)
    else:
        xmm4 = cgen.register('xmm')
        code = 'movdqa %s, oword[%s]\n' % (xmm3, reg)
        code += 'pshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm4, reg)
        code += 'pshufd %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
        cgen.release_reg(xmm4)
    cgen.release_reg(xmm3)
    return code, xmm1, Int32x4Arg


def _select_i32x8_i32x8_mi32x8_sse(cgen, reg1, reg2, reg3):
    xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
    xmm3 = cgen.register('xmm')
    code = 'movaps %s, oword[%s]\n' % (xmm1, reg1)
    code += 'movaps %s, oword[%s]\n' % (xmm3, reg3)
    code += 'pand %s, %s\n' % (xmm1, xmm3)
    code += 'pandn %s, oword[%s]\n' % (xmm3, reg2)
    code += 'por %s, %s\n' % (xmm1, xmm3)
    code += 'movaps %s, oword[%s + 16]\n' % (xmm2, reg1)
    code += 'movaps %s, oword[%s + 16]\n' % (xmm3, reg3)
    code += 'pand %s, %s\n' % (xmm2, xmm3)
    code += 'pandn %s, oword[%s + 16]\n' % (xmm3, reg2)
    code += 'por %s, %s\n' % (xmm2, xmm3)
    cgen.release_reg(xmm3)
    return code, (xmm1, xmm2), Int32x8Arg


def select_i32x8_i32x8_mi32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int32x8Arg

    if cgen.cpu.AVX2:
        code = 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'vmovaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'vmovaps %s, oword[%s]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vpandn %s, %s, oword[%s]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vpandn %s, %s, oword[%s + 16]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        return _select_i32x8_i32x8_mi32x8_sse(cgen, reg1, reg2, reg3)


def select_i32x8_i32x8_mf32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int32x8Arg

    if cgen.cpu.AVX2:
        code = 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'vmovaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'vmovaps %s, %s\n' % (xmm3, 'x' + reg3[1:])
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vpandn %s, %s, oword[%s]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'vextractf128 %s, %s, 1\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vpandn %s, %s, oword[%s + 16]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        return _select_i32x8_i32x8_mi32x8_sse(cgen, reg1, reg2, reg3)


def select_i32x8_i32x8_mf64x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int32x8Arg

    xmm3 = cgen.register('xmm')
    if cgen.cpu.AVX2:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vmovaps %s, yword[%s]\n' % (ymm1, reg3)
        code += 'vshufps %s, %s, %s, 0x08\n' % (ymm1, ymm1, ymm1)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg3)
        code += 'vshufps %s, %s, %s, 0x08\n' % (ymm2, ymm2, ymm2)
        code += 'vpunpcklqdq %s, %s, %s\n' % (ymm1, ymm1, ymm2)
        code += 'vpermq %s, %s, 0xD8\n' % (ymm1, ymm1)
        code += 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, ymm1)
        cgen.release_reg(ymm1)
        cgen.release_reg(ymm2)
        return code, reg1, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovaps %s, oword[%s]\n' % (xmm3, reg3)
        code += 'vshufps %s, %s, %s, 0x08\n' % (xmm3, xmm3, xmm3)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm4, reg3)
        code += 'vshufps %s, %s, %s, 0x08\n' % (xmm4, xmm4, xmm4)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        code += 'vmovaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'vmovaps %s, oword[%s]\n' % (xmm2, reg2)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)

        code += 'vmovaps %s, oword[%s + 32]\n' % (xmm3, reg3)
        code += 'vshufps %s, %s, %s, 0x08\n' % (xmm3, xmm3, xmm3)
        code += 'vmovaps %s, oword[%s + 48]\n' % (xmm4, reg3)
        code += 'vshufps %s, %s, %s, 0x08\n' % (xmm4, xmm4, xmm4)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm4, reg2)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm2, xmm4, xmm2, xmm3)

        cgen.release_reg(xmm3)
        cgen.release_reg(xmm4)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (xmm3, reg3)
        code += 'shufps %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm4, reg3)
        code += 'shufps %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        code += 'movaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'movaps %s, oword[%s]\n' % (xmm2, reg2)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)

        code += 'movaps %s, oword[%s + 32]\n' % (xmm3, reg3)
        code += 'shufps %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movaps %s, oword[%s + 48]\n' % (xmm4, reg3)
        code += 'shufps %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm4, reg2)
        code += 'pand %s, %s\n' % (xmm2, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm4)
        code += 'por %s, %s\n' % (xmm2, xmm3)

        cgen.release_reg(xmm3)
        cgen.release_reg(xmm4)
        return code, (xmm1, xmm2), Int32x8Arg


def select_i32x8_i32x8_mi64x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int32x8Arg

    xmm3 = cgen.register('xmm')
    if cgen.cpu.AVX2:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vmovdqa %s, yword[%s]\n' % (ymm1, reg3)
        code += 'vpshufd %s, %s, 0x08\n' % (ymm1, ymm1)
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm2, reg3)
        code += 'vpshufd %s, %s, 0x08\n' % (ymm2, ymm2)
        code += 'vpunpcklqdq %s, %s, %s\n' % (ymm1, ymm1, ymm2)
        code += 'vpermq %s, %s, 0xD8\n' % (ymm1, ymm1)
        code += 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, ymm1)
        cgen.release_reg(ymm1)
        cgen.release_reg(ymm2)
        return code, reg1, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (xmm3, reg3)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm4, reg3)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        code += 'vmovdqa %s, oword[%s]\n' % (xmm1, reg1)
        code += 'vmovdqa %s, oword[%s]\n' % (xmm2, reg2)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)

        code += 'vmovdqa %s, oword[%s + 32]\n' % (xmm3, reg3)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'vmovdqa %s, oword[%s + 48]\n' % (xmm4, reg3)
        code += 'vpshufd %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (xmm4, reg2)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm2, xmm4, xmm2, xmm3)

        cgen.release_reg(xmm3)
        cgen.release_reg(xmm4)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movdqa %s, oword[%s]\n' % (xmm3, reg3)
        code += 'pshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm4, reg3)
        code += 'pshufd %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        code += 'movdqa %s, oword[%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, oword[%s]\n' % (xmm2, reg2)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)

        code += 'movdqa %s, oword[%s + 32]\n' % (xmm3, reg3)
        code += 'pshufd %s, %s, 0x08\n' % (xmm3, xmm3)
        code += 'movdqa %s, oword[%s + 48]\n' % (xmm4, reg3)
        code += 'pshufd %s, %s, 0x08\n' % (xmm4, xmm4)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'movdqa %s, oword[%s + 16]\n' % (xmm4, reg2)
        code += 'pand %s, %s\n' % (xmm2, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm4)
        code += 'por %s, %s\n' % (xmm2, xmm3)

        cgen.release_reg(xmm3)
        cgen.release_reg(xmm4)
        return code, (xmm1, xmm2), Int32x8Arg


def select_i32x16_i32x16_mi32x16(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa32 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int32x16Arg

    if cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        ymm, mask = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vmovaps %s, yword[%s]\n' % (ymm, reg2)
        code += 'vmovaps %s, yword[%s]\n' % (mask, reg3)
        code += 'vblendvps %s, %s, yword[%s], %s\n' % (ymm1, ymm, reg1, mask)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm, reg2)
        code += 'vmovaps %s, yword[%s + 32]\n' % (mask, reg3)
        code += 'vblendvps %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm, reg1, mask)
        cgen.release_reg(ymm)
        cgen.release_reg(mask)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm4, xmm5 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'vmovaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'vmovaps %s, oword[%s]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vpandn %s, %s, oword[%s]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'vmovaps %s, oword[%s + 16]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vpandn %s, %s, oword[%s + 16]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vmovaps %s, oword[%s + 32]\n' % (xmm4, reg1)
        code += 'vmovaps %s, oword[%s + 32]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm4, xmm4, xmm3)
        code += 'vpandn %s, %s, oword[%s + 32]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm4, xmm4, xmm3)
        code += 'vmovaps %s, oword[%s + 48]\n' % (xmm5, reg1)
        code += 'vmovaps %s, oword[%s + 48]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm5, xmm5, xmm3)
        code += 'vpandn %s, %s, oword[%s + 48]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm5, xmm5, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2, xmm4, xmm5), Int32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm4, xmm5 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'movaps %s, oword[%s]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, oword[%s]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm2, xmm3)
        code += 'pandn %s, oword[%s + 16]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm2, xmm3)
        code += 'movaps %s, oword[%s + 32]\n' % (xmm4, reg1)
        code += 'movaps %s, oword[%s + 32]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm4, xmm3)
        code += 'pandn %s, oword[%s + 32]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm4, xmm3)
        code += 'movaps %s, oword[%s + 48]\n' % (xmm5, reg1)
        code += 'movaps %s, oword[%s + 48]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm5, xmm3)
        code += 'pandn %s, oword[%s + 48]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm5, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2, xmm4, xmm5), Int32x16Arg


def select_f64x2_f64x2_mf64x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Float64x2Arg
    elif cgen.cpu.AVX:
        code = 'vblendvpd %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'andpd %s, %s\n' % (xmm1, xmm3)
        code += 'andnpd %s, %s\n' % (xmm3, xmm2)
        code += 'orpd %s, %s\n' % (xmm1, xmm3)
    return code, xmm1, Float64x2Arg


def select_f64x2_f64x2_mi32x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Float64x2Arg
    elif cgen.cpu.AVX:
        code = 'vpunpckldq %s, %s, %s\n' % (xmm3, xmm3, xmm3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'punpckldq %s, %s\n' % (xmm3, xmm3)
        code += 'andpd %s, %s\n' % (xmm1, xmm3)
        code += 'andnpd %s, %s\n' % (xmm3, xmm2)
        code += 'orpd %s, %s\n' % (xmm1, xmm3)

    return code, xmm1, Float64x2Arg


def select_f64x2_f64x2_mf32x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Float64x2Arg
    elif cgen.cpu.AVX:
        code = 'vunpcklps %s, %s, %s\n' % (xmm3, xmm3, xmm3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'unpcklps %s, %s\n' % (xmm3, xmm3)
        code += 'andpd %s, %s\n' % (xmm1, xmm3)
        code += 'andnpd %s, %s\n' % (xmm3, xmm2)
        code += 'orpd %s, %s\n' % (xmm1, xmm3)

    return code, xmm1, Float64x2Arg


def _select_f64x4_f64x4_mf64x4(cgen, reg1, reg2, reg3, arg_type):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, arg_type
    elif cgen.cpu.AVX:
        code = 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, arg_type
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movapd %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movapd %s, oword [%s]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm1, xmm3)
        code += 'andnpd %s, oword [%s]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm1, xmm3)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm2, xmm3)
        code += 'andnpd %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), arg_type


def select_f64x3_f64x3_mf64x3(cgen, reg1, reg2, reg3):
    return _select_f64x4_f64x4_mf64x4(cgen, reg1, reg2, reg3, Float64x3Arg)


def select_f64x4_f64x4_mf64x4(cgen, reg1, reg2, reg3):
    return _select_f64x4_f64x4_mf64x4(cgen, reg1, reg2, reg3, Float64x4Arg)


def _select_f64x4_f64x4_mi64x4(cgen, reg1, reg2, reg3, arg_type):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, arg_type
    elif cgen.cpu.AVX2:
        code = 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, arg_type
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm, reg3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, ymm)
        cgen.release_reg(ymm)
        return code, reg1, arg_type
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movapd %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movapd %s, oword [%s]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm1, xmm3)
        code += 'andnpd %s, oword [%s]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm1, xmm3)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm2, xmm3)
        code += 'andnpd %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), arg_type


def select_f64x3_f64x3_mi64x3(cgen, reg1, reg2, reg3):
    return _select_f64x4_f64x4_mi64x4(cgen, reg1, reg2, reg3, Float64x3Arg)


def select_f64x4_f64x4_mi64x4(cgen, reg1, reg2, reg3):
    return _select_f64x4_f64x4_mi64x4(cgen, reg1, reg2, reg3, Float64x4Arg)


def _select_f64x4_f64x4_mf32x4(cgen, reg1, reg2, reg3, arg_type):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, arg_type
    elif cgen.cpu.AVX2:
        mask = cgen.register('ymm')
        code = "vpmovsxdq %s, %s\n" % (mask, reg3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, mask)
        cgen.release_reg(mask)
        return code, reg1, arg_type
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vpunpckldq %s, %s, %s\n' % ('x' + ymm[1:], reg3, reg3)
        code += 'vpunpckhdq %s, %s, %s\n' % (reg3, reg3, reg3)
        code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm, ymm, reg3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, ymm)
        cgen.release_reg(ymm)
        return code, reg1, arg_type
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')
        code = 'movapd %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movapd %s, %s\n' % (mask, reg3)
        code += 'punpckldq %s, %s\n' % (reg3, reg3)
        code += 'andpd %s, %s\n' % (xmm1, reg3)
        code += 'andnpd %s, oword [%s]\n' % (reg3, reg2)
        code += 'orpd %s, %s\n' % (xmm1, reg3)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'punpckhdq %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm2, mask)
        code += 'andnpd %s, oword [%s + 16]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm2, mask)
        cgen.release_reg(mask)
        return code, (xmm1, xmm2), arg_type


def select_f64x3_f64x3_mf32x3(cgen, reg1, reg2, reg3):
    return _select_f64x4_f64x4_mf32x4(cgen, reg1, reg2, reg3, Float64x3Arg)


def select_f64x4_f64x4_mf32x4(cgen, reg1, reg2, reg3):
    return _select_f64x4_f64x4_mf32x4(cgen, reg1, reg2, reg3, Float64x4Arg)


def select_f64x8_f64x8_mf64x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vmovaps %s, yword[%s]\n' % (ymm, reg3)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, ymm)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm, reg3)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, ymm)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        xmm4, xmm5 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'movapd %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movapd %s, oword [%s]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm1, xmm3)
        code += 'andnpd %s, oword [%s]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm1, xmm3)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movapd %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm2, xmm3)
        code += 'andnpd %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm2, xmm3)
        code += 'movapd %s, oword [%s + 32]\n' % (xmm4, reg1)
        code += 'movapd %s, oword [%s + 32]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm4, xmm3)
        code += 'andnpd %s, oword [%s + 32]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm4, xmm3)
        code += 'movapd %s, oword [%s + 48]\n' % (xmm5, reg1)
        code += 'movapd %s, oword [%s + 48]\n' % (xmm3, reg3)
        code += 'andpd %s, %s\n' % (xmm5, xmm3)
        code += 'andnpd %s, oword [%s + 48]\n' % (xmm3, reg2)
        code += 'orpd %s, %s\n' % (xmm5, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2, xmm4, xmm5), Float64x8Arg


def select_f64x8_f64x8_mf32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        mask = cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovaps %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, mask)
        code += 'vextractf128 %s, %s, 1\n' % ('x' + reg3[1:], reg3)
        code += 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, mask)
        cgen.release_reg(mask)
        return code, (ymm1, ymm2), Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        mask = cgen.register('ymm')
        mask2 = cgen.register('xmm')
        code = 'vmovaps %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vpunpckldq %s, %s, %s\n' % ('x' + mask[1:], 'x' + reg3[1:], 'x' + reg3[1:])
        code += 'vpunpckhdq %s, %s, %s\n' % (mask2, 'x' + reg3[1:], 'x' + reg3[1:])
        code += 'vinsertf128 %s, %s, %s, 1\n' % (mask, mask, mask2)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, mask)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vextractf128 %s, %s, 1\n' % ('x' + reg3[1:], reg3)
        code += 'vpunpckldq %s, %s, %s\n' % ('x' + mask[1:], 'x' + reg3[1:], 'x' + reg3[1:])
        code += 'vpunpckhdq %s, %s, %s\n' % (mask2, 'x' + reg3[1:], 'x' + reg3[1:])
        code += 'vinsertf128 %s, %s, %s, 1\n' % (mask, mask, mask2)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, mask)
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')

        code = 'movapd %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movapd %s, oword[%s]\n' % (mask, reg3)
        code += 'unpcklps %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm1, mask)
        code += 'andnpd %s, oword [%s]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm1, mask)

        code += 'movapd %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movapd %s, oword[%s]\n' % (mask, reg3)
        code += 'unpckhps %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm2, mask)
        code += 'andnpd %s, oword [%s + 16]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm2, mask)

        code += 'movapd %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'movapd %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'unpcklps %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm3, mask)
        code += 'andnpd %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm3, mask)

        code += 'movapd %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += 'movapd %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'unpckhps %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm4, mask)
        code += 'andnpd %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm4, mask)

        cgen.release_reg(mask)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def select_f64x8_f64x8_mi32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovapd %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        mask = cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovaps %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, mask)
        code += 'vextracti128 %s, %s, 1\n' % ('x' + reg3[1:], reg3)
        code += 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, mask)
        cgen.release_reg(mask)
        return code, (ymm1, ymm2), Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        mask = cgen.register('ymm')
        mask2 = cgen.register('xmm')
        reg3_m = cgen.register('xmm')
        code = 'vmovdqa %s, oword[%s]\n' % (reg3_m, reg3)
        code += 'vmovaps %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vpunpckldq %s, %s, %s\n' % ('x' + mask[1:], reg3_m, reg3_m)
        code += 'vpunpckhdq %s, %s, %s\n' % (mask2, reg3_m, reg3_m)
        code += 'vinsertf128 %s, %s, %s, 1\n' % (mask, mask, mask2)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, mask)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (reg3_m, reg3)
        code += 'vpunpckldq %s, %s, %s\n' % ('x' + mask[1:], reg3_m, reg3_m)
        code += 'vpunpckhdq %s, %s, %s\n' % (mask2, reg3_m, reg3_m)
        code += 'vinsertf128 %s, %s, %s, 1\n' % (mask, mask, mask2)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, mask)
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
        cgen.release_reg(reg3_m)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')

        code = 'movapd %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movapd %s, oword[%s]\n' % (mask, reg3)
        code += 'punpckldq %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm1, mask)
        code += 'andnpd %s, oword [%s]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm1, mask)

        code += 'movapd %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movapd %s, oword[%s]\n' % (mask, reg3)
        code += 'punpckhdq %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm2, mask)
        code += 'andnpd %s, oword [%s + 16]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm2, mask)

        code += 'movapd %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'movapd %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'punpckldq %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm3, mask)
        code += 'andnpd %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm3, mask)

        code += 'movapd %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += 'movapd %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'punpckhdq %s, %s\n' % (mask, mask)
        code += 'andpd %s, %s\n' % (xmm4, mask)
        code += 'andnpd %s, oword [%s + 48]\n' % (mask, reg2)
        code += 'orpd %s, %s\n' % (xmm4, mask)

        cgen.release_reg(mask)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, ret_type):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, ret_type
    elif cgen.cpu.AVX:
        code = 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'andps %s, %s\n' % (xmm1, xmm3)
        code += 'andnps %s, %s\n' % (xmm3, xmm2)
        code += 'xorps %s, %s\n' % (xmm1, xmm3)
    return code, xmm1, ret_type


def select_f32x2_f32x2_mf32x2(cgen, xmm1, xmm2, xmm3):
    return _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, Float32x2Arg)


def select_f32x2_f32x2_mi32x2(cgen, xmm1, xmm2, xmm3):
    return _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, Float32x2Arg)


def select_f32x3_f32x3_mf32x3(cgen, xmm1, xmm2, xmm3):
    return _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, Float32x3Arg)


def select_f32x3_f32x3_mi32x3(cgen, xmm1, xmm2, xmm3):
    return _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, Float32x3Arg)


def select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3):
    return _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, Float32x4Arg)


def select_f32x4_f32x4_mi32x4(cgen, xmm1, xmm2, xmm3):
    return _select_f32x4_f32x4_mf32x4(cgen, xmm1, xmm2, xmm3, Float32x4Arg)


def select_f32x8_f32x8_mf32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float32x8Arg
    elif cgen.cpu.AVX:
        code = 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm1, xmm3)
        code += 'andnps %s, oword [%s]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm1, xmm3)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm2, xmm3)
        code += 'andnps %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), Float32x8Arg


def select_f32x8_f32x8_mi32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float32x8Arg
    elif cgen.cpu.AVX2:
        code = 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword [%s]\n' % (ymm, reg3)
        code += 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, ymm)
        cgen.release_reg(ymm)
        return code, reg1, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm1, xmm3)
        code += 'andnps %s, oword [%s]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm1, xmm3)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm2, xmm3)
        code += 'andnps %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), Float32x8Arg


def select_f32x16_f32x16_mf32x16(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        ymm = cgen.register('ymm')
        code = 'vmovaps %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vmovaps %s, yword[%s]\n' % (ymm, reg3)
        code += 'vblendvps %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, ymm)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vmovaps %s, yword[%s + 32]\n' % (ymm, reg3)
        code += 'vblendvps %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, ymm)
        cgen.release_reg(ymm)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        xmm4, xmm5 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'movaps %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movaps %s, oword [%s]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm1, xmm3)
        code += 'andnps %s, oword [%s]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm1, xmm3)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movaps %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm2, xmm3)
        code += 'andnps %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm2, xmm3)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm4, reg1)
        code += 'movaps %s, oword [%s + 32]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm4, xmm3)
        code += 'andnps %s, oword [%s + 32]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm4, xmm3)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm5, reg1)
        code += 'movaps %s, oword [%s + 48]\n' % (xmm3, reg3)
        code += 'andps %s, %s\n' % (xmm5, xmm3)
        code += 'andnps %s, oword [%s + 48]\n' % (xmm3, reg2)
        code += 'orps %s, %s\n' % (xmm5, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2, xmm4, xmm5), Float32x16Arg


def select_f32x2_f32x2_mf64x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Float32x2Arg
    elif cgen.cpu.AVX:
        code = "vpermilps %s, %s, 0x08\n" % (xmm3, xmm3)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = "shufps %s, %s, 0x08\n" % (xmm3, xmm3)
        code += 'andps %s, %s\n' % (xmm1, xmm3)
        code += 'andnps %s, %s\n' % (xmm3, xmm2)
        code += 'xorps %s, %s\n' % (xmm1, xmm3)
    return code, xmm1, Float32x2Arg


def select_f32x3_f32x3_mf64x3(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Float32x3Arg
    elif cgen.cpu.AVX2:
        code = 'vpermilps %s, %s, 0x08\n' % (reg, reg)
        code += 'vpermpd %s, %s, 0x08\n' % (reg, reg)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    elif cgen.cpu.AVX:
        tmp = cgen.register('xmm')
        code = 'vpermilps %s, %s, 0x08\n' % (reg, reg)
        code += 'vextractf128 %s, %s, 1\n' % (tmp, reg)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + reg[1:], 'x' + reg[1:], tmp)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
        cgen.release_reg(tmp)
    else:
        mask = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (mask, reg)
        code += 'shufps %s, %s, 0x08\n' % (mask, mask)
        code += 'movhps %s, qword[%s + 16]\n' % (mask, reg)
        code += 'andps %s, %s\n' % (xmm1, mask)
        code += 'andnps %s, %s\n' % (mask, xmm2)
        code += 'xorps %s, %s\n' % (xmm1, mask)
        cgen.release_reg(mask)
    return code, xmm1, Float32x3Arg


def select_f32x3_f32x3_mi64x3(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Float32x3Arg
    elif cgen.cpu.AVX2:
        code = 'vpermilps %s, %s, 0x08\n' % (reg, reg)
        code += 'vpermpd %s, %s, 0x08\n' % (reg, reg)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    elif cgen.cpu.AVX:
        mask = cgen.register('xmm')
        code = 'vpermilps %s, oword[%s], 0x08\n' % (mask, reg)
        code += 'vmovhps %s, %s, qword[%s + 16]\n' % (mask, mask, reg)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, mask)
        cgen.release_reg(mask)
    else:
        mask = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (mask, reg)
        code += 'shufps %s, %s, 0x08\n' % (mask, mask)
        code += 'movhps %s, qword[%s + 16]\n' % (mask, reg)
        code += 'andps %s, %s\n' % (xmm1, mask)
        code += 'andnps %s, %s\n' % (mask, xmm2)
        code += 'xorps %s, %s\n' % (xmm1, mask)
        cgen.release_reg(mask)
    return code, xmm1, Float32x3Arg


def select_f32x4_f32x4_mf64x4(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Float32x4Arg
    elif cgen.cpu.AVX2:
        code = 'vpermilps %s, %s, 0x08\n' % (reg, reg)
        code += 'vpermpd %s, %s, 0xD8\n' % (reg, reg)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    elif cgen.cpu.AVX:
        tmp = cgen.register('xmm')
        code = 'vpermilps %s, %s, 0x08\n' % (reg, reg)
        code += 'vextractf128 %s, %s, 1\n' % (tmp, reg)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + reg[1:], 'x' + reg[1:], tmp)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
        cgen.release_reg(tmp)
    else:
        mask = cgen.register('xmm')
        mask2 = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (mask, reg)
        code += 'shufps %s, %s, 0x08\n' % (mask, mask)
        code += 'movaps %s, oword[%s + 16]\n' % (mask2, reg)
        code += 'shufps %s, %s, 0x08\n' % (mask2, mask2)
        code += 'movlhps %s, %s\n' % (mask, mask2)
        code += 'andps %s, %s\n' % (xmm1, mask)
        code += 'andnps %s, %s\n' % (mask, xmm2)
        code += 'xorps %s, %s\n' % (xmm1, mask)
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
    return code, xmm1, Float32x4Arg


def select_f32x4_f32x4_mi64x4(cgen, xmm1, xmm2, reg):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (xmm2, reg, xmm1)
        return code, xmm2, Float32x4Arg
    elif cgen.cpu.AVX2:
        code = 'vpermilps %s, %s, 0x08\n' % (reg, reg)
        code += 'vpermpd %s, %s, 0xD8\n' % (reg, reg)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + reg[1:])
    elif cgen.cpu.AVX:
        tmp = cgen.register('xmm')
        mask = cgen.register('ymm')
        code = 'vpermilps %s, yword [%s], 0x08\n' % (mask, reg)
        code += 'vextractf128 %s, %s, 1\n' % (tmp, mask)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + mask[1:], 'x' + mask[1:], tmp)
        code += 'vblendvps %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, 'x' + mask[1:])
        cgen.release_reg(tmp)
        cgen.release_reg(mask)
    else:
        mask = cgen.register('xmm')
        mask2 = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (mask, reg)
        code += 'shufps %s, %s, 0x08\n' % (mask, mask)
        code += 'movaps %s, oword[%s + 16]\n' % (mask2, reg)
        code += 'shufps %s, %s, 0x08\n' % (mask2, mask2)
        code += 'movlhps %s, %s\n' % (mask, mask2)
        code += 'andps %s, %s\n' % (xmm1, mask)
        code += 'andnps %s, %s\n' % (mask, xmm2)
        code += 'xorps %s, %s\n' % (xmm1, mask)
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
    return code, xmm1, Float32x4Arg


def select_f32x8_f32x8_mf64x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovaps %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Float32x8Arg
    elif cgen.cpu.AVX:
        mask = cgen.register('ymm')
        mask2 = cgen.register('xmm')
        mask3 = cgen.register('xmm')
        code = 'vpermilps %s, oword[%s], 0x08\n' % ('x' + mask[1:], reg3)
        code += 'vpermilps %s, oword[%s + 16], 0x08\n' % (mask2, reg3)
        code += 'vmovlhps %s, %s, %s\n' % ('x' + mask[1:], 'x' + mask[1:], mask2)
        code += 'vpermilps %s, oword[%s + 32], 0x08\n' % (mask2, reg3)
        code += 'vpermilps %s, oword[%s + 48], 0x08\n' % (mask3, reg3)
        code += 'vmovlhps %s, %s, %s\n' % (mask2, mask2, mask3)
        code += 'vinsertf128 %s, %s, %s, 1\n' % (mask, mask, mask2)
        code += 'vblendvps %s, %s, %s, %s\n' % (reg1, reg2, reg1, mask)
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
        cgen.release_reg(mask3)
        return code, reg1, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        mask = cgen.register('xmm')
        mask2 = cgen.register('xmm')
        code = 'movaps %s, oword[%s]\n' % (mask, reg3)
        code += 'shufps %s, %s, 0x08\n' % (mask, mask)
        code += 'movaps %s, oword[%s + 16]\n' % (mask2, reg3)
        code += 'shufps %s, %s, 0x08\n' % (mask2, mask2)
        code += 'movaps %s, oword[%s]\n' % (xmm1, reg1)
        code += 'movaps %s, oword[%s]\n' % (xmm3, reg2)
        code += 'movlhps %s, %s\n' % (mask, mask2)
        code += 'andps %s, %s\n' % (xmm1, mask)
        code += 'andnps %s, %s\n' % (mask, xmm3)
        code += 'xorps %s, %s\n' % (xmm1, mask)

        code += 'movaps %s, oword[%s + 32]\n' % (mask, reg3)
        code += 'shufps %s, %s, 0x08\n' % (mask, mask)
        code += 'movaps %s, oword[%s + 48]\n' % (mask2, reg3)
        code += 'shufps %s, %s, 0x08\n' % (mask2, mask2)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm2, reg1)
        code += 'movaps %s, oword[%s + 16]\n' % (xmm3, reg2)
        code += 'movlhps %s, %s\n' % (mask, mask2)
        code += 'andps %s, %s\n' % (xmm2, mask)
        code += 'andnps %s, %s\n' % (mask, xmm3)
        code += 'xorps %s, %s\n' % (xmm2, mask)
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), Float32x8Arg


def select_i64x2_i64x2_mi64x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Int64x2Arg
    elif cgen.cpu.AVX:
        code = 'vblendvpd %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
    return code, xmm1, Int64x2Arg


def select_i64x2_i64x2_mf32x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Int64x2Arg
    elif cgen.cpu.AVX:
        code = 'vunpcklps %s, %s, %s\n' % (xmm3, xmm3, xmm3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'unpcklps %s, %s\n' % (xmm3, xmm3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)

    return code, xmm1, Int64x2Arg


def select_i64x2_i64x2_mi32x2(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (xmm2, xmm3, xmm1)
        return code, xmm2, Int64x2Arg
    elif cgen.cpu.AVX:
        code = 'vpunpckldq %s, %s, %s\n' % (xmm3, xmm3, xmm3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (xmm1, xmm2, xmm1, xmm3)
    else:
        code = 'punpckldq %s, %s\n' % (xmm3, xmm3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, %s\n' % (xmm3, xmm2)
        code += 'por %s, %s\n' % (xmm1, xmm3)

    return code, xmm1, Int64x2Arg


def _select_i64x4_i64x4_mf64x4(cgen, reg1, reg2, reg3, arg_type):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, arg_type
    elif cgen.cpu.AVX2:
        code = 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, arg_type
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'vmovdqa %s, %s\n' % (xmm3, 'x' + reg3[1:])
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vpandn %s, %s, oword [%s]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'vextractf128 %s, %s, 1\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vpandn %s, %s, oword [%s + 16]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), arg_type
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, oword [%s]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, oword [%s]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm2, xmm3)
        code += 'pandn %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), arg_type


def select_i64x3_i64x3_mf64x3(cgen, reg1, reg2, reg3):
    return _select_i64x4_i64x4_mf64x4(cgen, reg1, reg2, reg3, Int64x3Arg)


def _select_i64x4_i64x4_mi64x4(cgen, reg1, reg2, reg3, arg_type):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, arg_type
    elif cgen.cpu.AVX2:
        code = 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, reg3)
        return code, reg1, arg_type
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'vmovdqa %s, oword [%s]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vpandn %s, %s, oword [%s]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vpandn %s, %s, oword [%s + 16]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), arg_type
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, oword [%s]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, oword [%s]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm2, xmm3)
        code += 'pandn %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm2, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2), arg_type


def select_i64x3_i64x3_mi64x3(cgen, reg1, reg2, reg3):
    return _select_i64x4_i64x4_mi64x4(cgen, reg1, reg2, reg3, Int64x3Arg)


def _select_i64x4_i64x4_mf32x4(cgen, reg1, reg2, reg3, arg_type):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, arg_type
    elif cgen.cpu.AVX2:
        mask = cgen.register('ymm')
        code = "vpmovsxdq %s, %s\n" % (mask, reg3)
        code += 'vblendvpd %s, %s, %s, %s\n' % (reg1, reg2, reg1, mask)
        cgen.release_reg(mask)
        return code, reg1, arg_type
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'vmovdqa %s, %s\n' % (mask, reg3)
        code += 'vpunpckldq %s, %s, %s\n' % (reg3, reg3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, reg3)
        code += 'vpandn %s, %s, oword [%s]\n' % (reg3, reg3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, reg3)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'vpunpckhdq %s, %s, %s\n' % (mask, mask, mask)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, mask)
        code += 'vpandn %s, %s, oword [%s + 16]\n' % (mask, mask, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, mask)
        cgen.release_reg(mask)
        return code, (xmm1, xmm2), arg_type
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, %s\n' % (mask, reg3)
        code += 'punpckldq %s, %s\n' % (reg3, reg3)
        code += 'pand %s, %s\n' % (xmm1, reg3)
        code += 'pandn %s, oword [%s]\n' % (reg3, reg2)
        code += 'por %s, %s\n' % (xmm1, reg3)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'punpckhdq %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm2, mask)
        code += 'pandn %s, oword [%s + 16]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm2, mask)
        cgen.release_reg(mask)
        return code, (xmm1, xmm2), arg_type


def select_i64x3_i64x3_mf32x3(cgen, reg1, reg2, reg3):
    return _select_i64x4_i64x4_mf32x4(cgen, reg1, reg2, reg3, Int64x3Arg)


def select_i64x4_i64x4_mf64x4(cgen, reg1, reg2, reg3):
    return _select_i64x4_i64x4_mf64x4(cgen, reg1, reg2, reg3, Int64x4Arg)


def select_i64x4_i64x4_mi64x4(cgen, reg1, reg2, reg3):
    return _select_i64x4_i64x4_mi64x4(cgen, reg1, reg2, reg3, Int64x4Arg)


def select_i64x4_i64x4_mf32x4(cgen, reg1, reg2, reg3):
    return _select_i64x4_i64x4_mf32x4(cgen, reg1, reg2, reg3, Int64x4Arg)


def select_i64x8_i64x8_mi64x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        ymm = cgen.register('ymm')
        code = 'vmovdqa %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vmovdqa %s, yword[%s]\n' % (ymm, reg3)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, ymm)
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm, reg3)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, ymm)
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        xmm4, xmm5 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'vmovdqa %s, oword [%s]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vpandn %s, %s, oword [%s]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, xmm3)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vpandn %s, %s, oword [%s + 16]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, xmm3)
        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm4, reg1)
        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm4, xmm4, xmm3)
        code += 'vpandn %s, %s, oword [%s + 32]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm4, xmm4, xmm3)
        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm5, reg1)
        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm3, reg3)
        code += 'vpand %s, %s, %s\n' % (xmm5, xmm5, xmm3)
        code += 'vpandn %s, %s, oword [%s + 48]\n' % (xmm3, xmm3, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm5, xmm5, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2, xmm4, xmm5), Int64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3 = cgen.register('xmm')
        xmm4, xmm5 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, oword [%s]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm1, xmm3)
        code += 'pandn %s, oword [%s]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm1, xmm3)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movdqa %s, oword [%s + 16]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm2, xmm3)
        code += 'pandn %s, oword [%s + 16]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm2, xmm3)
        code += 'movdqa %s, oword [%s + 32]\n' % (xmm4, reg1)
        code += 'movdqa %s, oword [%s + 32]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm4, xmm3)
        code += 'pandn %s, oword [%s + 32]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm4, xmm3)
        code += 'movdqa %s, oword [%s + 48]\n' % (xmm5, reg1)
        code += 'movdqa %s, oword [%s + 48]\n' % (xmm3, reg3)
        code += 'pand %s, %s\n' % (xmm5, xmm3)
        code += 'pandn %s, oword [%s + 48]\n' % (xmm3, reg2)
        code += 'por %s, %s\n' % (xmm5, xmm3)
        cgen.release_reg(xmm3)
        return code, (xmm1, xmm2, xmm4, xmm5), Int64x8Arg


def select_i64x8_i64x8_mi32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        mask = cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovdqa %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, mask)
        code += 'vextractf128 %s, %s, 1\n' % ('x' + reg3[1:], reg3)
        code += 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, mask)
        cgen.release_reg(mask)
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')

        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'vmovdqa %s, oword[%s]\n' % (mask, reg3)
        code += 'vunpcklps %s, %s, %s\n' % (mask, mask, mask)
        code += 'vpand %s, %s, %s\n' % (xmm1, xmm1, mask)
        code += 'vpandn %s, %s, oword [%s]\n' % (mask, mask, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm1, xmm1, mask)

        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'vmovdqa %s, oword[%s]\n' % (mask, reg3)
        code += 'vunpckhps %s, %s, %s\n' % (mask, mask, mask)
        code += 'vpand %s, %s, %s\n' % (xmm2, xmm2, mask)
        code += 'vpandn %s, %s, oword [%s + 16]\n' % (mask, mask, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm2, xmm2, mask)

        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'vunpcklps %s, %s, %s\n' % (mask, mask, mask)
        code += 'vpand %s, %s, %s\n' % (xmm3, xmm3, mask)
        code += 'vpandn %s, %s, oword [%s + 32]\n' % (mask, mask, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm3, xmm3, mask)

        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += 'vmovdqa %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'vunpckhps %s, %s, %s\n' % (mask, mask, mask)
        code += 'vpand %s, %s, %s\n' % (xmm4, xmm4, mask)
        code += 'vpandn %s, %s, oword [%s + 32]\n' % (mask, mask, reg2)
        code += 'vpor %s, %s, %s\n' % (xmm4, xmm4, mask)

        cgen.release_reg(mask)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')

        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, oword[%s]\n' % (mask, reg3)
        code += 'unpcklps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm1, mask)
        code += 'pandn %s, oword [%s]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm1, mask)

        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movdqa %s, oword[%s]\n' % (mask, reg3)
        code += 'unpckhps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm2, mask)
        code += 'pandn %s, oword [%s + 16]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm2, mask)

        code += 'movdqa %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'movdqa %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'unpcklps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm3, mask)
        code += 'pandn %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm3, mask)

        code += 'movdqa %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += 'movdqa %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'unpckhps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm4, mask)
        code += 'pandn %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm4, mask)

        cgen.release_reg(mask)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg


def select_i64x8_i64x8_mf32x8(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX512F:
        code = "vmovdqa64 %s {%s}, %s\n" % (reg2, reg3, reg1)
        return code, reg2, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        mask = cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovdqa %s, yword[%s]\n' % (ymm1, reg2)
        code += 'vblendvpd %s, %s, yword[%s], %s\n' % (ymm1, ymm1, reg1, mask)
        code += 'vextractf128 %s, %s, 1\n' % ('x' + reg3[1:], reg3)
        code += 'vpmovsxdq %s, %s\n' % (mask, 'x' + reg3[1:])
        code += 'vmovdqa %s, yword[%s + 32]\n' % (ymm2, reg2)
        code += 'vblendvpd %s, %s, yword[%s + 32], %s\n' % (ymm2, ymm2, reg1, mask)
        cgen.release_reg(mask)
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('ymm')
        mask2 = cgen.register('ymm')
        code = 'vmovdqa %s, oword [%s]\n' % (xmm1, reg2)
        code += 'vunpcklps %s, %s, %s\n' % (mask, reg3, reg3)
        code += 'vblendvpd %s, %s, oword[%s], %s\n' % (xmm1, xmm1, reg1, 'x' + mask[1:])
        code += 'vunpckhps %s, %s, %s\n' % (mask2, reg3, reg3)
        code += 'vmovdqa %s, oword [%s + 16]\n' % (xmm2, reg2)
        code += 'vblendvpd %s, %s, oword[%s + 16], %s\n' % (xmm2, xmm2, reg1, 'x' + mask2[1:])
        code += 'vmovdqa %s, oword [%s + 32]\n' % (xmm3, reg2)
        code += 'vextractf128 %s, %s, 1\n' % ('x' + mask[1:], mask)
        code += 'vblendvpd %s, %s, oword[%s + 32], %s\n' % (xmm3, xmm3, reg1, 'x' + mask[1:])
        code += 'vmovdqa %s, oword [%s + 48]\n' % (xmm4, reg2)
        code += 'vextractf128 %s, %s, 1\n' % ('x' + mask2[1:], mask2)
        code += 'vblendvpd %s, %s, oword[%s + 48], %s\n' % (xmm4, xmm4, reg1, 'x' + mask2[1:])
        cgen.release_reg(mask)
        cgen.release_reg(mask2)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        mask = cgen.register('xmm')

        code = 'movdqa %s, oword [%s]\n' % (xmm1, reg1)
        code += 'movdqa %s, oword[%s]\n' % (mask, reg3)
        code += 'unpcklps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm1, mask)
        code += 'pandn %s, oword [%s]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm1, mask)

        code += 'movdqa %s, oword [%s + 16]\n' % (xmm2, reg1)
        code += 'movdqa %s, oword[%s]\n' % (mask, reg3)
        code += 'unpckhps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm2, mask)
        code += 'pandn %s, oword [%s + 16]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm2, mask)

        code += 'movdqa %s, oword [%s + 32]\n' % (xmm3, reg1)
        code += 'movdqa %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'unpcklps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm3, mask)
        code += 'pandn %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm3, mask)

        code += 'movdqa %s, oword [%s + 48]\n' % (xmm4, reg1)
        code += 'movdqa %s, oword[%s + 16]\n' % (mask, reg3)
        code += 'unpckhps %s, %s\n' % (mask, mask)
        code += 'pand %s, %s\n' % (xmm4, mask)
        code += 'pandn %s, oword [%s + 32]\n' % (mask, reg2)
        code += 'por %s, %s\n' % (xmm4, mask)

        cgen.release_reg(mask)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg

register_built_in('select', (Int32x2Arg, Int32x2Arg, MaskI32x2Arg), select_i32x2_i32x2_mi32x2)
register_built_in('select', (Int32x2Arg, Int32x2Arg, MaskF32x2Arg), select_i32x2_i32x2_mi32x2)
register_built_in('select', (Int32x2Arg, Int32x2Arg, MaskI64x2Arg), select_i32x2_i32x2_mi64x2)
register_built_in('select', (Int32x2Arg, Int32x2Arg, MaskF64x2Arg), select_i32x2_i32x2_mf64x2)
register_built_in('select', (Int32x3Arg, Int32x3Arg, MaskI32x3Arg), select_i32x3_i32x3_mi32x3)
register_built_in('select', (Int32x3Arg, Int32x3Arg, MaskF32x3Arg), select_i32x3_i32x3_mi32x3)
register_built_in('select', (Int32x3Arg, Int32x3Arg, MaskI64x3Arg), select_i32x3_i32x3_mi64x3)
register_built_in('select', (Int32x3Arg, Int32x3Arg, MaskF64x3Arg), select_i32x3_i32x3_mf64x3)
register_built_in('select', (Int32x4Arg, Int32x4Arg, MaskI32x4Arg), select_i32x4_i32x4_mi32x4)
register_built_in('select', (Int32x4Arg, Int32x4Arg, MaskF32x4Arg), select_i32x4_i32x4_mi32x4)
register_built_in('select', (Int32x4Arg, Int32x4Arg, MaskI64x4Arg), select_i32x4_i32x4_mi64x4)
register_built_in('select', (Int32x4Arg, Int32x4Arg, MaskF64x4Arg), select_i32x4_i32x4_mf64x4)
register_built_in('select', (Int32x8Arg, Int32x8Arg, MaskI32x8Arg), select_i32x8_i32x8_mi32x8)
register_built_in('select', (Int32x8Arg, Int32x8Arg, MaskF32x8Arg), select_i32x8_i32x8_mf32x8)
register_built_in('select', (Int32x8Arg, Int32x8Arg, MaskI64x8Arg), select_i32x8_i32x8_mi64x8)
register_built_in('select', (Int32x8Arg, Int32x8Arg, MaskF64x8Arg), select_i32x8_i32x8_mf64x8)
register_built_in('select', (Int32x16Arg, Int32x16Arg, MaskI32x16Arg), select_i32x16_i32x16_mi32x16)
register_built_in('select', (Int32x16Arg, Int32x16Arg, MaskF32x16Arg), select_i32x16_i32x16_mi32x16)

register_built_in('select', (Float64x2Arg, Float64x2Arg, MaskF64x2Arg), select_f64x2_f64x2_mf64x2)
register_built_in('select', (Float64x2Arg, Float64x2Arg, MaskI64x2Arg), select_f64x2_f64x2_mf64x2)
register_built_in('select', (Float64x2Arg, Float64x2Arg, MaskI32x2Arg), select_f64x2_f64x2_mi32x2)
register_built_in('select', (Float64x2Arg, Float64x2Arg, MaskF32x2Arg), select_f64x2_f64x2_mf32x2)
register_built_in('select', (Float64x3Arg, Float64x3Arg, MaskF64x3Arg), select_f64x3_f64x3_mf64x3)
register_built_in('select', (Float64x3Arg, Float64x3Arg, MaskI64x3Arg), select_f64x3_f64x3_mi64x3)
register_built_in('select', (Float64x3Arg, Float64x3Arg, MaskF32x3Arg), select_f64x3_f64x3_mf32x3)
register_built_in('select', (Float64x3Arg, Float64x3Arg, MaskI32x3Arg), select_f64x3_f64x3_mf32x3)
register_built_in('select', (Float64x4Arg, Float64x4Arg, MaskF64x4Arg), select_f64x4_f64x4_mf64x4)
register_built_in('select', (Float64x4Arg, Float64x4Arg, MaskI64x4Arg), select_f64x4_f64x4_mi64x4)
register_built_in('select', (Float64x4Arg, Float64x4Arg, MaskF32x4Arg), select_f64x4_f64x4_mf32x4)
register_built_in('select', (Float64x4Arg, Float64x4Arg, MaskI32x4Arg), select_f64x4_f64x4_mf32x4)
register_built_in('select', (Float64x8Arg, Float64x8Arg, MaskF64x8Arg), select_f64x8_f64x8_mf64x8)
register_built_in('select', (Float64x8Arg, Float64x8Arg, MaskI64x8Arg), select_f64x8_f64x8_mf64x8)
register_built_in('select', (Float64x8Arg, Float64x8Arg, MaskF32x8Arg), select_f64x8_f64x8_mf32x8)
register_built_in('select', (Float64x8Arg, Float64x8Arg, MaskI32x8Arg), select_f64x8_f64x8_mi32x8)

register_built_in('select', (Float32x2Arg, Float32x2Arg, MaskF32x2Arg), select_f32x2_f32x2_mf32x2)
register_built_in('select', (Float32x2Arg, Float32x2Arg, MaskI32x2Arg), select_f32x2_f32x2_mi32x2)
register_built_in('select', (Float32x2Arg, Float32x2Arg, MaskF64x2Arg), select_f32x2_f32x2_mf64x2)
register_built_in('select', (Float32x2Arg, Float32x2Arg, MaskI64x2Arg), select_f32x2_f32x2_mf64x2)

register_built_in('select', (Float32x3Arg, Float32x3Arg, MaskF32x3Arg), select_f32x3_f32x3_mf32x3)
register_built_in('select', (Float32x3Arg, Float32x3Arg, MaskI32x3Arg), select_f32x3_f32x3_mi32x3)
register_built_in('select', (Float32x3Arg, Float32x3Arg, MaskF64x3Arg), select_f32x3_f32x3_mf64x3)
register_built_in('select', (Float32x3Arg, Float32x3Arg, MaskI64x3Arg), select_f32x3_f32x3_mi64x3)

register_built_in('select', (Float32x4Arg, Float32x4Arg, MaskF32x4Arg), select_f32x4_f32x4_mf32x4)
register_built_in('select', (Float32x4Arg, Float32x4Arg, MaskI32x4Arg), select_f32x4_f32x4_mi32x4)
register_built_in('select', (Float32x4Arg, Float32x4Arg, MaskF64x4Arg), select_f32x4_f32x4_mf64x4)
register_built_in('select', (Float32x4Arg, Float32x4Arg, MaskI64x4Arg), select_f32x4_f32x4_mi64x4)
register_built_in('select', (Float32x8Arg, Float32x8Arg, MaskF32x8Arg), select_f32x8_f32x8_mf32x8)
register_built_in('select', (Float32x8Arg, Float32x8Arg, MaskI32x8Arg), select_f32x8_f32x8_mi32x8)
register_built_in('select', (Float32x8Arg, Float32x8Arg, MaskF64x8Arg), select_f32x8_f32x8_mf64x8)
register_built_in('select', (Float32x8Arg, Float32x8Arg, MaskI64x8Arg), select_f32x8_f32x8_mf64x8)
register_built_in('select', (Float32x16Arg, Float32x16Arg, MaskF32x16Arg), select_f32x16_f32x16_mf32x16)
register_built_in('select', (Float32x16Arg, Float32x16Arg, MaskI32x16Arg), select_f32x16_f32x16_mf32x16)

register_built_in('select', (Int64x2Arg, Int64x2Arg, MaskF64x2Arg), select_i64x2_i64x2_mi64x2)
register_built_in('select', (Int64x2Arg, Int64x2Arg, MaskI64x2Arg), select_i64x2_i64x2_mi64x2)
register_built_in('select', (Int64x2Arg, Int64x2Arg, MaskI32x2Arg), select_i64x2_i64x2_mi32x2)
register_built_in('select', (Int64x2Arg, Int64x2Arg, MaskF32x2Arg), select_i64x2_i64x2_mf32x2)
register_built_in('select', (Int64x3Arg, Int64x3Arg, MaskF64x3Arg), select_i64x3_i64x3_mf64x3)
register_built_in('select', (Int64x3Arg, Int64x3Arg, MaskI64x3Arg), select_i64x3_i64x3_mi64x3)
register_built_in('select', (Int64x3Arg, Int64x3Arg, MaskF32x3Arg), select_i64x3_i64x3_mf32x3)
register_built_in('select', (Int64x3Arg, Int64x3Arg, MaskI32x3Arg), select_i64x3_i64x3_mf32x3)
register_built_in('select', (Int64x4Arg, Int64x4Arg, MaskF64x4Arg), select_i64x4_i64x4_mf64x4)
register_built_in('select', (Int64x4Arg, Int64x4Arg, MaskI64x4Arg), select_i64x4_i64x4_mi64x4)
register_built_in('select', (Int64x4Arg, Int64x4Arg, MaskF32x4Arg), select_i64x4_i64x4_mf32x4)
register_built_in('select', (Int64x4Arg, Int64x4Arg, MaskI32x4Arg), select_i64x4_i64x4_mf32x4)
register_built_in('select', (Int64x8Arg, Int64x8Arg, MaskF64x8Arg), select_i64x8_i64x8_mi64x8)
register_built_in('select', (Int64x8Arg, Int64x8Arg, MaskI64x8Arg), select_i64x8_i64x8_mi64x8)
register_built_in('select', (Int64x8Arg, Int64x8Arg, MaskF32x8Arg), select_i64x8_i64x8_mf32x8)
register_built_in('select', (Int64x8Arg, Int64x8Arg, MaskI32x8Arg), select_i64x8_i64x8_mi32x8)
