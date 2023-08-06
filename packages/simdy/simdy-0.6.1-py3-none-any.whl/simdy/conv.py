
from .holders import Name, Const
from .cgen import register_built_in
from .int_arg import Int32Arg, Int64Arg
from .flt_arg import Float32Arg, float32
from .dbl_arg import Float64Arg, float64
from .dbl_vec_arg import float64x2, float64x3, float64x4, float64x8,\
    Float64x2Arg, Float64x3Arg, Float64x4Arg, Float64x8Arg
from .flt_vec_arg import Float32x2Arg, Float32x3Arg, Float32x4Arg,\
    Float32x8Arg, float32x2, float32x3, float32x4, float32x8, float32x16, Float32x16Arg
from .int_vec_arg import Int32x2Arg, Int32x3Arg, Int32x4Arg, Int32x8Arg,\
    Int32x16Arg, Int64x2Arg, int64x2, Int64x3Arg, Int64x4Arg, Int64x8Arg,\
    int64x3, int64x4, int64x8, int32x2, int32x3, int32x4, int32x8, int32x16


__all__ = []


def int32_empty(cgen):
    reg = cgen.register('general')
    code = cgen.gen.load_i32(reg, value=0)
    return code, reg, Int32Arg


def int32_name(cgen, op_name):
    arg = cgen.get_arg(op_name)
    if isinstance(arg, Int32Arg):
        code, reg, arg_type = arg.load_cmd(cgen)
    elif isinstance(arg, Float32Arg):
        reg = cgen.register('general')
        code = cgen.gen.conv_f32_to_i32(reg, name=arg.name)
    elif isinstance(arg, Float64Arg):
        reg = cgen.register('general')
        code = cgen.gen.conv_f64_to_i32(reg, name=arg.name)
    elif isinstance(arg, Int64Arg):
        reg = cgen.register('general64')
        code, reg, arg_type = arg.load_cmd(cgen)
        reg = cgen.regs.t_64_to_32(reg)
    else:
        raise TypeError("Callable int doesn't support argument ", arg)
    return code, reg, Int32Arg


def int32_const(cgen, con):
    reg = cgen.register('general')
    value = int(con.value)
    if value > 2147483647 or value < -2147483648:
        raise ValueError("int32 constant %i is two big." % value)
    code = cgen.gen.load_i32(reg, value=value)
    return code, reg, Int32Arg


def int32_i32(cgen, reg):
    return '', reg, Int32Arg


def int32_i64(cgen, reg):
    dest_reg = cgen.register('general')
    code = 'mov %s, %s\n' % (dest_reg, cgen.regs.t_64_to_32(reg))
    return code, dest_reg, Int32Arg


def int32_f32(cgen, xmm):
    reg = cgen.register('general')
    code = cgen.gen.conv_f32_to_i32(reg, xmm=xmm)
    return code, reg, Int32Arg


def int32_f64(cgen, xmm):
    reg = cgen.register('general')
    code = cgen.gen.conv_f64_to_i32(reg, xmm=xmm)
    return code, reg, Int32Arg


register_built_in('int32', tuple(), int32_empty)
register_built_in('int32', (Name,), int32_name)
register_built_in('int32', (Const,), int32_const)
register_built_in('int32', (Int32Arg,), int32_i32)
register_built_in('int32', (Int64Arg,), int32_i64)
register_built_in('int32', (Float32Arg,), int32_f32)
register_built_in('int32', (Float64Arg,), int32_f64)


def int64_empty(cgen):
    reg = cgen.register('general64')
    code = 'xor %s, %s\n' % (reg, reg)
    return code, reg, Int64Arg


def int64_name(cgen, op_name):
    arg = cgen.get_arg(op_name)
    if isinstance(arg, Int32Arg):
        reg = cgen.register('general64')
        code = 'movsx %s, dword[%s]\n' % (reg, arg.name)
    elif isinstance(arg, Float32Arg):
        reg = cgen.register('general64')
        code = cgen.gen.conv_f32_to_i64(reg, name=arg.name)
    elif isinstance(arg, Float64Arg):
        reg = cgen.register('general64')
        code = cgen.gen.conv_f64_to_i64(reg, name=arg.name)
    elif isinstance(arg, Int64Arg):
        code, reg, arg_type = arg.load_cmd(cgen)
    else:
        raise TypeError("Callable int doesn't support argument ", arg)
    return code, reg, Int64Arg


def int64_const(cgen, con):
    reg = cgen.register('general64')
    value = int(con.value)
    if value > 9223372036854775807 or value < -9223372036854775808:
        raise ValueError("int64 constant %i is two big." % value)
    code = cgen.gen.load_i64(reg, value=value)
    return code, reg, Int64Arg


def int64_i32(cgen, reg):
    dest_reg = cgen.register('general64')
    code = 'movsx %s, %s\n' % (dest_reg, reg)
    return code, dest_reg, Int64Arg


def int64_i64(cgen, reg):
    return '', reg, Int64Arg


def int64_f32(cgen, xmm):
    reg = cgen.register('general64')
    code = cgen.gen.conv_f32_to_i64(reg, xmm=xmm)
    return code, reg, Int64Arg


def int64_f64(cgen, xmm):
    reg = cgen.register('general64')
    code = cgen.gen.conv_f64_to_i64(reg, xmm=xmm)
    return code, reg, Int64Arg


register_built_in('int64', tuple(), int64_empty)
register_built_in('int64', (Name,), int64_name)
register_built_in('int64', (Const,), int64_const)
register_built_in('int64', (Int32Arg,), int64_i32)
register_built_in('int64', (Int64Arg,), int64_i64)
register_built_in('int64', (Float32Arg,), int64_f32)
register_built_in('int64', (Float64Arg,), int64_f64)


def float64_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vxorps %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'xorps %s, %s\n' % (xmm, xmm)
    return code, xmm, Float64Arg


def float64_name(cgen, op_name):
    arg = cgen.get_arg(op_name)
    if isinstance(arg, Int32Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i32_to_f64(xmm, name=arg.name)
    elif isinstance(arg, Float32Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f32_to_f64(xmm, name=arg.name)
    elif isinstance(arg, Float64Arg):
        code, xmm, arg_type = arg.load_cmd(cgen)
    elif isinstance(arg, Int64Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i64_to_f64(xmm, name=arg.name)
    else:
        raise TypeError("Callable int doesn't support argument ", arg)
    return code, xmm, Float64Arg


def float64_const(cgen, con):
    value = float64(con.value)
    if value == 0.0:
        return float64_empty(cgen)
    arg = Float64Arg(value=value)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64_f32(cgen, xmm):
    xmm2 = cgen.register('xmm')
    code = cgen.gen.conv_f32_to_f64(xmm2, xmm)
    return code, xmm2, Float64Arg


def float64_i64(cgen, reg):
    xmm = cgen.register('xmm')
    code = cgen.gen.conv_i64_to_f64(xmm, src_reg=reg)
    return code, xmm, Float64Arg


def float64_i32(cgen, reg):
    xmm = cgen.register('xmm')
    code = cgen.gen.conv_i32_to_f64(xmm, src_reg=reg)
    return code, xmm, Float64Arg


def float64_f64(cgen, xmm):
    return '', xmm, Float64Arg


register_built_in('float64', tuple(), float64_empty)
register_built_in('float64', (Name,), float64_name)
register_built_in('float64', (Const,), float64_const)
register_built_in('float64', (Int32Arg,), float64_i32)
register_built_in('float64', (Int64Arg,), float64_i64)
register_built_in('float64', (Float32Arg,), float64_f32)
register_built_in('float64', (Float64Arg,), float64_f64)


def float32_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vxorps %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'xorps %s, %s\n' % (xmm, xmm)
    return code, xmm, Float32Arg


def float32_name(cgen, op_name):
    arg = cgen.get_arg(op_name)
    if isinstance(arg, Int32Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i32_to_f32(xmm, name=arg.name)
    elif isinstance(arg, Float32Arg):
        code, xmm, arg_type = arg.load_cmd(cgen)
    elif isinstance(arg, Float64Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f64_to_f32(xmm, name=arg.name)
    elif isinstance(arg, Int64Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i64_to_f32(xmm, name=arg.name)
    else:
        raise TypeError("Callable int doesn't support argument ", arg)
    return code, xmm, Float32Arg


def float32_const(cgen, con):
    value = float32(con.value)
    if value == 0.0:
        return float32_empty(cgen)
    arg = Float32Arg(value=value)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32_i32(cgen, reg):
    xmm = cgen.register('xmm')
    code = cgen.gen.conv_i32_to_f32(xmm, src_reg=reg)
    return code, xmm, Float32Arg


def float32_i64(cgen, reg):
    xmm = cgen.register('xmm')
    code = cgen.gen.conv_i64_to_f32(xmm, src_reg=reg)
    return code, xmm, Float32Arg


def float32_f32(cgen, xmm):
    return '', xmm, Float32Arg


def float32_f64(cgen, xmm):
    xmm2 = cgen.register('xmm')
    code = cgen.gen.conv_f64_to_f32(xmm2, src_xmm=xmm)
    return code, xmm2, Float32Arg


register_built_in('float32', tuple(), float32_empty)
register_built_in('float32', (Name,), float32_name)
register_built_in('float32', (Const,), float32_const)
register_built_in('float32', (Int32Arg,), float32_i32)
register_built_in('float32', (Int64Arg,), float32_i64)
register_built_in('float32', (Float32Arg,), float32_f32)
register_built_in('float32', (Float64Arg,), float32_f64)


def float64x2_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vxorps %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'xorps %s, %s\n' % (xmm, xmm)
    return code, xmm, Float64x2Arg


def float64x2_const(cgen, con):
    if con.value == 0.0:
        return float64x2_empty(cgen)
    arg = Float64x2Arg(value=float64x2(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x2_const_const(cgen, con1, con2):
    val = float64x2(con1.value, con2.value)
    arg = Float64x2Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x2_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float64Arg):
        code, xmm, arg_typ = arg.load_cmd(cgen)
        code += cgen.gen.broadcast_f64(xmm)
        return code, xmm, Float64x2Arg
    elif isinstance(arg, Float64x2Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Float32x2Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f32x2_to_f64x2(xmm, name=arg.name)
        return code, xmm, Float64x2Arg
    elif isinstance(arg, Int32x2Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i32x2_to_f64x2(xmm, name=arg.name)
        return code, xmm, Float64x2Arg
    else:
        raise TypeError("Callable float64x2 doesn't support argument ", arg)


def float64x2_f64(cgen, xmm):
    code = cgen.gen.broadcast_f64(xmm)
    return code, xmm, Float64x2Arg


def float64x2_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if not (isinstance(arg1, Float64Arg) and isinstance(arg2, Float64Arg)):
        raise TypeError("Callable float64x2 doesn't support arguments ", arg1, arg2)

    code, xmm, arg_typ = arg1.load_cmd(cgen)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vmovhpd %s, %s, qword [%s]\n' % (xmm, xmm, arg2.name)
    else:
        code += 'movhpd %s, qword [%s]\n' % (xmm, arg2.name)
    return code, xmm, Float64x2Arg


def float64x2_f64_f64(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovlhps %s, %s, %s\n' % (xmm1, xmm1, xmm2)
    else:
        code = 'movlhps %s, %s\n' % (xmm1, xmm2)
    return code, xmm1, Float64x2Arg


def float64x2_f64x2(cgen, xmm):
    return '', xmm, Float64x2Arg


def float64x2_i32x2(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_i32x2_to_f64x2(xmm1, xmm=xmm)
    return code, xmm1, Float64x2Arg


def float64x2_f32x2(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_f32x2_to_f64x2(xmm1, xmm=xmm)
    return code, xmm1, Float64x2Arg


register_built_in('float64x2', tuple(), float64x2_empty)
register_built_in('float64x2', (Const,), float64x2_const)
register_built_in('float64x2', (Const, Const), float64x2_const_const)
register_built_in('float64x2', (Name,), float64x2_name)
register_built_in('float64x2', (Float64Arg,), float64x2_f64)
register_built_in('float64x2', (Name, Name), float64x2_name_name)
register_built_in('float64x2', (Float64Arg, Float64Arg), float64x2_f64_f64)
register_built_in('float64x2', (Float64x2Arg,), float64x2_f64x2)
register_built_in('float64x2', (Int32x2Arg,), float64x2_i32x2)
register_built_in('float64x2', (Float32x2Arg,), float64x2_f32x2)


def float64x3_empty(cgen):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vxorps %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Float64x3Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'xorps %s, %s\n' % (xmms[0], xmms[0])
        code += 'xorps %s, %s\n' % (xmms[1], xmms[1])
        return code, xmms, Float64x3Arg


def float64x3_const(cgen, con):
    if con.value == 0.0:
        return float64x3_empty(cgen)
    arg = Float64x3Arg(value=float64x3(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x3_constx3(cgen, con1, con2, con3):
    val = float64x3(con1.value, con2.value, con3.value)
    arg = Float64x3Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x3_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float64Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vbroadcastsd %s, qword[%s]\n' % (ymm, arg.name)
            return code, ymm, Float64x3Arg
        else:
            xmm1 = cgen.register('xmm')
            code, xmm, arg_typ = arg.load_cmd(cgen)
            code += cgen.gen.broadcast_f64(xmm)
            code += cgen.gen.move_reg(xmm1, xmm)
            return code, (xmm, xmm1), Float64x3Arg
    elif isinstance(arg, Float64x3Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Float32x3Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvtps2pd %s, oword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float64x3Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'cvtps2pd %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'cvtss2sd %s, dword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Float64x3Arg
    elif isinstance(arg, Int32x3Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvtdq2pd %s, oword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float64x3Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'cvtdq2pd %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'cvtsi2sd %s, dword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Float64x3Arg
    else:
        raise TypeError("Callable float64x3 doesn't support argument ", arg)


def float64x3_f64(cgen, xmm):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vbroadcastsd %s, %s\n' % (ymm, xmm)
        return code, ymm, Float64x3Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = cgen.gen.broadcast_f64(xmm)
        code += 'vperm2f128 %s, %s, %s, 0\n' % (ymm, 'y' + xmm[1:], 'y' + xmm[1:])
        return code, ymm, Float64x3Arg
    else:
        xmm1 = cgen.register('xmm')
        code = cgen.gen.broadcast_f64(xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        return code, (xmm, xmm1), Float64x3Arg


def float64x3_f64x3(cgen, reg):
    if cgen.cpu.AVX:
        return '', reg, Float64x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_f64x2(xmm1, ptr_reg=reg)
        code += cgen.gen.load_f64(xmm2, ptr_reg=reg, offset=16)
        return code, (xmm1, xmm2), Float64x3Arg


def float64x3_i32x3(cgen, xmm):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvtdq2pd %s, %s\n' % (ymm, xmm)
        return code, ymm, Float64x3Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = cgen.gen.conv_i32x2_to_f64x2(xmm1, xmm=xmm)
        code += "movhlps %s, %s\n" % (xmm2, xmm)
        code += cgen.gen.conv_i32x2_to_f64x2(xmm2, xmm=xmm2)
        return code, (xmm1, xmm2), Float64x3Arg


def float64x3_f32x3(cgen, xmm):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvtps2pd %s, %s\n' % (ymm, xmm)
        return code, ymm, Float64x3Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = cgen.gen.conv_f32x2_to_f64x2(xmm1, xmm=xmm)
        code += "movhlps %s, %s\n" % (xmm2, xmm)
        code += 'cvtss2sd %s, %s\n' % (xmm2, xmm2)
        return code, (xmm1, xmm2), Float64x3Arg


def float64x3_namex3(cgen, name1, name2, name3):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)

    if not (isinstance(arg1, Float64Arg) and isinstance(arg2, Float64Arg) and isinstance(arg3, Float64Arg)):
        raise TypeError("Callable float64x3 doesn't support arguments ", arg1, arg2, arg3)

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vmovsd %s, qword [%s]\n' % ('x' + ymm1[1:], arg1.name)
        code += 'vmovhpd %s, %s, qword [%s]\n' % ('x' + ymm1[1:], 'x' + ymm1[1:], arg2.name)
        code += 'vmovsd %s, qword [%s]\n' % ('x' + ymm2[1:], arg3.name)
        if cgen.cpu.AVX512F:
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm1, ymm1, 'x' + ymm2[1:])
        else:
            code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm1, ymm1, 'x' + ymm2[1:])
        cgen.release_reg(ymm2)
        return code, ymm1, Float64x3Arg
    else:
        code, xmm1, arg_typ = arg1.load_cmd(cgen)
        code += 'movhpd %s, qword [%s]\n' % (xmm1, arg2.name)
        co, xmm2, arg_typ = arg3.load_cmd(cgen)
        return code + co, (xmm1, xmm2), Float64x3Arg


def float64x3_f64_f64_f64(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vmovlhps %s, %s, %s\n' % ('x' + ymm[1:], xmm1, xmm2)
        if cgen.cpu.AVX512F:
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        else:
            code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        return code, ymm, Float64x3Arg
    else:
        code = 'movlhps %s, %s\n' % (xmm1, xmm2)
        return code, (xmm1, xmm3), Float64x3Arg


def float64x3_f64x2_f64(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vinsertf64x2 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
        code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        return code, ymm, Float64x3Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        return code, ymm, Float64x3Arg
    else:
        return '', (xmm1, xmm2), Float64x3Arg


def float64x3_namex2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Float64x2Arg) and isinstance(arg2, Float64Arg):
        code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
        code2, xmm2, arg_typ2 = arg2.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            if cgen.cpu.AVX512F:
                code3 = 'vinsertf64x2 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
                code3 += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
            else:
                code3 = 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
            cgen.release_reg(xmm1)
            cgen.release_reg(xmm2)
            return code1 + code2 + code3, ymm, Float64x3Arg
        else:
            return code1 + code2, (xmm1, xmm2), Float64x3Arg
    else:
        raise ValueError("float64x3 doesn't support arguments.", arg1, arg2)


register_built_in('float64x3', tuple(), float64x3_empty)
register_built_in('float64x3', (Const,), float64x3_const)
register_built_in('float64x3', (Const, Const, Const), float64x3_constx3)
register_built_in('float64x3', (Name,), float64x3_name)
register_built_in('float64x3', (Float64Arg,), float64x3_f64)
register_built_in('float64x3', (Float64x3Arg,), float64x3_f64x3)
register_built_in('float64x3', (Int32x3Arg,), float64x3_i32x3)
register_built_in('float64x3', (Float32x3Arg,), float64x3_f32x3)
register_built_in('float64x3', (Name, Name, Name), float64x3_namex3)
register_built_in('float64x3', (Float64Arg, Float64Arg, Float64Arg), float64x3_f64_f64_f64)
register_built_in('float64x3', (Float64x2Arg, Float64Arg), float64x3_f64x2_f64)
register_built_in('float64x3', (Name, Name), float64x3_namex2)


def float64x4_empty(cgen):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vxorps %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Float64x4Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'xorps %s, %s\n' % (xmms[0], xmms[0])
        code += 'xorps %s, %s\n' % (xmms[1], xmms[1])
        return code, xmms, Float64x4Arg


def float64x4_const(cgen, con):
    if con.value == 0.0:
        return float64x4_empty(cgen)
    arg = Float64x4Arg(value=float64x4(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x4_constx4(cgen, con1, con2, con3, con4):
    val = float64x4(con1.value, con2.value, con3.value, con4.value)
    arg = Float64x4Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x4_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float64Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vbroadcastsd %s, qword[%s]\n' % (ymm, arg.name)
            return code, ymm, Float64x4Arg
        else:
            xmm1 = cgen.register('xmm')
            code, xmm, arg_typ = arg.load_cmd(cgen)
            code += cgen.gen.broadcast_f64(xmm)
            code += cgen.gen.move_reg(xmm1, xmm)
            return code, (xmm, xmm1), Float64x4Arg
    elif isinstance(arg, Float64x4Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Float32x4Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvtps2pd %s, oword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float64x4Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'cvtps2pd %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'cvtps2pd %s, qword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Float64x4Arg
    elif isinstance(arg, Int32x4Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvtdq2pd %s, oword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float64x4Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'cvtdq2pd %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'cvtdq2pd %s, qword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Float64x4Arg
    else:
        raise TypeError("Callable float64x4 doesn't support argument ", arg)


def float64x4_f64(cgen, xmm):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vbroadcastsd %s, %s\n' % (ymm, xmm)
        return code, ymm, Float64x4Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = cgen.gen.broadcast_f64(xmm)
        code += 'vperm2f128 %s, %s, %s, 0\n' % (ymm, 'y' + xmm[1:], 'y' + xmm[1:])
        return code, ymm, Float64x4Arg
    else:
        xmm1 = cgen.register('xmm')
        code = cgen.gen.broadcast_f64(xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        return code, (xmm, xmm1), Float64x4Arg


def float64x4_f64x4(cgen, reg):
    if cgen.cpu.AVX:
        return '', reg, Float64x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_f64x2(xmm1, ptr_reg=reg)
        code += cgen.gen.load_f64x2(xmm2, ptr_reg=reg, offset=16)
        return code, (xmm1, xmm2), Float64x4Arg


def float64x4_i32x4(cgen, xmm):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvtdq2pd %s, %s\n' % (ymm, xmm)
        return code, ymm, Float64x4Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = cgen.gen.conv_i32x2_to_f64x2(xmm1, xmm=xmm)
        code += "movhlps %s, %s\n" % (xmm2, xmm)
        code += cgen.gen.conv_i32x2_to_f64x2(xmm2, xmm=xmm2)
        return code, (xmm1, xmm2), Float64x4Arg


def float64x4_f32x4(cgen, xmm):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvtps2pd %s, %s\n' % (ymm, xmm)
        return code, ymm, Float64x4Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = cgen.gen.conv_f32x2_to_f64x2(xmm1, xmm=xmm)
        code += "movhlps %s, %s\n" % (xmm2, xmm)
        code += cgen.gen.conv_f32x2_to_f64x2(xmm2, xmm=xmm2)
        return code, (xmm1, xmm2), Float64x4Arg


def float64x4_namex4(cgen, name1, name2, name3, name4):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)
    arg4 = cgen.get_arg(name4)

    if not (isinstance(arg1, Float64Arg) and isinstance(arg2, Float64Arg) and
            isinstance(arg3, Float64Arg) and isinstance(arg4, Float64Arg)):
        raise TypeError("Callable float64x4 doesn't support arguments ", arg1, arg2, arg3, arg4)

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vmovsd %s, qword [%s]\n' % ('x' + ymm1[1:], arg1.name)
        code += 'vmovhpd %s, %s, qword [%s]\n' % ('x' + ymm1[1:], 'x' + ymm1[1:], arg2.name)
        code += 'vmovsd %s, qword [%s]\n' % ('x' + ymm2[1:], arg3.name)
        code += 'vmovhpd %s, %s, qword [%s]\n' % ('x' + ymm2[1:], 'x' + ymm2[1:], arg4.name)
        if cgen.cpu.AVX512F:
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm1, ymm1, 'x' + ymm2[1:])
        else:
            code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm1, ymm1, 'x' + ymm2[1:])
        cgen.release_reg(ymm2)
        return code, ymm1, Float64x4Arg
    else:
        code, xmm1, arg_typ = arg1.load_cmd(cgen)
        code += 'movhpd %s, qword [%s]\n' % (xmm1, arg2.name)
        co, xmm2, arg_typ = arg3.load_cmd(cgen)
        code += co
        code += 'movhpd %s, qword [%s]\n' % (xmm2, arg4.name)
        return code, (xmm1, xmm2), Float64x4Arg


def float64x4_f64_f64_f64_f64(cgen, xmm1, xmm2, xmm3, xmm4):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vmovlhps %s, %s, %s\n' % ('x' + ymm[1:], xmm1, xmm2)
        code += 'vmovlhps %s, %s, %s\n' % (xmm3, xmm3, xmm4)
        if cgen.cpu.AVX512F:
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        else:
            code += 'vinsertf128 %s, %s, %s, 1\n' % (ymm, ymm, xmm3)
        return code, ymm, Float64x4Arg
    else:
        code = 'movlhps %s, %s\n' % (xmm1, xmm2)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        return code, (xmm1, xmm3), Float64x4Arg


def float64x4_namex2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Float64x2Arg) and isinstance(arg2, Float64x2Arg):
        code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
        code2, xmm2, arg_typ2 = arg2.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            if cgen.cpu.AVX512F:
                code3 = 'vinsertf64x2 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
                code3 += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
            else:
                code3 = 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
            cgen.release_reg(xmm1)
            cgen.release_reg(xmm2)
            return code1 + code2 + code3, ymm, Float64x4Arg
        else:
            return code1 + code2, (xmm1, xmm2), Float64x4Arg
    else:
        raise ValueError("float64x4 doesn't support arguments.", arg1, arg2)


def float64x4_f64x2_f64x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        if cgen.cpu.AVX512F:
            code = 'vinsertf64x2 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
            code += 'vinsertf64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        else:
            code = 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        return code, ymm, Float64x4Arg
    else:
        return '', (xmm1, xmm2), Float64x4Arg


register_built_in('float64x4', tuple(), float64x4_empty)
register_built_in('float64x4', (Const,), float64x4_const)
register_built_in('float64x4', (Const, Const, Const, Const), float64x4_constx4)
register_built_in('float64x4', (Name,), float64x4_name)
register_built_in('float64x4', (Float64Arg,), float64x4_f64)
register_built_in('float64x4', (Float64x4Arg,), float64x4_f64x4)
register_built_in('float64x4', (Int32x4Arg,), float64x4_i32x4)
register_built_in('float64x4', (Float32x4Arg,), float64x4_f32x4)
register_built_in('float64x4', (Name, Name, Name, Name), float64x4_namex4)
register_built_in('float64x4', (Float64Arg, Float64Arg, Float64Arg, Float64Arg), float64x4_f64_f64_f64_f64)
# register_built_in('float64x4', (Float64x3Arg, Float64Arg), float64x4_f64x3_f64)
register_built_in('float64x4', (Name, Name), float64x4_namex2)
register_built_in('float64x4', (Float64x2Arg, Float64x2Arg), float64x4_f64x2_f64x2)


def float64x8_empty(cgen):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vxorps %s, %s, %s\n' % (zmm, zmm, zmm)
        return code, zmm, Float64x8Arg
    elif cgen.cpu.AVX:
        ymms = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vxorps %s, %s, %s\n' % (ymms[0], ymms[0], ymms[0])
        code += 'vxorps %s, %s, %s\n' % (ymms[1], ymms[1], ymms[1])
        return code, ymms, Float64x8Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = 'xorps %s, %s\n' % (xmms[0], xmms[0])
        code += 'xorps %s, %s\n' % (xmms[1], xmms[1])
        code += 'xorps %s, %s\n' % (xmms[2], xmms[2])
        code += 'xorps %s, %s\n' % (xmms[3], xmms[3])
        return code, xmms, Float64x8Arg


def float64x8_const(cgen, con):
    if con.value == 0.0:
        return float64x8_empty(cgen)
    arg = Float64x8Arg(value=float64x8(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x8_constx8(cgen, con1, con2, con3, con4, con5, con6, con7, con8):
    val = float64x8(con1.value, con2.value, con3.value, con4.value,
                    con5.value, con6.value, con7.value, con8.value)
    arg = Float64x8Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float64x8_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float64Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vbroadcastsd %s, qword[%s]\n' % (zmm, arg.name)
            return code, zmm, Float64x8Arg
        elif cgen.cpu.AVX:
            ymm1 = cgen.register('ymm')
            ymm2 = cgen.register('ymm')
            code = 'vbroadcastsd %s, qword[%s]\n' % (ymm1, arg.name)
            code += cgen.gen.move_reg(ymm2, ymm1)
            return code, (ymm1, ymm2), Float64x8Arg
        else:
            xmm2, xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm')
            code, xmm1, arg_typ = arg.load_cmd(cgen)
            code += cgen.gen.broadcast_f64(xmm1)
            code += cgen.gen.move_reg(xmm2, xmm1)
            code += cgen.gen.move_reg(xmm3, xmm1)
            code += cgen.gen.move_reg(xmm4, xmm1)
            return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg
    elif isinstance(arg, Float64x8Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Float32x8Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vcvtps2pd %s, yword [%s]\n' % (zmm, arg.name)
            return code, zmm, Float64x8Arg
        elif cgen.cpu.AVX:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = 'vcvtps2pd %s, oword [%s]\n' % (ymm1, arg.name)
            code += 'vcvtps2pd %s, oword [%s + 16]\n' % (ymm2, arg.name)
            return code, (ymm1, ymm2), Float64x8Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = 'cvtps2pd %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'cvtps2pd %s, qword [%s + 8]\n' % (xmm2, arg.name)
            code += 'cvtps2pd %s, qword [%s + 16]\n' % (xmm3, arg.name)
            code += 'cvtps2pd %s, qword [%s + 24]\n' % (xmm4, arg.name)
            return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg
    elif isinstance(arg, Int32x8Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vcvtdq2pd %s, yword [%s]\n' % (zmm, arg.name)
            return code, zmm, Float64x8Arg
        elif cgen.cpu.AVX:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = 'vcvtdq2pd %s, oword [%s]\n' % (ymm1, arg.name)
            code += 'vcvtdq2pd %s, oword [%s + 16]\n' % (ymm2, arg.name)
            return code, (ymm1, ymm2), Float64x8Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = 'cvtdq2pd %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'cvtdq2pd %s, qword [%s + 8]\n' % (xmm2, arg.name)
            code += 'cvtdq2pd %s, qword [%s + 16]\n' % (xmm3, arg.name)
            code += 'cvtdq2pd %s, qword [%s + 24]\n' % (xmm4, arg.name)
            return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg
    else:
        raise TypeError("Callable float64x8 doesn't support argument ", arg)


def float64x8_f64(cgen, xmm):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vbroadcastsd %s, %s\n' % (zmm, xmm)
        return code, zmm, Float64x8Arg
    elif cgen.cpu.AVX2:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vbroadcastsd %s, %s\n' % (ymm1, xmm)
        code += cgen.gen.move_reg(ymm2, ymm1)
        return code, (ymm1, ymm2), Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = cgen.gen.broadcast_f64(xmm)
        code += 'vperm2f128 %s, %s, %s, 0\n' % (ymm1, 'y' + xmm[1:], 'y' + xmm[1:])
        code += cgen.gen.move_reg(ymm2, ymm1)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        xmm3 = cgen.register('xmm')
        code = cgen.gen.broadcast_f64(xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        code += cgen.gen.move_reg(xmm2, xmm)
        code += cgen.gen.move_reg(xmm3, xmm)
        return code, (xmm, xmm1, xmm2, xmm3), Float64x8Arg


def float64x8_f64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        return '', reg, Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = cgen.gen.load_f64x4(ymm1, ptr_reg=reg)
        code += cgen.gen.load_f64x4(ymm2, ptr_reg=reg, offset=32)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_f64x2(xmm1, ptr_reg=reg)
        code += cgen.gen.load_f64x2(xmm2, ptr_reg=reg, offset=16)
        code += cgen.gen.load_f64x2(xmm3, ptr_reg=reg, offset=32)
        code += cgen.gen.load_f64x2(xmm4, ptr_reg=reg, offset=48)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def float64x8_i32x8(cgen, reg):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vcvtdq2pd %s, %s\n' % (zmm, reg)
        return code, zmm, Float64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vcvtdq2pd %s, %s\n' % (ymm1, 'x' + reg[1:])
        code += 'vextracti128 %s, %s, 1\n' % ('x' + ymm2[1:], reg)
        code += 'vcvtdq2pd %s, %s\n' % (ymm2, 'x' + ymm2[1:])
        return code, (ymm1, ymm2), Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vcvtdq2pd %s, oword [%s]\n' % (ymm1, reg)
        code += 'vcvtdq2pd %s, oword [%s + 16]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'cvtdq2pd %s, qword [%s]\n' % (xmm1, reg)
        code += 'cvtdq2pd %s, qword [%s + 8]\n' % (xmm2, reg)
        code += 'cvtdq2pd %s, qword [%s + 16]\n' % (xmm3, reg)
        code += 'cvtdq2pd %s, qword [%s + 24]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def float64x8_f32x8(cgen, reg):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vcvtps2pd %s, %s\n' % (zmm, reg)
        return code, zmm, Float64x8Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vcvtps2pd %s, %s\n' % (ymm1, 'x' + reg[1:])
        code += 'vextractf128 %s, %s, 1\n' % ('x' + ymm2[1:], reg)
        code += 'vcvtps2pd %s, %s\n' % (ymm2, 'x' + ymm2[1:])
        return code, (ymm1, ymm2), Float64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'cvtps2pd %s, qword [%s]\n' % (xmm1, reg)
        code += 'cvtps2pd %s, qword [%s + 8]\n' % (xmm2, reg)
        code += 'cvtps2pd %s, qword [%s + 16]\n' % (xmm3, reg)
        code += 'cvtps2pd %s, qword [%s + 24]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


def float64x8_namex2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Float64x4Arg) and isinstance(arg2, Float64x4Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vinsertf64x4 %s, %s, yword [%s], 0\n' % (zmm, zmm, arg1.name)
            code += 'vinsertf64x4 %s, %s, yword [%s], 1\n' % (zmm, zmm, arg2.name)
            return code, zmm, Float64x8Arg
        elif cgen.cpu.AVX:
            code1, ymm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, ymm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (ymm1, ymm2), Float64x8Arg
        else:
            code1, xmms1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmms2, arg_typ2 = arg2.load_cmd(cgen)
            xmms = xmms1 + xmms2
            return code1 + code2, xmms, Float64x8Arg
    else:
        raise ValueError("float64x8 doesn't support arguments.", arg1, arg2)


def float64x8_f64x4_f64x4(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vinsertf64x4 %s, %s, %s, 0\n' % (zmm, zmm, reg1)
        code += 'vinsertf64x4 %s, %s, %s, 1\n' % (zmm, zmm, reg2)
        return code, zmm, Float64x8Arg
    elif cgen.cpu.AVX:
        return '', (reg1, reg2), Float64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = cgen.gen.load_f64x2(xmm1, ptr_reg=reg1)
        code += cgen.gen.load_f64x2(xmm2, ptr_reg=reg1, offset=16)
        code += cgen.gen.load_f64x2(xmm3, ptr_reg=reg2)
        code += cgen.gen.load_f64x2(xmm4, ptr_reg=reg2, offset=16)
        return code, (xmm1, xmm2, xmm3, xmm4), Float64x8Arg


register_built_in('float64x8', tuple(), float64x8_empty)
register_built_in('float64x8', (Const,), float64x8_const)
register_built_in('float64x8', (Const, Const, Const, Const, Const, Const, Const, Const), float64x8_constx8)
register_built_in('float64x8', (Name,), float64x8_name)
register_built_in('float64x8', (Float64Arg,), float64x8_f64)
register_built_in('float64x8', (Float64x8Arg,), float64x8_f64x8)
register_built_in('float64x8', (Int32x8Arg,), float64x8_i32x8)
register_built_in('float64x8', (Float32x8Arg,), float64x8_f32x8)
register_built_in('float64x8', (Name, Name), float64x8_namex2)
register_built_in('float64x8', (Float64x4Arg, Float64x4Arg), float64x8_f64x4_f64x4)


def float32x2_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vxorps %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'xorps %s, %s\n' % (xmm, xmm)
    return code, xmm, Float32x2Arg


def float32x2_const(cgen, con):
    if con.value == 0.0:
        return float32x2_empty(cgen)
    arg = Float32x2Arg(value=float32x2(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x2_const_const(cgen, con1, con2):
    val = float32x2(con1.value, con2.value)
    arg = Float32x2Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x2_f32(cgen, xmm):
    code = cgen.gen.broadcast_f32(xmm)
    return code, xmm, Float32x2Arg


def float32x2_f32x2(cgen, xmm):
    return '', xmm, Float32x2Arg


def float32x2_i32x2(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_i32x4_to_f32x4(xmm1, xmm=xmm)
    return code, xmm1, Float32x2Arg


def float32x2_f64x2(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_f64x2_to_f32x2(xmm1, xmm=xmm)
    return code, xmm1, Float32x2Arg


def float32x2_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float32Arg):
        code, xmm, arg_typ = arg.load_cmd(cgen)
        code += cgen.gen.broadcast_f32(xmm)
        return code, xmm, Float32x2Arg
    elif isinstance(arg, Float64x2Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f64x2_to_f32x2(xmm, name=arg.name)
        return code, xmm, Float32x2Arg
    elif isinstance(arg, Float32x2Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int32x2Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i32x4_to_f32x4(xmm, name=arg.name)
        return code, xmm, Float32x2Arg
    else:
        raise TypeError("Callable float32x2 doesn't support argument ", arg)


def float32x2_f32_f32(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vinsertps %s, %s, %s, 0x10\n' % (xmm1, xmm1, xmm2)
    else:
        code = 'insertps %s, %s, 0x10\n' % (xmm1, xmm2)
    return code, xmm1, Float32x2Arg


def float32x2_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if not (isinstance(arg1, Float32Arg) and isinstance(arg2, Float32Arg)):
        raise TypeError("Callable float32x2 doesn't support arguments ", arg1, arg2)

    code, xmm, arg_typ = arg1.load_cmd(cgen)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, dword [%s], 0x10\n' % (xmm, xmm, arg2.name)
    else:
        code += 'insertps %s, dword [%s], 0x10\n' % (xmm, arg2.name)
    return code, xmm, Float32x2Arg


register_built_in('float32x2', tuple(), float32x2_empty)
register_built_in('float32x2', (Const,), float32x2_const)
register_built_in('float32x2', (Const, Const), float32x2_const_const)
register_built_in('float32x2', (Name,), float32x2_name)
register_built_in('float32x2', (Float32Arg,), float32x2_f32)
register_built_in('float32x2', (Float32x2Arg,), float32x2_f32x2)
register_built_in('float32x2', (Int32x2Arg,), float32x2_i32x2)
register_built_in('float32x2', (Float64x2Arg,), float32x2_f64x2)
register_built_in('float32x2', (Name, Name), float32x2_name_name)
register_built_in('float32x2', (Float32Arg, Float32Arg), float32x2_f32_f32)


def float32x3_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vxorps %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'xorps %s, %s\n' % (xmm, xmm)
    return code, xmm, Float32x3Arg


def float32x3_const(cgen, con):
    if con.value == 0.0:
        return float32x3_empty(cgen)
    arg = Float32x3Arg(value=float32x3(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x3_constx3(cgen, con1, con2, con3):
    val = float32x3(con1.value, con2.value, con3.value)
    arg = Float32x3Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x3_f32(cgen, xmm):
    code = cgen.gen.broadcast_f32(xmm)
    return code, xmm, Float32x3Arg


def float32x3_f32x3(cgen, xmm):
    return '', xmm, Float32x3Arg


def float32x3_i32x3(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_i32x4_to_f32x4(xmm1, xmm=xmm)
    return code, xmm1, Float32x3Arg


def float32x3_f64x3(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        xmm = cgen.register('xmm')
        code = "vcvtpd2ps %s, %s\n" % (xmm, reg)
        return code, xmm, Float32x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvtpd2ps %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvtpd2ps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'insertps %s, %s, 0x20\n' % (xmm1, xmm2)
        cgen.release_reg(xmm2)
        return code, xmm1, Float32x3Arg


def float32x3_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float32Arg):
        code, xmm, arg_typ = arg.load_cmd(cgen)
        code += cgen.gen.broadcast_f32(xmm)
        return code, xmm, Float32x3Arg
    elif isinstance(arg, Float64x3Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            xmm = cgen.register('xmm')
            code = "vcvtpd2ps %s, yword [%s]\n" % (xmm, arg.name)
            return code, xmm, Float32x3Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'cvtpd2ps %s, oword [%s]\n' % (xmm1, arg.name)
            code += 'cvtpd2ps %s, oword [%s + 16]\n' % (xmm2, arg.name)
            code += 'insertps %s, %s, 0x20\n' % (xmm1, xmm2)
            cgen.release_reg(xmm2)
            return code, xmm1, Float32x3Arg
    elif isinstance(arg, Float32x3Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int32x3Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i32x4_to_f32x4(xmm, name=arg.name)
        return code, xmm, Float32x3Arg
    else:
        raise TypeError("Callable float32x3 doesn't support argument ", arg)


def float32x3_f32_f32_f32(cgen, xmm1, xmm2, xmm3):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vinsertps %s, %s, %s, 0x10\n' % (xmm1, xmm1, xmm2)
        code += 'vinsertps %s, %s, %s, 0x20\n' % (xmm1, xmm1, xmm3)
    else:
        code = 'insertps %s, %s, 0x10\n' % (xmm1, xmm2)
        code += 'insertps %s, %s, 0x20\n' % (xmm1, xmm3)
    return code, xmm1, Float32x3Arg


def float32x3_name_x3(cgen, name1, name2, name3):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)

    if not (isinstance(arg1, Float32Arg) and isinstance(arg2, Float32Arg) and isinstance(arg3, Float32Arg)):
        raise TypeError("Callable float32x3 doesn't support arguments ", arg1, arg2, arg3)

    code, xmm, arg_typ = arg1.load_cmd(cgen)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, dword [%s], 0x10\n' % (xmm, xmm, arg2.name)
        code += 'vinsertps %s, %s, dword [%s], 0x20\n' % (xmm, xmm, arg3.name)
    else:
        code += 'insertps %s, dword [%s], 0x10\n' % (xmm, arg2.name)
        code += 'insertps %s, dword [%s], 0x20\n' % (xmm, arg3.name)
    return code, xmm, Float32x3Arg


def float32x3_f32x2_f32(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vinsertps %s, %s, %s, 0x20\n' % (xmm1, xmm1, xmm2)
    else:
        code = 'insertps %s, %s, 0x20\n' % (xmm1, xmm2)
    return code, xmm1, Float32x3Arg


def float32x3_name_x2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if not (isinstance(arg1, Float32x2Arg) and isinstance(arg2, Float32Arg)):
        raise TypeError("Callable float32x3 doesn't support arguments ", arg1, arg2)

    code, xmm, arg_typ = arg1.load_cmd(cgen)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, dword [%s], 0x20\n' % (xmm, xmm, arg2.name)
    else:
        code += 'insertps %s, dword [%s], 0x20\n' % (xmm, arg2.name)
    return code, xmm, Float32x3Arg


register_built_in('float32x3', tuple(), float32x3_empty)
register_built_in('float32x3', (Const,), float32x3_const)
register_built_in('float32x3', (Const, Const, Const), float32x3_constx3)
register_built_in('float32x3', (Name,), float32x3_name)
register_built_in('float32x3', (Float32Arg,), float32x3_f32)
register_built_in('float32x3', (Float32x3Arg,), float32x3_f32x3)
register_built_in('float32x3', (Int32x3Arg,), float32x3_i32x3)
register_built_in('float32x3', (Float64x3Arg,), float32x3_f64x3)
register_built_in('float32x3', (Name, Name, Name), float32x3_name_x3)
register_built_in('float32x3', (Float32Arg, Float32Arg, Float32Arg), float32x3_f32_f32_f32)
register_built_in('float32x3', (Float32x2Arg, Float32Arg), float32x3_f32x2_f32)
register_built_in('float32x3', (Name, Name), float32x3_name_x2)


def float32x4_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vxorps %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'xorps %s, %s\n' % (xmm, xmm)
    return code, xmm, Float32x4Arg


def float32x4_const(cgen, con):
    if con.value == 0.0:
        return float32x4_empty(cgen)
    arg = Float32x4Arg(value=float32x4(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x4_const_x4(cgen, con1, con2, con3, con4):
    val = float32x4(con1.value, con2.value, con3.value, con4.value)
    arg = Float32x4Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x4_f32(cgen, xmm):
    code = cgen.gen.broadcast_f32(xmm)
    return code, xmm, Float32x4Arg


def float32x4_f32x4(cgen, xmm):
    return '', xmm, Float32x4Arg


def float32x4_i32x4(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_i32x4_to_f32x4(xmm1, xmm=xmm)
    return code, xmm1, Float32x4Arg


def float32x4_f64x4(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        xmm = cgen.register('xmm')
        code = "vcvtpd2ps %s, %s\n" % (xmm, reg)
        return code, xmm, Float32x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvtpd2ps %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvtpd2ps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'movlhps %s, %s\n' % (xmm1, xmm2)
        cgen.release_reg(xmm2)
        return code, xmm1, Float32x4Arg


def float32x4_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float32Arg):
        code, xmm, arg_typ = arg.load_cmd(cgen)
        code += cgen.gen.broadcast_f32(xmm)
        return code, xmm, Float32x4Arg
    elif isinstance(arg, Float64x4Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            xmm = cgen.register('xmm')
            code = "vcvtpd2ps %s, yword [%s]\n" % (xmm, arg.name)
            return code, xmm, Float32x4Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'cvtpd2ps %s, oword [%s]\n' % (xmm1, arg.name)
            code += 'cvtpd2ps %s, oword [%s + 16]\n' % (xmm2, arg.name)
            code += 'movlhps %s, %s\n' % (xmm1, xmm2)
            cgen.release_reg(xmm2)
            return code, xmm1, Float32x4Arg
    elif isinstance(arg, Float32x4Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int32x4Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_i32x4_to_f32x4(xmm, name=arg.name)
        return code, xmm, Float32x4Arg
    else:
        raise TypeError("Callable float32x4 doesn't support argument ", arg)


def float32x4_name_x4(cgen, name1, name2, name3, name4):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)
    arg4 = cgen.get_arg(name4)

    if not (isinstance(arg1, Float32Arg) and isinstance(arg2, Float32Arg) and
            isinstance(arg3, Float32Arg) and isinstance(arg4, Float32Arg)):
        raise TypeError("Callable float32x4 doesn't support arguments ", arg1, arg2, arg3, arg4)

    code, xmm, arg_typ = arg1.load_cmd(cgen)
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code += 'vinsertps %s, %s, dword [%s], 0x10\n' % (xmm, xmm, arg2.name)
        code += 'vinsertps %s, %s, dword [%s], 0x20\n' % (xmm, xmm, arg3.name)
        code += 'vinsertps %s, %s, dword [%s], 0x30\n' % (xmm, xmm, arg4.name)
    else:
        code += 'insertps %s, dword [%s], 0x10\n' % (xmm, arg2.name)
        code += 'insertps %s, dword [%s], 0x20\n' % (xmm, arg3.name)
        code += 'insertps %s, dword [%s], 0x30\n' % (xmm, arg4.name)
    return code, xmm, Float32x4Arg


def float32x4_f32_x4(cgen, xmm1, xmm2, xmm3, xmm4):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vinsertps %s, %s, %s, 0x10\n' % (xmm1, xmm1, xmm2)
        code += 'vinsertps %s, %s, %s, 0x20\n' % (xmm1, xmm1, xmm3)
        code += 'vinsertps %s, %s, %s, 0x30\n' % (xmm1, xmm1, xmm4)
    else:
        code = 'insertps %s, %s, 0x10\n' % (xmm1, xmm2)
        code += 'insertps %s, %s, 0x20\n' % (xmm1, xmm3)
        code += 'insertps %s, %s, 0x30\n' % (xmm1, xmm4)
    return code, xmm1, Float32x4Arg


def float32x4_f32x2_f32x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovlhps %s, %s, %s\n' % (xmm1, xmm1, xmm2)
    else:
        code = 'movlhps %s, %s\n' % (xmm1, xmm2)
    return code, xmm1, Float32x4Arg


def float32x4_f32x3_f32(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vinsertps %s, %s, %s, 0x30\n' % (xmm1, xmm1, xmm2)
    else:
        code = 'insertps %s, %s, 0x30\n' % (xmm1, xmm2)
    return code, xmm1, Float32x4Arg


def float32x4_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Float32x2Arg) and isinstance(arg2, Float32x2Arg):
        code, xmm, arg_typ = arg1.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code += 'vmovhpd %s, %s, qword [%s]\n' % (xmm, xmm, arg2.name)
        else:
            code += 'movhpd %s, qword [%s]\n' % (xmm, arg2.name)
        return code, xmm, Float32x4Arg
    elif isinstance(arg1, Float32x3Arg) and isinstance(arg2, Float32Arg):
        code, xmm, arg_typ = arg1.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code += 'vinsertps %s, %s, dword [%s], 0x30\n' % (xmm, xmm, arg2.name)
        else:
            code += 'insertps %s, dword [%s], 0x30\n' % (xmm, arg2.name)
        return code, xmm, Float32x4Arg
    else:
        raise TypeError("Callable float32x4 doesn't support arguments ", arg1, arg2)


register_built_in('float32x4', tuple(), float32x4_empty)
register_built_in('float32x4', (Const,), float32x4_const)
register_built_in('float32x4', (Const, Const, Const, Const), float32x4_const_x4)
register_built_in('float32x4', (Float32Arg,), float32x4_f32)
register_built_in('float32x4', (Float64x4Arg,), float32x4_f64x4)
register_built_in('float32x4', (Int32x4Arg,), float32x4_i32x4)
register_built_in('float32x4', (Float32x4Arg,), float32x4_f32x4)
register_built_in('float32x4', (Name,), float32x4_name)
register_built_in('float32x4', (Name, Name, Name, Name), float32x4_name_x4)
register_built_in('float32x4', (Float32Arg, Float32Arg, Float32Arg, Float32Arg), float32x4_f32_x4)
register_built_in('float32x4', (Float32x2Arg, Float32x2Arg), float32x4_f32x2_f32x2)
register_built_in('float32x4', (Float32x3Arg, Float32Arg), float32x4_f32x3_f32)
register_built_in('float32x4', (Name, Name), float32x4_name_name)


def float32x8_empty(cgen):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vxorps %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Float32x8Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'xorps %s, %s\n' % (xmms[0], xmms[0])
        code += 'xorps %s, %s\n' % (xmms[1], xmms[1])
        return code, xmms, Float32x8Arg


def float32x8_const(cgen, con):
    if con.value == 0.0:
        return float32x8_empty(cgen)
    arg = Float32x8Arg(value=float32x8(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x8_const_x8(cgen, con1, con2, con3, con4, con5, con6, con7, con8):
    val = float32x8(con1.value, con2.value, con3.value, con4.value,
                    con5.value, con6.value, con7.value, con8.value)
    arg = Float32x8Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x8_f32(cgen, xmm):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vbroadcastss %s, %s\n' % (ymm, xmm)
        return code, ymm, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = cgen.gen.broadcast_f32(xmm)
        code += 'vperm2f128 %s, %s, %s, 0\n' % (ymm, 'y' + xmm[1:], 'y' + xmm[1:])
        return code, ymm, Float32x8Arg
    else:
        xmm1 = cgen.register('xmm')
        code = cgen.gen.broadcast_f32(xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        return code, (xmm, xmm1), Float32x8Arg


def float32x8_f32x8(cgen, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        return '', reg, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_f32x4(xmm1, ptr_reg=reg)
        code += cgen.gen.load_f32x4(xmm2, ptr_reg=reg, offset=16)
        return code, (xmm1, xmm2), Float32x8Arg


def float32x8_i32x8(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvtdq2ps %s, %s\n' % (ymm, reg)
        return code, ymm, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vcvtdq2ps %s, yword [%s]\n' % (ymm, reg)
        return code, ymm, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvtdq2ps %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvtdq2ps %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Float32x8Arg


def float32x8_f64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvtpd2ps %s, %s\n' % (ymm, reg)
        return code, ymm, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vcvtpd2ps %s, yword [%s]\n' % ('x' + ymm1[1:], reg)
        code += 'vcvtpd2ps %s, yword [%s + 32]\n' % ('x' + ymm2[1:], reg)
        code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm1, ymm1, ymm2)
        cgen.release_reg(ymm2)
        return code, ymm1, Float32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvtpd2ps %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvtpd2ps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'movlhps %s, %s\n' % (xmm1, xmm2)
        code += 'cvtpd2ps %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'cvtpd2ps %s, oword [%s + 48]\n' % (xmm4, reg)
        code += 'movlhps %s, %s\n' % (xmm3, xmm4)
        cgen.release_reg(xmm2)
        cgen.release_reg(xmm4)
        return code, (xmm1, xmm3), Float32x8Arg


def float32x8_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float32Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vbroadcastss %s, dword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float32x8Arg
        else:
            code, xmm1, arg_typ = arg.load_cmd(cgen)
            xmm2 = cgen.register('xmm')
            code += cgen.gen.broadcast_f32(xmm1)
            code += cgen.gen.move_reg(xmm2, xmm1)
            return code, (xmm1, xmm2), Float32x8Arg
    elif isinstance(arg, Float32x8Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Float64x8Arg):
        if cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvtpd2ps %s, zword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float32x8Arg
        elif cgen.cpu.AVX:
            ymm1 = cgen.register('ymm')
            ymm2 = cgen.register('ymm')
            code = 'vcvtpd2ps %s, yword [%s]\n' % ('x' + ymm1[1:], arg.name)
            code += 'vcvtpd2ps %s, yword [%s + 32]\n' % ('x' + ymm2[1:], arg.name)
            code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm1, ymm1, ymm2)
            cgen.release_reg(ymm2)
            return code, ymm1, Float32x8Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'cvtpd2ps %s, oword [%s]\n' % (xmm1, arg.name)
            code += 'cvtpd2ps %s, oword [%s + 16]\n' % (xmm2, arg.name)
            code += 'movlhps %s, %s\n' % (xmm1, xmm2)
            code += 'cvtpd2ps %s, oword [%s + 32]\n' % (xmm3, arg.name)
            code += 'cvtpd2ps %s, oword [%s + 48]\n' % (xmm4, arg.name)
            code += 'movlhps %s, %s\n' % (xmm3, xmm4)
            cgen.release_reg(xmm2)
            cgen.release_reg(xmm4)
            return code, (xmm1, xmm3), Float32x8Arg
    elif isinstance(arg, Int32x8Arg):
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvtdq2ps %s, yword [%s]\n' % (ymm, arg.name)
            return code, ymm, Float32x8Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'cvtdq2ps %s, oword [%s]\n' % (xmm1, arg.name)
            code += 'cvtdq2ps %s, oword [%s + 16]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Float32x8Arg
    else:
        raise TypeError("Callable float64x8 doesn't support argument ", arg)


def float32x8_f32x4_f32x4(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vinserti32x4 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
        code += 'vinserti32x4 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        return code, ymm, Float32x8Arg
    elif cgen.cpu.AVX:
        ymm = cgen.register('ymm')
        code = 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        return code, ymm, Float32x8Arg
    else:
        return '', (xmm1, xmm2), Float32x8Arg


def float32x8_namex2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Float32x4Arg) and isinstance(arg2, Float32x4Arg):
        if cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vinserti32x4 %s, %s, oword[%s], 0\n' % (ymm, ymm, arg1.name)
            code += 'vinserti32x4 %s, %s, oword[%s], 1\n' % (ymm, ymm, arg2.name)
            return code, ymm, Float32x8Arg
        elif cgen.cpu.AVX:
            code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
            ymm = cgen.register('ymm')
            code2 = 'vinsertf128 %s, %s, oword[%s], 1\n' % (ymm, 'y' + xmm1[1:], arg2.name)
            cgen.release_reg(xmm1)
            return code1 + code2, ymm, Float32x8Arg
        else:
            code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (xmm1, xmm2), Float32x8Arg
    else:
        raise ValueError("float32x8 doesn't support arguments.", arg1, arg2)


register_built_in('float32x8', tuple(), float32x8_empty)
register_built_in('float32x8', (Const,), float32x8_const)
register_built_in('float32x8', (Const, Const, Const, Const, Const, Const, Const, Const), float32x8_const_x8)
register_built_in('float32x8', (Float32Arg,), float32x8_f32)
register_built_in('float32x8', (Float32x8Arg,), float32x8_f32x8)
register_built_in('float32x8', (Int32x8Arg,), float32x8_i32x8)
register_built_in('float32x8', (Float64x8Arg,), float32x8_f64x8)
register_built_in('float32x8', (Name,), float32x8_name)
register_built_in('float32x8', (Float32x4Arg, Float32x4Arg), float32x8_f32x4_f32x4)
register_built_in('float32x8', (Name, Name), float32x8_namex2)


def float32x16_empty(cgen):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vxorps %s, %s, %s\n' % (zmm, zmm, zmm)
        return code, zmm, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vxorps %s, %s, %s\n' % (ymm1, ymm1, ymm1)
        code += 'vxorps %s, %s, %s\n' % (ymm2, ymm2, ymm2)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = 'xorps %s, %s\n' % (xmms[0], xmms[0])
        code += 'xorps %s, %s\n' % (xmms[1], xmms[1])
        code += 'xorps %s, %s\n' % (xmms[2], xmms[2])
        code += 'xorps %s, %s\n' % (xmms[3], xmms[3])
        return code, xmms, Float32x16Arg


def float32x16_const(cgen, con):
    if con.value == 0.0:
        return float32x16_empty(cgen)
    arg = Float32x16Arg(value=float32x16(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x16_const_x16(cgen, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16):
    val = float32x16(c1.value, c2.value, c3.value, c4.value, c5.value, c6.value, c7.value, c8.value,
                     c9.value, c10.value, c11.value, c12.value, c13.value, c14.value, c15.value, c16.value)
    arg = Float32x16Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def float32x16_f32(cgen, xmm):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vbroadcastss %s, %s\n' % (zmm, xmm)
        return code, zmm, Float32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vbroadcastss %s, %s\n' % (ymm1, xmm)
        code += 'vmovaps %s, %s\n' % (ymm2, ymm1)
        return code, (ymm1, ymm2), Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = cgen.gen.broadcast_f32(xmm)
        code += 'vperm2f128 %s, %s, %s, 0\n' % (ymm1, 'y' + xmm[1:], 'y' + xmm[1:])
        code += 'vmovaps %s, %s\n' % (ymm2, ymm1)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2, xmm3 = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.broadcast_f32(xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        code += cgen.gen.move_reg(xmm2, xmm)
        code += cgen.gen.move_reg(xmm3, xmm)
        return code, (xmm, xmm1, xmm2, xmm3), Float32x16Arg


def float32x16_f32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        return '', reg, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = cgen.gen.load_f32x8(ymm1, ptr_reg=reg)
        code += cgen.gen.load_f32x8(ymm2, ptr_reg=reg, offset=32)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_f32x4(xmm1, ptr_reg=reg)
        code += cgen.gen.load_f32x4(xmm2, ptr_reg=reg, offset=16)
        code += cgen.gen.load_f32x4(xmm3, ptr_reg=reg, offset=32)
        code += cgen.gen.load_f32x4(xmm4, ptr_reg=reg, offset=48)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def float32x16_i32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vcvtdq2ps %s, %s\n' % (zmm, reg)
        return code, zmm, Float32x16Arg
    elif cgen.cpu.AVX:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vcvtdq2ps %s, yword [%s]\n' % (ymm1, reg)
        code += 'vcvtdq2ps %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvtdq2ps %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvtdq2ps %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'cvtdq2ps %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'cvtdq2ps %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def float32x16_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Float32Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vbroadcastss %s, dword [%s]\n' % (zmm, arg.name)
            return code, zmm, Float32x16Arg
        elif cgen.cpu.AVX:
            ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vbroadcastss %s, dword [%s]\n' % (ymm1, arg.name)
            code += 'vmovaps %s, %s\n' % (ymm2, ymm1)
            return code, (ymm1, ymm2), Float32x16Arg
        else:
            code, xmm1, arg_typ = arg.load_cmd(cgen)
            xmm2, xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
            code += cgen.gen.broadcast_f32(xmm1)
            code += cgen.gen.move_reg(xmm2, xmm1)
            code += cgen.gen.move_reg(xmm3, xmm1)
            code += cgen.gen.move_reg(xmm4, xmm1)
            return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg
    elif isinstance(arg, Float32x16Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int32x16Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vcvtdq2ps %s, zword [%s]\n' % (zmm, arg.name)
            return code, zmm, Float32x16Arg
        elif cgen.cpu.AVX:
            ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vcvtdq2ps %s, yword [%s]\n' % (ymm1, arg.name)
            code += 'vcvtdq2ps %s, yword [%s + 32]\n' % (ymm2, arg.name)
            return code, (ymm1, ymm2), Float32x16Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'cvtdq2ps %s, oword [%s]\n' % (xmm1, arg.name)
            code += 'cvtdq2ps %s, oword [%s + 16]\n' % (xmm2, arg.name)
            code += 'cvtdq2ps %s, oword [%s + 32]\n' % (xmm3, arg.name)
            code += 'cvtdq2ps %s, oword [%s + 48]\n' % (xmm4, arg.name)
            return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg
    else:
        raise TypeError("Callable float32x16 doesn't support argument ", arg)


def float32x16_f32x8_f32x8(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vinserti32x8 %s, %s, %s, 0\n' % (zmm, zmm, reg1)
        code += 'vinserti32x8 %s, %s, %s, 1\n' % (zmm, zmm, reg2)
        return code, zmm, Float32x16Arg
    elif cgen.cpu.AVX:
        return '', (reg1, reg2), Float32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_f32x4(xmm1, ptr_reg=reg1)
        code += cgen.gen.load_f32x4(xmm2, ptr_reg=reg1, offset=16)
        code += cgen.gen.load_f32x4(xmm3, ptr_reg=reg2)
        code += cgen.gen.load_f32x4(xmm4, ptr_reg=reg2, offset=16)
        return code, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg


def float32x16_name_x2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Float32x8Arg) and isinstance(arg2, Float32x8Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vinserti32x8 %s, %s, yword[%s], 0\n' % (zmm, zmm, arg1.name)
            code += 'vinserti32x8 %s, %s, yword[%s], 1\n' % (zmm, zmm, arg2.name)
            return code, zmm, Float32x16Arg
        elif cgen.cpu.AVX:
            code1, ymm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, ymm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (ymm1, ymm2), Float32x16Arg
        else:
            code1, (xmm1, xmm2), arg_typ1 = arg1.load_cmd(cgen)
            code2, (xmm3, xmm4), arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (xmm1, xmm2, xmm3, xmm4), Float32x16Arg
    else:
        raise ValueError("float32x16 doesn't support arguments.", arg1, arg2)


register_built_in('float32x16', tuple(), float32x16_empty)
register_built_in('float32x16', (Const,), float32x16_const)
register_built_in('float32x16', (Const, Const, Const, Const, Const, Const, Const, Const,
                                 Const, Const, Const, Const, Const, Const, Const, Const), float32x16_const_x16)
register_built_in('float32x16', (Float32Arg,), float32x16_f32)
register_built_in('float32x16', (Float32x16Arg,), float32x16_f32x16)
register_built_in('float32x16', (Int32x16Arg,), float32x16_i32x16)
register_built_in('float32x16', (Name,), float32x16_name)
register_built_in('float32x16', (Float32x8Arg, Float32x8Arg), float32x16_f32x8_f32x8)
register_built_in('float32x16', (Name, Name), float32x16_name_x2)


def int64x2_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        code = 'vpxorq %s, %s, %s\n' % (xmm, xmm, xmm)
    elif cgen.cpu.AVX:
        code = 'vpxor %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'pxor %s, %s\n' % (xmm, xmm)
    return code, xmm, Int64x2Arg


def int64x2_const(cgen, con):
    if con.value == 0:
        return int64x2_empty(cgen)
    arg = Int64x2Arg(value=int64x2(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x2_const_const(cgen, con1, con2):
    val = int64x2(con1.value, con2.value)
    arg = Int64x2Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x2_i64x2(cgen, xmm):
    return '', xmm, Int64x2Arg


def int64x2_i32x2(cgen, xmm):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpmovsxdq %s, %s\n' % (xmm, xmm)
    else:
        code = 'pmovsxdq %s, %s\n' % (xmm, xmm)
    return code, xmm, Int64x2Arg


def int64x2_i64(cgen, reg):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vpunpcklqdq %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'movq %s, %s\n' % (xmm, reg)
        code += 'punpcklqdq %s, %s\n' % (xmm, xmm)
    return code, xmm, Int64x2Arg


def int64x2_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int64x2Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = "vmovq %s, qword[%s]\n" % (xmm, arg.name)
            code += 'vpunpcklqdq %s, %s, %s\n' % (xmm, xmm, xmm)
        else:
            code = 'movq %s, qword[%s]\n' % (xmm, arg.name)
            code += 'punpcklqdq %s, %s\n' % (xmm, xmm)
        return code, xmm, Int64x2Arg
    elif isinstance(arg, Int32x2Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vpmovsxdq %s, qword [%s]\n' % (xmm, arg.name)
        else:
            code = 'pmovsxdq %s, qword [%s]\n' % (xmm, arg.name)
        return code, xmm, Int64x2Arg
    else:
        raise TypeError("Callable int64x2 doesn't support argument ", arg)


def int64x2_i64_i64(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovq %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrq %s, %s, %s, 1\n' % (xmm1, xmm1, reg2)
    else:
        code = 'movq %s, %s\n' % (xmm1, reg1)
        code += 'pinsrq %s, %s, 1\n' % (xmm1, reg2)
    return code, xmm1, Int64x2Arg


def int64x2_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if not (isinstance(arg1, Int64Arg) and isinstance(arg2, Int64Arg)):
        raise TypeError("Callable int64x2 doesn't support arguments ", arg1, arg2)

    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = "vmovq %s, qword[%s]\n" % (xmm, arg1.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % (xmm, xmm, arg2.name)
    else:
        code = "movq %s, qword[%s]\n" % (xmm, arg1.name)
        code += 'pinsrq %s, qword [%s], 1\n' % (xmm, arg2.name)
    return code, xmm, Int64x2Arg


register_built_in('int64x2', tuple(), int64x2_empty)
register_built_in('int64x2', (Const,), int64x2_const)
register_built_in('int64x2', (Const, Const), int64x2_const_const)
register_built_in('int64x2', (Int64x2Arg,), int64x2_i64x2)
register_built_in('int64x2', (Int32x2Arg,), int64x2_i32x2)
register_built_in('int64x2', (Int64Arg,), int64x2_i64)
register_built_in('int64x2', (Name,), int64x2_name)
register_built_in('int64x2', (Int64Arg, Int64Arg), int64x2_i64_i64)
register_built_in('int64x2', (Name, Name), int64x2_name_name)


def int64x3_empty(cgen):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vpxorq %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX2:
        ymm = cgen.register('ymm')
        code = 'vpxor %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'vpxor %s, %s, %s\n' % (xmms[0], xmms[0], xmms[0])
        code += 'vpxor %s, %s, %s\n' % (xmms[1], xmms[1], xmms[1])
        return code, xmms, Int64x3Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'pxor %s, %s\n' % (xmms[0], xmms[0])
        code += 'pxor %s, %s\n' % (xmms[1], xmms[1])
        return code, xmms, Int64x3Arg


def int64x3_const(cgen, con):
    if con.value == 0:
        return int64x3_empty(cgen)
    arg = Int64x3Arg(value=int64x3(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x3_const_x3(cgen, con1, con2, con3):
    val = int64x3(con1.value, con2.value, con3.value)
    arg = Int64x3Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x3_i64x3(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Int64x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_i64x2(xmm1, ptr_reg=reg)
        code += cgen.gen.load_i64x2(xmm2, ptr_reg=reg, offset=16)
        return code, (xmm1, xmm2), Int64x3Arg


def int64x3_i32x3(cgen, xmm):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (ymm, xmm)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = "vmovhlps %s, %s, %s\n" % (xmm2, xmm2, xmm)
        code += 'vpmovsxdq %s, %s\n' % (xmm1, xmm)
        code += 'vpmovsxdq %s, %s\n' % (xmm2, xmm2)
        return code, (xmm1, xmm2), Int64x3Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = "movhlps %s, %s\n" % (xmm2, xmm)
        code += 'pmovsxdq %s, %s\n' % (xmm1, xmm)
        code += 'pmovsxdq %s, %s\n' % (xmm2, xmm2)
        return code, (xmm1, xmm2), Int64x3Arg


def int64x3_i64(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        xmm = cgen.register('xmm')
        ymm = cgen.register('ymm')
        code = 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastq %s, %s\n' % (ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX:
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        code = 'vmovq %s, %s\n' % (xmm1, reg)
        code += 'vpunpcklqdq %s, %s, %s\n' % (xmm1, xmm1, xmm1)
        code += 'vmovaps %s, %s\n' % (xmm2, xmm1)
        return code, (xmm1, xmm2), Int64x3Arg
    else:
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        code = 'movq %s, %s\n' % (xmm1, reg)
        code += 'punpcklqdq %s, %s\n' % (xmm1, xmm1)
        code += 'movaps %s, %s\n' % (xmm2, xmm1)
        return code, (xmm1, xmm2), Int64x3Arg


def int64x3_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int64x3Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vpbroadcastq %s, qword[%s]\n' % (ymm, arg.name)
            return code, ymm, Int64x3Arg
        if cgen.cpu.AVX:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = "vmovq %s, qword[%s]\n" % (xmm1, arg.name)
            code += 'vpunpcklqdq %s, %s, %s\n' % (xmm1, xmm1, xmm1)
            code += "vmovaps %s, %s\n" % (xmm2, xmm1)
            return code, (xmm1, xmm2), Int64x3Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'movq %s, qword[%s]\n' % (xmm1, arg.name)
            code += 'punpcklqdq %s, %s\n' % (xmm1, xmm1)
            code += "movaps %s, %s\n" % (xmm2, xmm1)
            return code, (xmm1, xmm2), Int64x3Arg
    elif isinstance(arg, Int32x3Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vpmovsxdq %s, oword [%s]\n' % (ymm, arg.name)
            return code, ymm, Int64x3Arg
        elif cgen.cpu.AVX:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'vpmovsxdq %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'vpmovsxdq %s, qword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Int64x3Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'pmovsxdq %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'pmovsxdq %s, qword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Int64x3Arg
    else:
        raise TypeError("Callable int64x3 doesn't support argument ", arg)


def int64x3_i64_x3(cgen, reg1, reg2, reg3):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        xmm = cgen.register('xmm')
        code = 'vmovq %s, %s\n' % ('x' + ymm[1:], reg1)
        code += 'vpinsrq %s, %s, %s, 1\n' % ('x' + ymm[1:], 'x' + ymm[1:], reg2)
        code += 'vmovq %s, %s\n' % (xmm, reg3)
        if cgen.cpu.AVX512F:
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        else:
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovq %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrq %s, %s, %s, 1\n' % (xmm1, xmm1, reg2)
        code += 'vmovq %s, %s\n' % (xmm2, reg3)
        return code, (xmm1, xmm2), Int64x3Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movq %s, %s\n' % (xmm1, reg1)
        code += 'pinsrq %s, %s, 1\n' % (xmm1, reg2)
        code += 'movq %s, %s\n' % (xmm2, reg3)
        return code, (xmm1, xmm2), Int64x3Arg


def int64x3_name_x3(cgen, name1, name2, name3):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)

    if not (isinstance(arg1, Int64Arg) and isinstance(arg2, Int64Arg) and isinstance(arg3, Int64Arg)):
        raise TypeError("Callable int64x3 doesn't support arguments ", arg1, arg2, arg3)

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        xmm = cgen.register('xmm')
        code = "vmovq %s, qword[%s]\n" % ('x' + ymm[1:], arg1.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % ('x' + ymm[1:], 'x' + ymm[1:], arg2.name)
        code += "vmovq %s, qword[%s]\n" % (xmm, arg3.name)
        if cgen.cpu.AVX512F:
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        else:
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int64x3Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = "vmovq %s, qword[%s]\n" % (xmm1, arg1.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % (xmm1, xmm1, arg2.name)
        code += "vmovq %s, qword[%s]\n" % (xmm2, arg3.name)
        return code, (xmm1, xmm2), Int64x3Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = "movq %s, qword[%s]\n" % (xmm1, arg1.name)
        code += 'pinsrq %s, qword [%s], 1\n' % (xmm1, arg2.name)
        code += "movq %s, qword[%s]\n" % (xmm2, arg3.name)
        return code, (xmm1, xmm2), Int64x3Arg


register_built_in('int64x3', tuple(), int64x3_empty)
register_built_in('int64x3', (Const,), int64x3_const)
register_built_in('int64x3', (Const, Const, Const), int64x3_const_x3)
register_built_in('int64x3', (Int64x3Arg,), int64x3_i64x3)
register_built_in('int64x3', (Int32x3Arg,), int64x3_i32x3)
register_built_in('int64x3', (Int64Arg,), int64x3_i64)
register_built_in('int64x3', (Name,), int64x3_name)
register_built_in('int64x3', (Int64Arg, Int64Arg, Int64Arg), int64x3_i64_x3)
register_built_in('int64x3', (Name, Name, Name), int64x3_name_x3)


def int64x4_empty(cgen):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vpxorq %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Int64x4Arg
    elif cgen.cpu.AVX2:
        ymm = cgen.register('ymm')
        code = 'vpxor %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Int64x4Arg
    elif cgen.cpu.AVX:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'vpxor %s, %s, %s\n' % (xmms[0], xmms[0], xmms[0])
        code += 'vpxor %s, %s, %s\n' % (xmms[1], xmms[1], xmms[1])
        return code, xmms, Int64x4Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'pxor %s, %s\n' % (xmms[0], xmms[0])
        code += 'pxor %s, %s\n' % (xmms[1], xmms[1])
        return code, xmms, Int64x4Arg


def int64x4_const(cgen, con):
    if con.value == 0:
        return int64x4_empty(cgen)
    arg = Int64x4Arg(value=int64x4(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x4_const_x4(cgen, con1, con2, con3, con4):
    val = int64x4(con1.value, con2.value, con3.value, con4.value)
    arg = Int64x4Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x4_i64x4(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Int64x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_i64x2(xmm1, ptr_reg=reg)
        code += cgen.gen.load_i64x2(xmm2, ptr_reg=reg, offset=16)
        return code, (xmm1, xmm2), Int64x4Arg


def int64x4_i32x4(cgen, xmm):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (ymm, xmm)
        return code, ymm, Int64x4Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = "vmovhlps %s, %s, %s\n" % (xmm2, xmm2, xmm)
        code += 'vpmovsxdq %s, %s\n' % (xmm1, xmm)
        code += 'vpmovsxdq %s, %s\n' % (xmm2, xmm2)
        return code, (xmm1, xmm2), Int64x4Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = "movhlps %s, %s\n" % (xmm2, xmm)
        code += 'pmovsxdq %s, %s\n' % (xmm1, xmm)
        code += 'pmovsxdq %s, %s\n' % (xmm2, xmm2)
        return code, (xmm1, xmm2), Int64x4Arg


def int64x4_i64(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        xmm = cgen.register('xmm')
        ymm = cgen.register('ymm')
        code = 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastq %s, %s\n' % (ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int64x4Arg
    elif cgen.cpu.AVX:
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        code = 'vmovq %s, %s\n' % (xmm1, reg)
        code += 'vpunpcklqdq %s, %s, %s\n' % (xmm1, xmm1, xmm1)
        code += 'vmovaps %s, %s\n' % (xmm2, xmm1)
        return code, (xmm1, xmm2), Int64x4Arg
    else:
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        code = 'movq %s, %s\n' % (xmm1, reg)
        code += 'punpcklqdq %s, %s\n' % (xmm1, xmm1)
        code += 'movaps %s, %s\n' % (xmm2, xmm1)
        return code, (xmm1, xmm2), Int64x4Arg


def int64x4_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int64x4Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vpbroadcastq %s, qword[%s]\n' % (ymm, arg.name)
            return code, ymm, Int64x4Arg
        if cgen.cpu.AVX:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = "vmovq %s, qword[%s]\n" % (xmm1, arg.name)
            code += 'vpunpcklqdq %s, %s, %s\n' % (xmm1, xmm1, xmm1)
            code += "vmovaps %s, %s\n" % (xmm2, xmm1)
            return code, (xmm1, xmm2), Int64x4Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'movq %s, qword[%s]\n' % (xmm1, arg.name)
            code += 'punpcklqdq %s, %s\n' % (xmm1, xmm1)
            code += "movaps %s, %s\n" % (xmm2, xmm1)
            return code, (xmm1, xmm2), Int64x4Arg
    elif isinstance(arg, Int32x4Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vpmovsxdq %s, oword [%s]\n' % (ymm, arg.name)
            return code, ymm, Int64x4Arg
        elif cgen.cpu.AVX:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'vpmovsxdq %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'vpmovsxdq %s, qword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Int64x4Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            code = 'pmovsxdq %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'pmovsxdq %s, qword [%s + 8]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Int64x4Arg
    else:
        raise TypeError("Callable int64x4 doesn't support argument ", arg)


def int64x4_i64_x4(cgen, reg1, reg2, reg3, reg4):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        xmm = cgen.register('xmm')
        code = 'vmovq %s, %s\n' % ('x' + ymm[1:], reg1)
        code += 'vpinsrq %s, %s, %s, 1\n' % ('x' + ymm[1:], 'x' + ymm[1:], reg2)
        code += 'vmovq %s, %s\n' % (xmm, reg3)
        code += 'vpinsrq %s, %s, %s, 1\n' % (xmm, xmm, reg4)
        if cgen.cpu.AVX512F:
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        else:
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int64x4Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vmovq %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrq %s, %s, %s, 1\n' % (xmm1, xmm1, reg2)
        code += 'vmovq %s, %s\n' % (xmm2, reg3)
        code += 'vpinsrq %s, %s, %s, 1\n' % (xmm2, xmm2, reg4)
        return code, (xmm1, xmm2), Int64x4Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = 'movq %s, %s\n' % (xmm1, reg1)
        code += 'pinsrq %s, %s, 1\n' % (xmm1, reg2)
        code += 'movq %s, %s\n' % (xmm2, reg3)
        code += 'pinsrq %s, %s, 1\n' % (xmm2, reg4)
        return code, (xmm1, xmm2), Int64x4Arg


def int64x4_name_x4(cgen, name1, name2, name3, name4):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)
    arg4 = cgen.get_arg(name4)

    if not (isinstance(arg1, Int64Arg) and isinstance(arg2, Int64Arg) and
            isinstance(arg3, Int64Arg) and isinstance(arg4, Int64Arg)):
        raise TypeError("Callable int64x4 doesn't support arguments ", arg1, arg2, arg3, arg4)

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        xmm = cgen.register('xmm')
        code = "vmovq %s, qword[%s]\n" % ('x' + ymm[1:], arg1.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % ('x' + ymm[1:], 'x' + ymm[1:], arg2.name)
        code += "vmovq %s, qword[%s]\n" % (xmm, arg3.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % (xmm, xmm, arg4.name)
        if cgen.cpu.AVX512F:
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        else:
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int64x4Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = "vmovq %s, qword[%s]\n" % (xmm1, arg1.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % (xmm1, xmm1, arg2.name)
        code += "vmovq %s, qword[%s]\n" % (xmm2, arg3.name)
        code += 'vpinsrq %s, %s, qword [%s], 1\n' % (xmm2, xmm2, arg4.name)
        return code, (xmm1, xmm2), Int64x4Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        code = "movq %s, qword[%s]\n" % (xmm1, arg1.name)
        code += 'pinsrq %s, qword [%s], 1\n' % (xmm1, arg2.name)
        code += "movq %s, qword[%s]\n" % (xmm2, arg3.name)
        code += 'pinsrq %s, qword [%s], 1\n' % (xmm2, arg4.name)
        return code, (xmm1, xmm2), Int64x4Arg


def int64x4_i64x2_i64x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        if cgen.cpu.AVX512F:
            code = 'vmovdqa64 %s, %s\n' % ('x' + ymm[1:], xmm1)
            code += 'vinserti64x2 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        else:
            code = 'vmovdqa %s, %s\n' % ('x' + ymm[1:], xmm1)
            code += 'vinserti128 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        return code, ymm, Int64x4Arg
    else:
        return '', (xmm1, xmm2), Int64x4Arg


def int64x4_name_x2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Int64x2Arg) and isinstance(arg2, Int64x2Arg):
        if cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vinserti64x2 %s, %s, oword[%s], 0\n' % (ymm, ymm, arg1.name)
            code += 'vinserti64x2 %s, %s, oword[%s], 1\n' % (ymm, ymm, arg2.name)
            return code, ymm, Int64x4Arg
        elif cgen.cpu.AVX2:
            code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmm2, arg_typ2 = arg2.load_cmd(cgen)
            ymm = cgen.register('ymm')
            code3 = 'vperm2i128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
            cgen.release_reg(xmm1)
            cgen.release_reg(xmm2)
            return code1 + code2 + code3, ymm, Int64x4Arg
        else:
            code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (xmm1, xmm2), Int64x4Arg
    else:
        raise ValueError("int64x4 doesn't support arguments.", arg1, arg2)


register_built_in('int64x4', tuple(), int64x4_empty)
register_built_in('int64x4', (Const,), int64x4_const)
register_built_in('int64x4', (Const, Const, Const, Const), int64x4_const_x4)
register_built_in('int64x4', (Int64x4Arg,), int64x4_i64x4)
register_built_in('int64x4', (Int32x4Arg,), int64x4_i32x4)
register_built_in('int64x4', (Int64Arg,), int64x4_i64)
register_built_in('int64x4', (Name,), int64x4_name)
register_built_in('int64x4', (Int64Arg, Int64Arg, Int64Arg, Int64Arg), int64x4_i64_x4)
register_built_in('int64x4', (Name, Name, Name, Name), int64x4_name_x4)
register_built_in('int64x4', (Int64x2Arg, Int64x2Arg), int64x4_i64x2_i64x2)
register_built_in('int64x4', (Name, Name), int64x4_name_x2)


def int64x8_empty(cgen):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vpxorq %s, %s, %s\n' % (zmm, zmm, zmm)
        return code, zmm, Int64x8Arg
    if cgen.cpu.AVX2:
        ymms = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vpxor %s, %s, %s\n' % (ymms[0], ymms[0], ymms[0])
        code += 'vpxor %s, %s, %s\n' % (ymms[1], ymms[1], ymms[1])
        return code, ymms, Int64x8Arg
    elif cgen.cpu.AVX:
        xmms = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = 'vpxor %s, %s, %s\n' % (xmms[0], xmms[0], xmms[0])
        code += 'vpxor %s, %s, %s\n' % (xmms[1], xmms[1], xmms[1])
        code += 'vpxor %s, %s, %s\n' % (xmms[2], xmms[2], xmms[2])
        code += 'vpxor %s, %s, %s\n' % (xmms[3], xmms[3], xmms[3])
        return code, xmms, Int64x8Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = 'pxor %s, %s\n' % (xmms[0], xmms[0])
        code += 'pxor %s, %s\n' % (xmms[1], xmms[1])
        code += 'pxor %s, %s\n' % (xmms[2], xmms[2])
        code += 'pxor %s, %s\n' % (xmms[3], xmms[3])
        return code, xmms, Int64x8Arg


def int64x8_const(cgen, con):
    if con.value == 0:
        return int64x8_empty(cgen)
    arg = Int64x8Arg(value=int64x8(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x8_const_x8(cgen, con1, con2, con3, con4, con5, con6, con7, con8):
    val = int64x8(con1.value, con2.value, con3.value, con4.value,
                  con5.value, con6.value, con7.value, con8.value)
    arg = Int64x8Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int64x8_i64(cgen, reg):
    if cgen.cpu.AVX512F:
        xmm = cgen.register('xmm')
        zmm = cgen.register('zmm')
        code = 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastq %s, %s\n' % (zmm, xmm)
        cgen.release_reg(xmm)
        return code, zmm, Int64x8Arg
    elif cgen.cpu.AVX2:
        xmm = cgen.register('xmm')
        ymm1 = cgen.register('ymm')
        ymm2 = cgen.register('ymm')
        code = 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastq %s, %s\n' % (ymm1, xmm)
        code += 'vmovdqa %s, %s\n' % (ymm2, ymm1)
        cgen.release_reg(xmm)
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm = cgen.register('xmm')
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        xmm3 = cgen.register('xmm')
        code = 'vmovq %s, %s\n' % (xmm, reg)
        code += 'vpunpcklqdq %s, %s, %s\n' % (xmm, xmm, xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        code += cgen.gen.move_reg(xmm2, xmm)
        code += cgen.gen.move_reg(xmm3, xmm)
        return code, (xmm, xmm1, xmm2, xmm3), Int64x8Arg
    else:
        xmm = cgen.register('xmm')
        xmm1 = cgen.register('xmm')
        xmm2 = cgen.register('xmm')
        xmm3 = cgen.register('xmm')
        code = 'movq %s, %s\n' % (xmm, reg)
        code += 'punpcklqdq %s, %s\n' % (xmm, xmm)
        code += cgen.gen.move_reg(xmm1, xmm)
        code += cgen.gen.move_reg(xmm2, xmm)
        code += cgen.gen.move_reg(xmm3, xmm)
        return code, (xmm, xmm1, xmm2, xmm3), Int64x8Arg


def int64x8_i64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        return '', reg, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = cgen.gen.load_i64x4(ymm1, ptr_reg=reg)
        code += cgen.gen.load_i64x4(ymm2, ptr_reg=reg, offset=32)
        return code, (ymm1, ymm2), Int64x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_i64x2(xmm1, ptr_reg=reg)
        code += cgen.gen.load_i64x2(xmm2, ptr_reg=reg, offset=16)
        code += cgen.gen.load_i64x2(xmm3, ptr_reg=reg, offset=32)
        code += cgen.gen.load_i64x2(xmm4, ptr_reg=reg, offset=48)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg


def int64x8_i32x8(cgen, reg):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vpmovsxdq %s, %s\n' % (zmm, reg)
        return code, zmm, Int64x8Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
        code = 'vpmovsxdq %s, %s\n' % (ymm1, 'x' + reg[1:])
        code += 'vextracti128 %s, %s, 1\n' % ('x' + ymm2[1:], reg)
        code += 'vpmovsxdq %s, %s\n' % (ymm2, 'x' + ymm2[1:])
        return code, (ymm1, ymm2), Int64x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'vpmovsxdq %s, qword [%s]\n' % (xmm1, reg)
        code += 'vpmovsxdq %s, qword [%s + 8]\n' % (xmm2, reg)
        code += 'vpmovsxdq %s, qword [%s + 16]\n' % (xmm3, reg)
        code += 'vpmovsxdq %s, qword [%s + 24]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = 'pmovsxdq %s, qword [%s]\n' % (xmm1, reg)
        code += 'pmovsxdq %s, qword [%s + 8]\n' % (xmm2, reg)
        code += 'pmovsxdq %s, qword [%s + 16]\n' % (xmm3, reg)
        code += 'pmovsxdq %s, qword [%s + 24]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg


def int64x8_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int64x8Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vpbroadcastq %s, qword[%s]\n' % (zmm, arg.name)
            return code, zmm, Int64x8Arg
        elif cgen.cpu.AVX2:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = 'vpbroadcastq %s, qword[%s]\n' % (ymm1, arg.name)
            code += 'vmovdqa %s, %s\n' % (ymm2, ymm1)
            return code, (ymm1, ymm2), Int64x8Arg
        if cgen.cpu.AVX:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = "vmovq %s, qword[%s]\n" % (xmm1, arg.name)
            code += 'vpunpcklqdq %s, %s, %s\n' % (xmm1, xmm1, xmm1)
            code += "vmovdqa %s, %s\n" % (xmm2, xmm1)
            code += "vmovdqa %s, %s\n" % (xmm3, xmm1)
            code += "vmovdqa %s, %s\n" % (xmm4, xmm1)
            return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = 'movq %s, qword[%s]\n' % (xmm1, arg.name)
            code += 'punpcklqdq %s, %s\n' % (xmm1, xmm1)
            code += "movdqa %s, %s\n" % (xmm2, xmm1)
            code += "movdqa %s, %s\n" % (xmm3, xmm1)
            code += "movdqa %s, %s\n" % (xmm4, xmm1)
            return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    elif isinstance(arg, Int32x8Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vpmovsxdq %s, yword [%s]\n' % (zmm, arg.name)
            return code, zmm, Int64x8Arg
        elif cgen.cpu.AVX2:
            ymm1, ymm2 = cgen.register('ymm'), cgen.register('ymm')
            code = 'vpmovsxdq %s, oword [%s]\n' % (ymm1, arg.name)
            code += 'vpmovsxdq %s, oword [%s + 16]\n' % (ymm2, arg.name)
            return code, (ymm1, ymm2), Int64x8Arg
        elif cgen.cpu.AVX:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = 'vpmovsxdq %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'vpmovsxdq %s, qword [%s + 8]\n' % (xmm2, arg.name)
            code += 'vpmovsxdq %s, qword [%s + 16]\n' % (xmm3, arg.name)
            code += 'vpmovsxdq %s, qword [%s + 24]\n' % (xmm4, arg.name)
            return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
        else:
            xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
            xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
            code = 'pmovsxdq %s, qword [%s]\n' % (xmm1, arg.name)
            code += 'pmovsxdq %s, qword [%s + 8]\n' % (xmm2, arg.name)
            code += 'pmovsxdq %s, qword [%s + 16]\n' % (xmm3, arg.name)
            code += 'pmovsxdq %s, qword [%s + 24]\n' % (xmm4, arg.name)
            return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg
    else:
        raise TypeError("Callable int64x8 doesn't support argument ", arg)


def int64x8_i64x4_i64x4(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vinserti64x4 %s, %s, %s, 0\n' % (zmm, zmm, reg1)
        code += 'vinserti64x4 %s, %s, %s, 1\n' % (zmm, zmm, reg2)
        return code, zmm, Int64x8Arg
    elif cgen.cpu.AVX2:
        return '', (reg1, reg2), Int64x8Arg
    else:
        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm3, xmm4 = cgen.register('xmm'), cgen.register('xmm')
        code = cgen.gen.load_i64x2(xmm1, ptr_reg=reg1)
        code += cgen.gen.load_i64x2(xmm2, ptr_reg=reg1, offset=16)
        code += cgen.gen.load_i64x2(xmm3, ptr_reg=reg2)
        code += cgen.gen.load_i64x2(xmm4, ptr_reg=reg2, offset=16)
        return code, (xmm1, xmm2, xmm3, xmm4), Int64x8Arg


def int64x8_name_x2(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Int64x4Arg) and isinstance(arg2, Int64x4Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vinserti64x4 %s, %s, yword[%s], 0\n' % (zmm, zmm, arg1.name)
            code += 'vinserti64x4 %s, %s, yword[%s], 1\n' % (zmm, zmm, arg2.name)
            return code, zmm, Int64x8Arg
        elif cgen.cpu.AVX2:
            code1, ymm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, ymm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (ymm1, ymm2), Int64x8Arg
        else:
            code1, xmms1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmms2, arg_typ2 = arg2.load_cmd(cgen)
            xmms = xmms1 + xmms2
            return code1 + code2, xmms, Int64x8Arg
    else:
        raise ValueError("int64x8 doesn't support arguments.", arg1, arg2)


register_built_in('int64x8', tuple(), int64x8_empty)
register_built_in('int64x8', (Const,), int64x8_const)
register_built_in('int64x8', (Const, Const, Const, Const, Const, Const, Const, Const), int64x8_const_x8)
register_built_in('int64x8', (Int64Arg,), int64x8_i64)
register_built_in('int64x8', (Int64x8Arg,), int64x8_i64x8)
register_built_in('int64x8', (Int32x8Arg,), int64x8_i32x8)
register_built_in('int64x8', (Name,), int64x8_name)
register_built_in('int64x8', (Int64x4Arg, Int64x4Arg), int64x8_i64x4_i64x4)
register_built_in('int64x8', (Name, Name), int64x8_name_x2)


def int32x2_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        code = 'vpxord %s, %s, %s\n' % (xmm, xmm, xmm)
    elif cgen.cpu.AVX:
        code = 'vpxor %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'pxor %s, %s\n' % (xmm, xmm)
    return code, xmm, Int32x2Arg


def int32x2_const(cgen, con):
    if con.value == 0:
        return int32x2_empty(cgen)
    arg = Int32x2Arg(value=int32x2(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x2_const_const(cgen, con1, con2):
    val = int32x2(con1.value, con2.value)
    arg = Int32x2Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x2_i32(cgen, reg):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (xmm, reg)
    else:
        code = 'movd %s, %s\n' % (xmm, reg)
    code += cgen.gen.broadcast_i32(xmm)
    return code, xmm, Int32x2Arg


def int32x2_i32x2(cgen, xmm):
    return '', xmm, Int32x2Arg


def int32x2_f32x2(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_f32x2_to_i32x2(xmm1, xmm=xmm)
    return code, xmm1, Int32x2Arg


def int32x2_f64x2(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_f64x2_to_i32x2(xmm1, xmm=xmm)
    return code, xmm1, Int32x2Arg


def int32x2_i64x2(cgen, xmm):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpshufd %s, %s, 0x8\n' % (xmm, xmm)
    else:
        code = 'pshufd %s, %s, 0x8\n' % (xmm, xmm)
    return code, xmm, Int32x2Arg


def int32x2_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int32Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vmovd %s, dword [%s]\n' % (xmm, arg.name)
        else:
            code = 'movd %s, dword [%s]\n' % (xmm, arg.name)
        code += cgen.gen.broadcast_i32(xmm)
        return code, xmm, Int32x2Arg
    elif isinstance(arg, Float64x2Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f64x2_to_i32x2(xmm, name=arg.name)
        return code, xmm, Int32x2Arg
    elif isinstance(arg, Float32x2Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f32x2_to_i32x2(xmm, name=arg.name)
        return code, xmm, Int32x2Arg
    elif isinstance(arg, Int32x2Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64x2Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm, arg.name)
        else:
            code = 'pshufd %s, oword[%s], 0x8\n' % (xmm, arg.name)
        return code, xmm, Int32x2Arg
    else:
        raise TypeError("Callable int32x2 doesn't support argument ", arg)


def int32x2_i32_i32(cgen, reg1, reg2):
    xmm1 = cgen.register('xmm')

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrd %s, %s, %s, 0x1\n' % (xmm1, xmm1, reg2)
    else:
        code = 'movd %s, %s\n' % (xmm1, reg1)
        code += 'pinsrd %s, %s, 0x1\n' % (xmm1, reg2)

    return code, xmm1, Int32x2Arg


def int32x2_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if not (isinstance(arg1, Int32Arg) and isinstance(arg2, Int32Arg)):
        raise TypeError("Callable int32x2 doesn't support arguments ", arg1, arg2)

    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, dword [%s]\n' % (xmm, arg1.name)
        code += 'vpinsrd %s, %s, dword [%s], 0x1\n' % (xmm, xmm, arg2.name)
    else:
        code = 'movd %s, dword [%s]\n' % (xmm, arg1.name)
        code += 'pinsrd %s, dword [%s], 0x1\n' % (xmm, arg2.name)
    return code, xmm, Int32x2Arg


register_built_in('int32x2', tuple(), int32x2_empty)
register_built_in('int32x2', (Const,), int32x2_const)
register_built_in('int32x2', (Const, Const), int32x2_const_const)
register_built_in('int32x2', (Int32Arg,), int32x2_i32)
register_built_in('int32x2', (Int32x2Arg,), int32x2_i32x2)
register_built_in('int32x2', (Float32x2Arg,), int32x2_f32x2)
register_built_in('int32x2', (Float64x2Arg,), int32x2_f64x2)
register_built_in('int32x2', (Int64x2Arg,), int32x2_i64x2)
register_built_in('int32x2', (Name,), int32x2_name)
register_built_in('int32x2', (Int32Arg, Int32Arg), int32x2_i32_i32)
register_built_in('int32x2', (Name, Name), int32x2_name_name)


def int32x3_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        code = 'vpxord %s, %s, %s\n' % (xmm, xmm, xmm)
    elif cgen.cpu.AVX:
        code = 'vpxor %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'pxor %s, %s\n' % (xmm, xmm)
    return code, xmm, Int32x3Arg


def int32x3_const(cgen, con):
    if con.value == 0:
        return int32x3_empty(cgen)
    arg = Int32x3Arg(value=int32x3(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x3_const_x3(cgen, con1, con2, con3):
    val = int32x3(con1.value, con2.value, con3.value)
    arg = Int32x3Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x3_i32(cgen, reg):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (xmm, reg)
    else:
        code = 'movd %s, %s\n' % (xmm, reg)
    code += cgen.gen.broadcast_i32(xmm)
    return code, xmm, Int32x3Arg


def int32x3_i32x3(cgen, xmm):
    return '', xmm, Int32x3Arg


def int32x3_f32x3(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_f32x2_to_i32x2(xmm1, xmm=xmm)
    return code, xmm1, Int32x3Arg


def int32x3_f64x3(cgen, reg):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vcvttpd2dq %s, %s\n' % (xmm, reg)
    else:
        xmm1 = cgen.register('xmm')
        code = 'cvttpd2dq %s, oword [%s]\n' % (xmm, reg)
        code += 'cvttpd2dq %s, oword [%s + 16]\n' % (xmm1, reg)
        code += 'movlhps %s, %s\n' % (xmm, xmm1)
        cgen.release_reg(xmm1)
    return code, xmm, Int32x3Arg


def int32x3_i64x3(cgen, reg):
    xmm = cgen.register('xmm')

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        xmm1 = cgen.register('xmm')
        code = 'vpshufd %s, %s, 0x8\n' % (reg, reg)
        if cgen.cpu.AVX512F:
            code += 'vextracti64x2 %s, %s, 1\n' % (xmm1, reg)
        else:
            code += 'vextracti128 %s, %s, 1\n' % (xmm1, reg)
        code += 'vmovaps %s, %s\n' % (xmm, 'x' + reg[1:])
        code += 'vmovlhps %s, %s, %s\n' % (xmm, xmm, xmm1)
        cgen.release_reg(xmm1)
    elif cgen.cpu.AVX:
        xmm1 = cgen.register('xmm')
        code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm, reg)
        code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm1, reg)
        code += 'vmovlhps %s, %s, %s\n' % (xmm, xmm, xmm1)
        cgen.release_reg(xmm1)
    else:
        xmm1 = cgen.register('xmm')
        code = 'pshufd %s, oword[%s], 0x8\n' % (xmm, reg)
        code += 'pshufd %s, oword[%s + 16], 0x8\n' % (xmm1, reg)
        code += 'movlhps %s, %s\n' % (xmm, xmm1)
        cgen.release_reg(xmm1)
    return code, xmm, Int32x3Arg


def int32x3_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int32Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vmovd %s, dword [%s]\n' % (xmm, arg.name)
        else:
            code = 'movd %s, dword [%s]\n' % (xmm, arg.name)
        code += cgen.gen.broadcast_i32(xmm)
        return code, xmm, Int32x3Arg
    elif isinstance(arg, Float64x3Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vcvttpd2dq %s, yword [%s]\n' % (xmm, arg.name)
        else:
            xmm1 = cgen.register('xmm')
            code = 'cvttpd2dq %s, oword [%s]\n' % (xmm, arg.name)
            code += 'cvttpd2dq %s, oword [%s + 16]\n' % (xmm1, arg.name)
            code += 'movlhps %s, %s\n' % (xmm, xmm1)
            cgen.release_reg(xmm1)
        return code, xmm, Int32x3Arg
    elif isinstance(arg, Float32x3Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f32x2_to_i32x2(xmm, name=arg.name)
        return code, xmm, Int32x3Arg
    elif isinstance(arg, Int32x3Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64x3Arg):
        xmm, xmm1 = cgen.register('xmm'), cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm, arg.name)
            code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm1, arg.name)
            code += 'vmovlhps %s, %s, %s\n' % (xmm, xmm, xmm1)
        else:
            code = 'pshufd %s, oword[%s], 0x8\n' % (xmm, arg.name)
            code += 'pshufd %s, oword[%s + 16], 0x8\n' % (xmm1, arg.name)
            code += 'movlhps %s, %s\n' % (xmm, xmm1)
        cgen.release_reg(xmm1)
        return code, xmm, Int32x3Arg
    else:
        raise TypeError("Callable int32x3 doesn't support argument ", arg)


def int32x3_i32_x3(cgen, reg1, reg2, reg3):
    xmm1 = cgen.register('xmm')

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrd %s, %s, %s, 0x1\n' % (xmm1, xmm1, reg2)
        code += 'vpinsrd %s, %s, %s, 0x2\n' % (xmm1, xmm1, reg3)
    else:
        code = 'movd %s, %s\n' % (xmm1, reg1)
        code += 'pinsrd %s, %s, 0x1\n' % (xmm1, reg2)
        code += 'pinsrd %s, %s, 0x2\n' % (xmm1, reg3)

    return code, xmm1, Int32x3Arg


def int32x3_name_x3(cgen, name1, name2, name3):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)

    if not (isinstance(arg1, Int32Arg) and isinstance(arg2, Int32Arg) and isinstance(arg3, Int32Arg)):
        raise TypeError("Callable int32x3 doesn't support arguments ", arg1, arg2, arg3)

    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, dword [%s]\n' % (xmm, arg1.name)
        code += 'vpinsrd %s, %s, dword [%s], 0x1\n' % (xmm, xmm, arg2.name)
        code += 'vpinsrd %s, %s, dword [%s], 0x2\n' % (xmm, xmm, arg3.name)
    else:
        code = 'movd %s, dword [%s]\n' % (xmm, arg1.name)
        code += 'pinsrd %s, dword [%s], 0x1\n' % (xmm, arg2.name)
        code += 'pinsrd %s, dword [%s], 0x2\n' % (xmm, arg3.name)
    return code, xmm, Int32x3Arg


def int32x3_i32x2_i32(cgen, xmm, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpinsrd %s, %s, %s, 0x2\n' % (xmm, xmm, reg)
    else:
        code = 'pinsrd %s, %s, 0x2\n' % (xmm, reg)
    return code, xmm, Int32x3Arg


def int32x3_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Int32x2Arg) and isinstance(arg2, Int32Arg):
        code, xmm, arg_typ = arg1.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code += 'vpinsrd %s, %s, dword [%s], 0x2\n' % (xmm, xmm, arg2.name)
        else:
            code += 'pinsrd %s, dword [%s], 0x2\n' % (xmm, arg2.name)
        return code, xmm, Int32x3Arg
    else:
        raise TypeError("Callable int32x3 doesn't support arguments ", arg1, arg2)


register_built_in('int32x3', tuple(), int32x3_empty)
register_built_in('int32x3', (Const,), int32x3_const)
register_built_in('int32x3', (Const, Const, Const), int32x3_const_x3)
register_built_in('int32x3', (Int32Arg,), int32x3_i32)
register_built_in('int32x3', (Int32x3Arg,), int32x3_i32x3)
register_built_in('int32x3', (Float32x3Arg,), int32x3_f32x3)
register_built_in('int32x3', (Float64x3Arg,), int32x3_f64x3)
register_built_in('int32x3', (Int64x3Arg,), int32x3_i64x3)
register_built_in('int32x3', (Name,), int32x3_name)
register_built_in('int32x3', (Int32Arg, Int32Arg, Int32Arg), int32x3_i32_x3)
register_built_in('int32x3', (Name, Name, Name), int32x3_name_x3)
register_built_in('int32x3', (Int32x2Arg, Int32Arg), int32x3_i32x2_i32)
register_built_in('int32x3', (Name, Name), int32x3_name_name)


def int32x4_empty(cgen):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX512F:
        code = 'vpxord %s, %s, %s\n' % (xmm, xmm, xmm)
    elif cgen.cpu.AVX:
        code = 'vpxor %s, %s, %s\n' % (xmm, xmm, xmm)
    else:
        code = 'pxor %s, %s\n' % (xmm, xmm)
    return code, xmm, Int32x4Arg


def int32x4_const(cgen, con):
    if con.value == 0:
        return int32x4_empty(cgen)
    arg = Int32x4Arg(value=int32x4(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x4_const_x4(cgen, con1, con2, con3, con4):
    val = int32x4(con1.value, con2.value, con3.value, con4.value)
    arg = Int32x4Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x4_i32(cgen, reg):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX:
        code = 'vmovd %s, %s\n' % (xmm, reg)
    else:
        code = 'movd %s, %s\n' % (xmm, reg)
    code += cgen.gen.broadcast_i32(xmm)
    return code, xmm, Int32x4Arg


def int32x4_i32x4(cgen, xmm):
    return '', xmm, Int32x4Arg


def int32x4_f32x4(cgen, xmm):
    xmm1 = cgen.register('xmm')
    code = cgen.gen.conv_f32x2_to_i32x2(xmm1, xmm=xmm)
    return code, xmm1, Int32x4Arg


def int32x4_f64x4(cgen, reg):
    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vcvttpd2dq %s, %s\n' % (xmm, reg)
    else:
        xmm1 = cgen.register('xmm')
        code = 'cvttpd2dq %s, oword [%s]\n' % (xmm, reg)
        code += 'cvttpd2dq %s, oword [%s + 16]\n' % (xmm1, reg)
        code += 'movlhps %s, %s\n' % (xmm, xmm1)
        cgen.release_reg(xmm1)
    return code, xmm, Int32x4Arg


def int32x4_i64x4(cgen, reg):
    xmm = cgen.register('xmm')

    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        xmm1 = cgen.register('xmm')
        code = 'vpshufd %s, %s, 0x8\n' % (reg, reg)
        if cgen.cpu.AVX512F:
            code += 'vextracti64x2 %s, %s, 1\n' % (xmm1, reg)
        else:
            code += 'vextracti128 %s, %s, 1\n' % (xmm1, reg)
        code += 'vmovaps %s, %s\n' % (xmm, 'x' + reg[1:])
        code += 'vmovlhps %s, %s, %s\n' % (xmm, xmm, xmm1)
        cgen.release_reg(xmm1)
    elif cgen.cpu.AVX:
        xmm1 = cgen.register('xmm')
        code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm, reg)
        code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm1, reg)
        code += 'vmovlhps %s, %s, %s\n' % (xmm, xmm, xmm1)
        cgen.release_reg(xmm1)
    else:
        xmm1 = cgen.register('xmm')
        code = 'pshufd %s, oword[%s], 0x8\n' % (xmm, reg)
        code += 'pshufd %s, oword[%s + 16], 0x8\n' % (xmm1, reg)
        code += 'movlhps %s, %s\n' % (xmm, xmm1)
        cgen.release_reg(xmm1)
    return code, xmm, Int32x4Arg


def int32x4_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int32Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vmovd %s, dword [%s]\n' % (xmm, arg.name)
        else:
            code = 'movd %s, dword [%s]\n' % (xmm, arg.name)
        code += cgen.gen.broadcast_i32(xmm)
        return code, xmm, Int32x4Arg
    elif isinstance(arg, Float64x4Arg):
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vcvttpd2dq %s, yword [%s]\n' % (xmm, arg.name)
        else:
            xmm1 = cgen.register('xmm')
            code = 'cvttpd2dq %s, oword [%s]\n' % (xmm, arg.name)
            code += 'cvttpd2dq %s, oword [%s + 16]\n' % (xmm1, arg.name)
            code += 'movlhps %s, %s\n' % (xmm, xmm1)
            cgen.release_reg(xmm1)
        return code, xmm, Int32x4Arg
    elif isinstance(arg, Float32x4Arg):
        xmm = cgen.register('xmm')
        code = cgen.gen.conv_f32x2_to_i32x2(xmm, name=arg.name)
        return code, xmm, Int32x4Arg
    elif isinstance(arg, Int32x4Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64x4Arg):
        xmm, xmm1 = cgen.register('xmm'), cgen.register('xmm')
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm, arg.name)
            code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm1, arg.name)
            code += 'vmovlhps %s, %s, %s\n' % (xmm, xmm, xmm1)
        else:
            code = 'pshufd %s, oword[%s], 0x8\n' % (xmm, arg.name)
            code += 'pshufd %s, oword[%s + 16], 0x8\n' % (xmm1, arg.name)
            code += 'movlhps %s, %s\n' % (xmm, xmm1)
        cgen.release_reg(xmm1)
        return code, xmm, Int32x4Arg
    else:
        raise TypeError("Callable int32x4 doesn't support argument ", arg)


def int32x4_i32_x4(cgen, reg1, reg2, reg3, reg4):
    xmm1 = cgen.register('xmm')

    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, %s\n' % (xmm1, reg1)
        code += 'vpinsrd %s, %s, %s, 0x1\n' % (xmm1, xmm1, reg2)
        code += 'vpinsrd %s, %s, %s, 0x2\n' % (xmm1, xmm1, reg3)
        code += 'vpinsrd %s, %s, %s, 0x3\n' % (xmm1, xmm1, reg4)
    else:
        code = 'movd %s, %s\n' % (xmm1, reg1)
        code += 'pinsrd %s, %s, 0x1\n' % (xmm1, reg2)
        code += 'pinsrd %s, %s, 0x2\n' % (xmm1, reg3)
        code += 'pinsrd %s, %s, 0x3\n' % (xmm1, reg4)

    return code, xmm1, Int32x4Arg


def int32x4_name_x4(cgen, name1, name2, name3, name4):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)
    arg3 = cgen.get_arg(name3)
    arg4 = cgen.get_arg(name4)

    if not (isinstance(arg1, Int32Arg) and isinstance(arg2, Int32Arg) and
            isinstance(arg3, Int32Arg) and isinstance(arg4, Int32Arg)):
        raise TypeError("Callable int32x4 doesn't support arguments ", arg1, arg2, arg3)

    xmm = cgen.register('xmm')
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vmovd %s, dword [%s]\n' % (xmm, arg1.name)
        code += 'vpinsrd %s, %s, dword [%s], 0x1\n' % (xmm, xmm, arg2.name)
        code += 'vpinsrd %s, %s, dword [%s], 0x2\n' % (xmm, xmm, arg3.name)
        code += 'vpinsrd %s, %s, dword [%s], 0x3\n' % (xmm, xmm, arg4.name)
    else:
        code = 'movd %s, dword [%s]\n' % (xmm, arg1.name)
        code += 'pinsrd %s, dword [%s], 0x1\n' % (xmm, arg2.name)
        code += 'pinsrd %s, dword [%s], 0x2\n' % (xmm, arg3.name)
        code += 'pinsrd %s, dword [%s], 0x3\n' % (xmm, arg4.name)
    return code, xmm, Int32x4Arg


def int32x4_i32x2_i32x2(cgen, xmm1, xmm2):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpunpcklqdq %s, %s, %s\n' % (xmm1, xmm1, xmm2)
    else:
        code = 'punpcklqdq %s, %s\n' % (xmm1, xmm2)
    return code, xmm1, Int32x4Arg


def int32x4_i32x3_i32(cgen, xmm, reg):
    if cgen.cpu.AVX or cgen.cpu.AVX512F:
        code = 'vpinsrd %s, %s, %s, 0x3\n' % (xmm, xmm, reg)
    else:
        code = 'pinsrd %s, %s, 0x3\n' % (xmm, reg)
    return code, xmm, Int32x4Arg


def int32x4_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Int32x2Arg) and isinstance(arg2, Int32x2Arg):
        code, xmm, arg_typ = arg1.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code += 'vmovhpd %s, %s, qword [%s]\n' % (xmm, xmm, arg2.name)
        else:
            code += 'movhpd %s, qword [%s]\n' % (xmm, arg2.name)
        return code, xmm, Int32x4Arg
    elif isinstance(arg1, Int32x3Arg) and isinstance(arg2, Int32Arg):
        code, xmm, arg_typ = arg1.load_cmd(cgen)
        if cgen.cpu.AVX or cgen.cpu.AVX512F:
            code += 'vpinsrd %s, %s, dword [%s], 0x3\n' % (xmm, xmm, arg2.name)
        else:
            code += 'pinsrd %s, dword [%s], 0x3\n' % (xmm, arg2.name)
        return code, xmm, Int32x4Arg
    else:
        raise TypeError("Callable int32x4 doesn't support arguments ", arg1, arg2)


register_built_in('int32x4', tuple(), int32x4_empty)
register_built_in('int32x4', (Const,), int32x4_const)
register_built_in('int32x4', (Const, Const, Const, Const), int32x4_const_x4)
register_built_in('int32x4', (Int32Arg,), int32x4_i32)
register_built_in('int32x4', (Int32x4Arg,), int32x4_i32x4)
register_built_in('int32x4', (Float32x4Arg,), int32x4_f32x4)
register_built_in('int32x4', (Float64x4Arg,), int32x4_f64x4)
register_built_in('int32x4', (Int64x4Arg,), int32x4_i64x4)
register_built_in('int32x4', (Name,), int32x4_name)
register_built_in('int32x4', (Int32Arg, Int32Arg, Int32Arg, Int32Arg), int32x4_i32_x4)
register_built_in('int32x4', (Name, Name, Name, Name), int32x4_name_x4)
register_built_in('int32x4', (Int32x2Arg, Int32x2Arg), int32x4_i32x2_i32x2)
register_built_in('int32x4', (Int32x3Arg, Int32Arg), int32x4_i32x3_i32)
register_built_in('int32x4', (Name, Name), int32x4_name_name)


def int32x8_empty(cgen):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        if cgen.cpu.AVX512F:
            code = 'vpxord %s, %s, %s\n' % (ymm, ymm, ymm)
        else:
            code = 'vpxor %s, %s, %s\n' % (ymm, ymm, ymm)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'vpxor %s, %s, %s\n' % (xmms[0], xmms[0], xmms[0])
        code += 'vpxor %s, %s, %s\n' % (xmms[1], xmms[1], xmms[1])
        return code, xmms, Int32x8Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'pxor %s, %s\n' % (xmms[0], xmms[0])
        code += 'pxor %s, %s\n' % (xmms[1], xmms[1])
        return code, xmms, Int32x8Arg


def int32x8_const(cgen, con):
    if con.value == 0:
        return int32x8_empty(cgen)
    arg = Int32x8Arg(value=int32x8(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x8_const_x8(cgen, con1, con2, con3, con4, con5, con6, con7, con8):
    val = int32x8(con1.value, con2.value, con3.value, con4.value,
                  con5.value, con6.value, con7.value, con8.value)
    arg = Int32x8Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x8_i32x8(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        return '', reg, Int32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_i32x4(xmm1, ptr_reg=reg)
        code += cgen.gen.load_i32x4(xmm2, ptr_reg=reg, offset=16)
        return code, (xmm1, xmm2), Int32x8Arg


def int32x8_i32(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        xmm = cgen.register('xmm')
        code = 'vmovd %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastd %s, %s\n' % (ymm, xmm)
        cgen.release_reg(xmm)
        return code, ymm, Int32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        if cgen.cpu.AVX:
            code = 'vmovd %s, %s\n' % (xmm1, reg)
        else:
            code = 'movd %s, %s\n' % (xmm1, reg)
        code += cgen.gen.broadcast_i32(xmm1)
        code += cgen.gen.move_reg(xmm2, xmm1)
        return code, (xmm1, xmm2), Int32x8Arg


def int32x8_f32x8(cgen, reg):
    if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvttps2dq %s, %s\n' % (ymm, reg)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        ymm = cgen.register('ymm')
        code = 'vcvttps2dq %s, %s\n' % (ymm, reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm2, ymm)
        code += 'vmovaps %s, %s\n' % (xmm1, 'x' + ymm[1:])
        cgen.release_reg(ymm)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvttps2dq %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvttps2dq %s, oword [%s + 16]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int32x8Arg


def int32x8_f64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vcvttpd2dq %s, %s\n' % (ymm, reg)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX2:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        ymm = cgen.register('ymm')
        code = 'vcvttpd2dq %s, yword[%s]\n' % (xmm1, reg)
        code += 'vcvttpd2dq %s, yword[%s + 32]\n' % (xmm2, reg)
        code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        return code, ymm, Int32x8Arg
    if cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'vcvttpd2dq %s, yword[%s]\n' % (xmm1, reg)
        code += 'vcvttpd2dq %s, yword[%s + 32]\n' % (xmm2, reg)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm = cgen.register('xmm')
        code = 'cvttpd2dq %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvttpd2dq %s, oword [%s + 16]\n' % (xmm, reg)
        code += 'movlhps %s, %s\n' % (xmm1, xmm)
        code += 'cvttpd2dq %s, oword [%s + 32]\n' % (xmm2, reg)
        code += 'cvttpd2dq %s, oword [%s + 48]\n' % (xmm, reg)
        code += 'movlhps %s, %s\n' % (xmm2, xmm)
        cgen.release_reg(xmm)
        return code, (xmm1, xmm2), Int32x8Arg


def int32x8_i64x8(cgen, reg):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vpmovsqd %s, %s\n' % (ymm, reg)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX2:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm = cgen.register('xmm')
        ymm = cgen.register('ymm')
        code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm1, reg)
        code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm, reg)
        code += 'vmovlhps %s, %s, %s\n' % (xmm1, xmm1, xmm)
        code += 'vpshufd %s, oword[%s + 32], 0x8\n' % (xmm2, reg)
        code += 'vpshufd %s, oword[%s + 48], 0x8\n' % (xmm, reg)
        code += 'vmovlhps %s, %s, %s\n' % (xmm2, xmm2, xmm)
        code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        cgen.release_reg(xmm1)
        cgen.release_reg(xmm2)
        cgen.release_reg(xmm)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm = cgen.register('xmm')
        code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm1, reg)
        code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm, reg)
        code += 'vmovlhps %s, %s, %s\n' % (xmm1, xmm1, xmm)
        code += 'vpshufd %s, oword[%s + 32], 0x8\n' % (xmm2, reg)
        code += 'vpshufd %s, oword[%s + 48], 0x8\n' % (xmm, reg)
        code += 'vmovlhps %s, %s, %s\n' % (xmm2, xmm2, xmm)
        return code, (xmm1, xmm2), Int32x8Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm = cgen.register('xmm')
        code = 'pshufd %s, oword[%s], 0x8\n' % (xmm1, reg)
        code += 'pshufd %s, oword[%s + 16], 0x8\n' % (xmm, reg)
        code += 'movlhps %s, %s\n' % (xmm1, xmm)
        code += 'pshufd %s, oword[%s + 32], 0x8\n' % (xmm2, reg)
        code += 'pshufd %s, oword[%s + 48], 0x8\n' % (xmm, reg)
        code += 'movlhps %s, %s\n' % (xmm2, xmm)
        cgen.release_reg(xmm)
        return code, (xmm1, xmm2), Int32x8Arg


def int32x8_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int32Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vpbroadcastd %s, dword [%s]\n' % (ymm, arg.name)
            return code, ymm, Int32x8Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            if cgen.cpu.AVX:
                code = 'vmovd %s, dword [%s]\n' % (xmm1, arg.name)
            else:
                code = 'movd %s, dword [%s]\n' % (xmm1, arg.name)
            code += cgen.gen.broadcast_i32(xmm1)
            code += cgen.gen.move_reg(xmm2, xmm1)
            return code, (xmm1, xmm2), Int32x8Arg
    elif isinstance(arg, Float64x8Arg):
        if cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvttpd2dq %s, zword[%s]\n' % (ymm, arg.name)
            return code, ymm, Int32x8Arg
        elif cgen.cpu.AVX2:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            ymm = cgen.register('ymm')
            code = 'vcvttpd2dq %s, yword[%s]\n' % (xmm1, arg.name)
            code += 'vcvttpd2dq %s, yword[%s + 32]\n' % (xmm2, arg.name)
            code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
            cgen.release_reg(xmm1)
            cgen.release_reg(xmm2)
            return code, ymm, Int32x8Arg
        if cgen.cpu.AVX:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            code = 'vcvttpd2dq %s, yword[%s]\n' % (xmm1, arg.name)
            code += 'vcvttpd2dq %s, yword[%s + 32]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Int32x8Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            xmm = cgen.register('xmm')
            code = 'cvttpd2dq %s, oword [%s]\n' % (xmm1, arg.name)
            code += 'cvttpd2dq %s, oword [%s + 16]\n' % (xmm, arg.name)
            code += 'movlhps %s, %s\n' % (xmm1, xmm)
            code += 'cvttpd2dq %s, oword [%s + 32]\n' % (xmm2, arg.name)
            code += 'cvttpd2dq %s, oword [%s + 48]\n' % (xmm, arg.name)
            code += 'movlhps %s, %s\n' % (xmm2, xmm)
            cgen.release_reg(xmm)
            return code, (xmm1, xmm2), Int32x8Arg
    elif isinstance(arg, Float32x8Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code = 'vcvttps2dq %s, yword[%s]\n' % (ymm, arg.name)
            return code, ymm, Int32x8Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            if cgen.cpu.AVX:
                code = 'vcvttps2dq %s, oword[%s]\n' % (xmm1, arg.name)
                code += 'vcvttps2dq %s, oword[%s + 16]\n' % (xmm2, arg.name)
            else:
                code = 'cvttps2dq %s, oword[%s]\n' % (xmm1, arg.name)
                code += 'cvttps2dq %s, oword[%s + 16]\n' % (xmm2, arg.name)
            return code, (xmm1, xmm2), Int32x8Arg
    elif isinstance(arg, Int32x8Arg):
        return arg.load_cmd(cgen)
    elif isinstance(arg, Int64x8Arg):
        if cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            code, zmm, typ = arg.load_cmd(cgen)
            code += 'vpmovsqd %s, %s\n' % (ymm, zmm)
            cgen.release_reg(zmm)
            return code, ymm, Int32x8Arg

        xmm1, xmm2 = cgen.register('xmm'), cgen.register('xmm')
        xmm = cgen.register('xmm')
        if cgen.cpu.AVX:
            code = 'vpshufd %s, oword[%s], 0x8\n' % (xmm1, arg.name)
            code += 'vpshufd %s, oword[%s + 16], 0x8\n' % (xmm, arg.name)
            code += 'vmovlhps %s, %s, %s\n' % (xmm1, xmm1, xmm)
            code += 'vpshufd %s, oword[%s + 32], 0x8\n' % (xmm2, arg.name)
            code += 'vpshufd %s, oword[%s + 48], 0x8\n' % (xmm, arg.name)
            code += 'vmovlhps %s, %s, %s\n' % (xmm2, xmm2, xmm)
            cgen.release_reg(xmm)
            if cgen.cpu.AVX2:
                ymm = cgen.register('ymm')
                code += 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
                cgen.release_reg(xmm1)
                cgen.release_reg(xmm2)
                return code, ymm, Int32x8Arg
            else:
                return code, (xmm1, xmm2), Int32x8Arg
        else:
            code = 'pshufd %s, oword[%s], 0x8\n' % (xmm1, arg.name)
            code += 'pshufd %s, oword[%s + 16], 0x8\n' % (xmm, arg.name)
            code += 'movlhps %s, %s\n' % (xmm1, xmm)
            code += 'pshufd %s, oword[%s + 32], 0x8\n' % (xmm2, arg.name)
            code += 'pshufd %s, oword[%s + 48], 0x8\n' % (xmm, arg.name)
            code += 'movlhps %s, %s\n' % (xmm2, xmm)
            cgen.release_reg(xmm)
            return code, (xmm1, xmm2), Int32x8Arg
    else:
        raise TypeError("Callable int32x8 doesn't support argument ", arg)


def int32x8_i32x4_i32x4(cgen, xmm1, xmm2):
    if cgen.cpu.AVX512F:
        ymm = cgen.register('ymm')
        code = 'vinserti32x4 %s, %s, %s, 0\n' % (ymm, ymm, xmm1)
        code += 'vinserti32x4 %s, %s, %s, 1\n' % (ymm, ymm, xmm2)
        return code, ymm, Int32x8Arg
    elif cgen.cpu.AVX2:
        ymm = cgen.register('ymm')
        code = 'vperm2f128 %s, %s, %s, 0x20\n' % (ymm, 'y' + xmm1[1:], 'y' + xmm2[1:])
        return code, ymm, Int32x8Arg
    else:
        return '', (xmm1, xmm2), Int32x8Arg


def int32x8_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Int32x4Arg) and isinstance(arg2, Int32x4Arg):
        if cgen.cpu.AVX2 or cgen.cpu.AVX512F:
            ymm = cgen.register('ymm')
            if cgen.cpu.AVX512F:
                code1 = 'vinserti32x4 %s, %s, oword [%s], 0\n' % (ymm, ymm, arg1.name)
                code2 = 'vinserti32x4 %s, %s, oword [%s], 1\n' % (ymm, ymm, arg2.name)
            else:
                code1 = 'vmovaps %s, oword[%s]\n' % ('x' + ymm[1:], arg1.name)
                code2 = 'vinserti128 %s, %s, oword [%s], 0x1\n' % (ymm, ymm, arg2.name)
            return code1 + code2, ymm, Int32x8Arg
        else:
            code1, xmm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (xmm1, xmm2), Int32x8Arg
    else:
        raise TypeError("Callable int32x8 doesn't support arguments ", arg1, arg2)


register_built_in('int32x8', tuple(), int32x8_empty)
register_built_in('int32x8', (Const,), int32x8_const)
register_built_in('int32x8', (Const, Const, Const, Const, Const, Const, Const, Const), int32x8_const_x8)
register_built_in('int32x8', (Int32x8Arg,), int32x8_i32x8)
register_built_in('int32x8', (Int32Arg,), int32x8_i32)
register_built_in('int32x8', (Float32x8Arg,), int32x8_f32x8)
register_built_in('int32x8', (Float64x8Arg,), int32x8_f64x8)
register_built_in('int32x8', (Int64x8Arg,), int32x8_i64x8)
register_built_in('int32x8', (Name,), int32x8_name)
register_built_in('int32x8', (Int32x4Arg, Int32x4Arg), int32x8_i32x4_i32x4)
register_built_in('int32x8', (Name, Name), int32x8_name_name)


def int32x16_empty(cgen):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vpxord %s, %s, %s\n' % (zmm, zmm, zmm)
        return code, zmm, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vpxor %s, %s, %s\n' % (ymm1, ymm1, ymm1)
        code += 'vpxor %s, %s, %s\n' % (ymm2, ymm2, ymm2)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmms = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = 'vpxor %s, %s, %s\n' % (xmms[0], xmms[0], xmms[0])
        code += 'vpxor %s, %s, %s\n' % (xmms[1], xmms[1], xmms[1])
        code += 'vpxor %s, %s, %s\n' % (xmms[2], xmms[2], xmms[2])
        code += 'vpxor %s, %s, %s\n' % (xmms[3], xmms[3], xmms[3])
        return code, xmms, Int32x16Arg
    else:
        xmms = (cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'), cgen.register('xmm'))
        code = 'pxor %s, %s\n' % (xmms[0], xmms[0])
        code += 'pxor %s, %s\n' % (xmms[1], xmms[1])
        code += 'pxor %s, %s\n' % (xmms[2], xmms[2])
        code += 'pxor %s, %s\n' % (xmms[3], xmms[3])
        return code, xmms, Int32x16Arg


def int32x16_const(cgen, con):
    if con.value == 0:
        return int32x16_empty(cgen)
    arg = Int32x16Arg(value=int32x16(con.value))
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x16_const_x16(cgen, con1, con2, con3, con4, con5, con6, con7, con8,
                       con9, con10, con11, con12, con13, con14, con15, con16):
    val = int32x16(con1.value, con2.value, con3.value, con4.value,
                   con5.value, con6.value, con7.value, con8.value,
                   con9.value, con10.value, con11.value, con12.value,
                   con13.value, con14.value, con15.value, con16.value)
    arg = Int32x16Arg(value=val)
    const_arg = cgen.create_const(arg)
    return const_arg.load_cmd(cgen)


def int32x16_i32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        return '', reg, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = cgen.gen.load_i32x8(ymm1, ptr_reg=reg)
        code += cgen.gen.load_i32x8(ymm2, ptr_reg=reg, offset=32)
        return code, (ymm1, ymm2), Int32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_i32x4(xmm1, ptr_reg=reg)
        code += cgen.gen.load_i32x4(xmm2, ptr_reg=reg, offset=16)
        code += cgen.gen.load_i32x4(xmm3, ptr_reg=reg, offset=32)
        code += cgen.gen.load_i32x4(xmm4, ptr_reg=reg, offset=48)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


def int32x16_i32(cgen, reg):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        xmm = cgen.register('xmm')
        code = 'vmovd %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastd %s, %s\n' % (zmm, xmm)
        cgen.release_reg(xmm)
        return code, zmm, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        xmm = cgen.register('xmm')
        code = 'vmovd %s, %s\n' % (xmm, reg)
        code += 'vpbroadcastd %s, %s\n' % (ymm1, xmm)
        code += 'vmovdqa %s, %s\n' % (ymm2, ymm1)
        cgen.release_reg(xmm)
        return code, (ymm1, ymm2), Int32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        if cgen.cpu.AVX:
            code = 'vmovd %s, %s\n' % (xmm1, reg)
        else:
            code = 'movd %s, %s\n' % (xmm1, reg)
        code += cgen.gen.broadcast_i32(xmm1)
        code += cgen.gen.move_reg(xmm2, xmm1)
        code += cgen.gen.move_reg(xmm3, xmm1)
        code += cgen.gen.move_reg(xmm4, xmm1)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


def int32x16_f32x16(cgen, reg):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vcvttps2dq %s, %s\n' % (zmm, reg)
        return code, zmm, Int32x16Arg
    elif cgen.cpu.AVX2:
        ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
        code = 'vcvttps2dq %s, yword [%s]\n' % (ymm1, reg)
        code += 'vcvttps2dq %s, yword [%s + 32]\n' % (ymm2, reg)
        return code, (ymm1, ymm2), Int32x16Arg
    elif cgen.cpu.AVX:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        ymm = cgen.register('ymm')
        code = 'vcvttps2dq %s, yword[%s]\n' % (ymm, reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm2, ymm)
        code += 'vmovaps %s, %s\n' % (xmm1, 'x' + ymm[1:])
        code += 'vcvttps2dq %s, yword[%s + 32]\n' % (ymm, reg)
        code += 'vextractf128 %s, %s, 1\n' % (xmm4, ymm)
        code += 'vmovaps %s, %s\n' % (xmm3, 'x' + ymm[1:])
        cgen.release_reg(ymm)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = 'cvttps2dq %s, oword [%s]\n' % (xmm1, reg)
        code += 'cvttps2dq %s, oword [%s + 16]\n' % (xmm2, reg)
        code += 'cvttps2dq %s, oword [%s + 32]\n' % (xmm3, reg)
        code += 'cvttps2dq %s, oword [%s + 48]\n' % (xmm4, reg)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


def int32x16_name(cgen, name):
    arg = cgen.get_arg(name)
    if isinstance(arg, Int32Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vpbroadcastd %s, dword [%s]\n' % (zmm, arg.name)
            return code, zmm, Int32x16Arg
        elif cgen.cpu.AVX2:
            ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vpbroadcastd %s, dword [%s]\n' % (ymm1, arg.name)
            code += 'vmovdqa %s, %s\n' % (ymm2, ymm1)
            return code, (ymm1, ymm2), Int32x16Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
            if cgen.cpu.AVX:
                code = 'vmovd %s, dword [%s]\n' % (xmm1, arg.name)
            else:
                code = 'movd %s, dword [%s]\n' % (xmm1, arg.name)
            code += cgen.gen.broadcast_i32(xmm1)
            code += cgen.gen.move_reg(xmm2, xmm1)
            code += cgen.gen.move_reg(xmm3, xmm1)
            code += cgen.gen.move_reg(xmm4, xmm1)
            return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    elif isinstance(arg, Float32x16Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vcvttps2dq %s, zword[%s]\n' % (zmm, arg.name)
            return code, zmm, Int32x16Arg
        elif cgen.cpu.AVX2:
            ymm1, ymm2 = (cgen.register('ymm'), cgen.register('ymm'))
            code = 'vcvttps2dq %s, yword[%s]\n' % (ymm1, arg.name)
            code += 'vcvttps2dq %s, yword[%s + 32]\n' % (ymm2, arg.name)
            return code, (ymm1, ymm2), Int32x16Arg
        else:
            xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
            xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
            if cgen.cpu.AVX:
                code = 'vcvttps2dq %s, oword[%s]\n' % (xmm1, arg.name)
                code += 'vcvttps2dq %s, oword[%s + 16]\n' % (xmm2, arg.name)
                code += 'vcvttps2dq %s, oword[%s + 32]\n' % (xmm3, arg.name)
                code += 'vcvttps2dq %s, oword[%s + 48]\n' % (xmm4, arg.name)
            else:
                code = 'cvttps2dq %s, oword[%s]\n' % (xmm1, arg.name)
                code += 'cvttps2dq %s, oword[%s + 16]\n' % (xmm2, arg.name)
                code += 'cvttps2dq %s, oword[%s + 32]\n' % (xmm3, arg.name)
                code += 'cvttps2dq %s, oword[%s + 48]\n' % (xmm4, arg.name)
            return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg
    elif isinstance(arg, Int32x16Arg):
        return arg.load_cmd(cgen)
    else:
        raise TypeError("Callable int32x16 doesn't support argument ", arg)


def int32x16_i32x8_i32x8(cgen, reg1, reg2):
    if cgen.cpu.AVX512F:
        zmm = cgen.register('zmm')
        code = 'vinserti32x8 %s, %s, %s, 0\n' % (zmm, zmm, reg1)
        code += 'vinserti32x8 %s, %s, %s, 1\n' % (zmm, zmm, reg2)
        return code, zmm, Int32x16Arg
    elif cgen.cpu.AVX2:
        return '', (reg1, reg2), Int32x16Arg
    else:
        xmm1, xmm2 = (cgen.register('xmm'), cgen.register('xmm'))
        xmm3, xmm4 = (cgen.register('xmm'), cgen.register('xmm'))
        code = cgen.gen.load_i32x4(xmm1, ptr_reg=reg1)
        code += cgen.gen.load_i32x4(xmm2, ptr_reg=reg1, offset=16)
        code += cgen.gen.load_i32x4(xmm3, ptr_reg=reg2)
        code += cgen.gen.load_i32x4(xmm4, ptr_reg=reg2, offset=16)
        return code, (xmm1, xmm2, xmm3, xmm4), Int32x16Arg


def int32x16_name_name(cgen, name1, name2):
    arg1 = cgen.get_arg(name1)
    arg2 = cgen.get_arg(name2)

    if isinstance(arg1, Int32x8Arg) and isinstance(arg2, Int32x8Arg):
        if cgen.cpu.AVX512F:
            zmm = cgen.register('zmm')
            code = 'vinserti32x8 %s, %s, yword[%s], 0\n' % (zmm, zmm, arg1.name)
            code += 'vinserti32x8 %s, %s, yword[%s], 1\n' % (zmm, zmm, arg2.name)
            return code, zmm, Int32x16Arg
        elif cgen.cpu.AVX2:
            code1, ymm1, arg_typ1 = arg1.load_cmd(cgen)
            code2, ymm2, arg_typ2 = arg2.load_cmd(cgen)
            return code1 + code2, (ymm1, ymm2), Int32x16Arg
        else:
            code1, xmms1, arg_typ1 = arg1.load_cmd(cgen)
            code2, xmms2, arg_typ2 = arg2.load_cmd(cgen)
            xmms = xmms1 + xmms2
            return code1 + code2, xmms, Int32x16Arg
    else:
        raise TypeError("Callable int32x16 doesn't support arguments ", arg1, arg2)


register_built_in('int32x16', tuple(), int32x16_empty)
register_built_in('int32x16', (Const,), int32x16_const)
register_built_in('int32x16', (Const, Const, Const, Const, Const, Const, Const, Const,
                               Const, Const, Const, Const, Const, Const, Const, Const), int32x16_const_x16)
register_built_in('int32x16', (Int32x16Arg,), int32x16_i32x16)
register_built_in('int32x16', (Int32Arg,), int32x16_i32)
register_built_in('int32x16', (Float32x16Arg,), int32x16_f32x16)
register_built_in('int32x16', (Name,), int32x16_name)
register_built_in('int32x16', (Int32x8Arg, Int32x8Arg), int32x16_i32x8_i32x8)
register_built_in('int32x16', (Name, Name), int32x16_name_name)
