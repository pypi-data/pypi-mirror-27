
import operator
from inspect import signature
from .holders import Const, Operations, Callable, Attribute, Name, Subscript, CompileError
from .int_arg import Int32Arg, Int64Arg, int32, int64
from .flt_arg import Float32Arg, float32
from .dbl_arg import Float64Arg, float64
from .flt_vec_arg import Float32VecBase
from .dbl_vec_arg import Float64VecBase
from .acum import Acums, move_regs_to_acums
from .arr import StackedArrayArg
from .ptr import PointerArg
from .opt import FunctionOptimizer


def load_const_operand(cgen, value):
    if isinstance(value, int):
        reg = cgen.register('general')
        if value is False or value is True:
            raise CompileError("Bool constant not supported.")
        if value > 2147483647 or value < -2147483648:
            raise CompileError("Constant %i falls outside 32-bit range." % value)
        code = cgen.gen.load_i32(reg, value=value)
        return code, reg, Int32Arg
    elif isinstance(value, float):
        if value == 0.0:
            xmm = cgen.register('xmm')
            if cgen.cpu.AVX:
                code = "vxorps %s, %s, %s\n" % (xmm, xmm, xmm)
            else:
                code = "xorps %s, %s\n" % (xmm, xmm)
            return code, xmm, Float64Arg
        arg = Float64Arg(value=float64(value))
        const_arg = cgen.create_const(arg)
        return const_arg.load_cmd(cgen)
    else:
        raise CompileError("Not supported constant %s" % str(value))


def get_arg_from_storage(cgen, operand, rest_oprs):
    reg1 = None
    code = ''
    if cgen.in_cache(operand.cache_key()):
        _, reg1, typ1 = process_operand(cgen, operand, rest_oprs=rest_oprs)
        arg1 = cgen.arg_factory(typ1)
    elif hasattr(operand, 'unary_op') and operand.unary_op:
        code, reg1, typ1 = process_operand(cgen, operand, rest_oprs=rest_oprs)
        arg1 = cgen.arg_factory(typ1)
    else:
        arg1 = cgen.get_arg(operand)
    return code, arg1, reg1


def release_regs(cgen, acum, *regs):
    for reg in regs:
        if reg is not None and reg != acum:
            cgen.release_reg(reg)


def _load_subscript(cgen, code, operand, arg, ptr_reg):
    index, reg = None, None
    if isinstance(operand.index, Const) and isinstance(operand.index.value, int):
        index = operand.index.value
    else:
        code, reg, arg_type = process_expression(cgen, operand.index)
        if arg_type is not Int32Arg and arg_type is not Int64Arg:
            raise CompileError("Subscript index must be integer!")

    if isinstance(operand.path, Attribute):
        code2, reg2, arg_type2 = arg.load_attr_item_cmd(cgen, operand.path.path, index=index, reg=reg, ptr_reg=ptr_reg)
    else:
        code2, reg2, arg_type2 = arg.load_item_cmd(cgen, index=index, reg=reg, ptr_reg=ptr_reg)
    release_regs(cgen, reg2, reg, ptr_reg)
    return code + code2, reg2, arg_type2


def load_subscript_operand(cgen, operand):
    code, arg, ptr_reg = get_arg_from_storage(cgen, operand.path, [])
    if arg is None:
        raise CompileError("Operand %s doesn't exist" % operand.path.name)

    return _load_subscript(cgen, code, operand, arg, ptr_reg)


def convert_to_fn_arg(arg_typ, cgen, reg):
    if isinstance(reg, tuple):
        arg = cgen.create_tmp_arg(arg_typ)
        code = arg.store_cmd(cgen, reg)
        cgen.release_reg(reg)
        ptr_reg = cgen.register('pointer')
        code += cgen.gen.load_addr(ptr_reg, arg.name)
        return code, ptr_reg
    return '', reg


def load_expressions(cgen, operands):

    def convert_multi_arg(arg_typ, reg):
        arg = cgen.create_tmp_arg(arg_typ)
        code = arg.store_cmd(cgen, reg)
        cgen.release_reg(reg)
        ptr_reg = cgen.register('pointer')
        code += cgen.gen.load_addr(ptr_reg, arg.name)
        return code, ptr_reg, arg

    def save_loaded_args(typs, regs, args, n):
        code = ''
        for i in range(n):
            if regs[i] != None:
                arg = cgen.create_tmp_arg(typs[i])
                code += arg.store_cmd(cgen, regs[i])
                cgen.release_reg(regs[i])
                regs[i] = None
                args[i] = arg
        return code

    def load_tmp_arg(arg):
        if arg.is_multi_part(cgen):
            reg = cgen.register('pointer')
            code = cgen.gen.load_addr(reg, arg.name)
        else:
            code, reg, arg_typ = arg.load_cmd(cgen)
        return code, reg

    typs, regs, args = [], [], []
    code = ''
    for index, op in enumerate(operands):
        reg, arg_typ, arg = None, None, None
        if not isinstance(op, (Name, Const, Attribute)):
            co = save_loaded_args(typs, regs, args, index)
            code += co

            co, reg, arg_typ = process_expression(cgen, op)
            code += co

        typs.append(arg_typ)
        regs.append(reg)
        args.append(arg)

    for index, op in enumerate(operands):
        if regs[index] is not None:
            if isinstance(regs[index], tuple):
                co, ptr_reg, arg = convert_multi_arg(typs[index], regs[index])
                code += co
                regs[index] = ptr_reg
                args[index] = arg
        else:
            if args[index] is not None:
                co, reg = load_tmp_arg(args[index])
                code += co
                regs[index] = reg
            else:
                co, reg, arg_typ = process_expression(cgen, op)
                code += co
                if isinstance(reg, tuple):
                    co, ptr_reg, arg = convert_multi_arg(arg_typ, reg)
                    code += co
                    args[index] = arg
                    regs[index] = ptr_reg
                else:
                    regs[index] = reg
                typs[index] = arg_typ

    return code, typs, regs, args


def save_stack_load_fn_args(cgen, operand, stack, ad_arg_typs):
    code, stack_args, ad_args = '', [], []

    for reg, arg_type in stack:
        arg = cgen.create_tmp_arg(arg_type)
        code += arg.store_cmd(cgen, reg)
        stack_args.append(arg)

    for reg, arg_type in ad_arg_typs:
        arg = cgen.create_tmp_arg(arg_type)
        code += arg.store_cmd(cgen, reg)
        ad_args.append(arg)

    cgen.clear_regs()
    co, typs, regs, args = load_expressions(cgen, operand.args)
    code += co

    return code, stack_args, ad_args, (typs, regs, args)


def return_saved_args(cgen, stack, ad_arg_typs, stack_args, ad_args):
    code = ''
    for index, arg in enumerate(stack_args):
        co, reg, arg_typ = arg.load_cmd(cgen)
        code += co
        old_reg, arg_typ = stack[index]
        stack[index] = (reg, arg_typ)
    for index, arg in enumerate(ad_args):
        co, reg, arg_typ = arg.load_cmd(cgen)
        code += co
        old_reg, arg_typ = ad_arg_typs[index]
        ad_arg_typs[index] = (reg, arg_typ)
    return code


def return_default_arg(cgen, stack, ad_arg_typs, stack_args, ad_args):
    code = return_saved_args(cgen, stack, ad_arg_typs, stack_args, ad_args)
    reg = cgen.register('general')
    code += 'xor %s, %s\n' % (reg, reg)
    ret_types = (Int32Arg,)
    regs = [reg]
    return code, ret_types, regs


def retruned_fn_args(cgen, ret_types, operand, stack, ad_arg_typs, stack_args, ad_args):
    if len(ret_types) > 1:
        raise CompileError("TODO Function/Kernel can return multiple values!")
    code = ''
    acums = Acums()
    regs, args = [], []
    for typ in ret_types:
        arg = cgen.arg_factory(typ)
        reg = acums.pop_type(cgen, arg)
        regs.append(reg)
        args.append(arg)
    cgen.allocate_regs(regs)
    for index, arg in enumerate(args):
        if arg.is_multi_part(cgen):
            co, new_regs, new_typ = arg.load_cmd(cgen, ptr_reg=regs[index])
            code += co
            cgen.release_reg(regs[index])
            regs[index] = new_regs

    code += return_saved_args(cgen, stack, ad_arg_typs, stack_args, ad_args)
    return code, regs


def process_local_fn(cgen, operand, stack=[], ad_arg_typs=[]):
    code, stack_args, ad_args, (typs, regs, fn_args) = save_stack_load_fn_args(cgen, operand, stack, ad_arg_typs)
    fn_stm = cgen.get_local_fn(operand.name, typs)

    cgen.create_local_scope(operand.name, fn_stm.body)
    for typ, reg, farg in zip(typs, regs, fn_stm.args):
        arg = cgen.create_arg(Name(farg.name), typ)
        if arg.is_multi_part(cgen):
            co, regs, new_typ = arg.load_cmd(cgen, ptr_reg=reg)
            code += co
            code += arg.store_cmd(cgen, regs)
        else:
            code += arg.store_cmd(cgen, reg)
    code += ''.join(cgen.stm_code(s) for s in fn_stm.body)
    ret = cgen.get_return_type()
    cgen.clear_regs()
    code += '%s:\n' % cgen.return_label()
    stores = cgen.destroy_local_scope()

    if ret is None:
        co, ret_types, regs = return_default_arg(cgen, stack, ad_arg_typs, stack_args, ad_args)
        code += co
    else:
        if not fn_stm.body[-1].is_return():
            raise CompileError("Expected return as last statemnt in %s." % operand.name)
        ret_types = ret
        co, regs = retruned_fn_args(cgen, ret_types, operand, stack, ad_arg_typs, stack_args, ad_args)
        code += co

    if cgen._optimize:
        fun_opt = FunctionOptimizer(cgen, code, stores)
        code = fun_opt.optimize()

    for arg in stack_args + ad_args + fn_args:
        if arg is not None:
            cgen.release_tmp_arg(arg)

    if len(fn_stm.ret_type_names) == 0:
        return code, regs, ret_types
    else:
        if len(fn_stm.ret_type_names) != len(ret_types):
            raise CompileError("Callable %s must return %i values." % (operand.name, len(fn_stm.ret_type_names)))
        for typ_name, arg_typ in zip(fn_stm.ret_type_names, ret_types):
            if typ_name != arg_typ.type_name():
                raise CompileError("Wrong return type got %s expected %s." %
                                   (arg_typ.type_name(), typ_name))
        return code, regs, ret_types


def conv_loc_array(cgen, key, regs):
    code = ''
    for k, r in zip(key, regs):
        if k.is_pointer() and isinstance(k.arg, StackedArrayArg):
            name = cgen.struct_for_loc_array(k.arg)
            code += cgen.gen.load_addr(r, name)
    return code


def process_built_in(cgen, operand, stack=[], ad_arg_typs=[]):
    def release_built_in_regs(cgen, ret_reg, reg_args):
        for reg in reg_args:
            if isinstance(reg, tuple):
                reg, _ = reg
            if isinstance(ret_reg, tuple):
                if reg not in ret_reg:
                    cgen.release_reg(reg)
            elif reg != ret_reg:
                cgen.release_reg(reg)

    def should_save_stack(operands):
        # TODO simple operations are also allowed
        for op in operands:
            if not isinstance(op, (Name, Const, Attribute)):
                return True
        return False

    must_save_stack = should_save_stack(operand.args)
    code, stack_args, ad_args = '', [], []
    if must_save_stack:
        for reg, arg_type in stack:
            arg = cgen.create_tmp_arg(arg_type)
            code += arg.store_cmd(cgen, reg)
            cgen.release_reg(reg)
            stack_args.append(arg)

        for reg, arg_type in ad_arg_typs:
            arg = cgen.create_tmp_arg(arg_type)
            code += arg.store_cmd(cgen, reg)
            cgen.release_reg(reg)
            ad_args.append(arg)

    for i in range(len(operand.args) + 1):
        right_key = tuple(type(arg) for arg in operand.args[i:])
        if cgen.has_right_key_builtin(operand.name, right_key):
            co, typs, regs, fn_args = load_expressions(cgen, operand.args[:i])
            code += co
            lkey = []
            for index, typ in enumerate(typs):
                if typ.is_pointer():
                    regs[index] = (regs[index], typ)
                    lkey.append(PointerArg)
                else:
                    lkey.append(typ)
            key = tuple(tuple(lkey) + right_key)
            callback = cgen.get_built_in(operand.name, key)
            if callback is not None:
                args = regs + [arg for arg in operand.args[i:]]
                co, reg, arg_typ = callback(cgen, *args)
                code += co
                release_built_in_regs(cgen, reg, regs)
                if must_save_stack:
                    code += return_saved_args(cgen, stack, ad_arg_typs, stack_args, ad_args)
                for arg in fn_args + stack_args + ad_args:
                    if arg is not None:
                        cgen.release_tmp_arg(arg)
                return code, reg, arg_typ

    raise CompileError("Callable %s exist, argument mismatch." % operand.name)


def process_kernel(cgen, operand, stack=[], ad_arg_typs=[]):

    code, stack_args, ad_args, (typs, regs, fn_args) = save_stack_load_fn_args(cgen, operand, stack, ad_arg_typs)
    kernel = cgen.get_kernel(operand.name, typs)
    if kernel is None:
        raise CompileError("Kernel %s exist, arguments mismatch." % operand.name)

    co = conv_loc_array(cgen, typs, regs)
    code += co
    code += move_regs_to_acums(cgen, regs)
    cgen.clear_regs()
    code += 'call %s\n' % kernel.internal_name

    if kernel.ret_type is None:
        co, ret_types, regs = return_default_arg(cgen, stack, ad_arg_typs, stack_args, ad_args)
        code += co
    else:
        ret_types = kernel.ret_type
        co, regs = retruned_fn_args(cgen, ret_types, operand, stack, ad_arg_typs, stack_args, ad_args)
        code += co

    for arg in stack_args + ad_args + fn_args:
        if arg is not None:
            cgen.release_tmp_arg(arg)

    return code, regs, ret_types


def process_struct(cgen, operand):
    cgen.clear_regs()
    code, typs, regs, args = load_expressions(cgen, operand.args)

    struct_arg = cgen.create_user_arg(operand.name)
    sig = signature(struct_arg.value.__init__)
    if len(typs) != len(sig.parameters):
        raise CompileError("User arg %s expect %i positional arguments." % (operand.name, len(sig.parameters)))

    co, ptr_reg, ptr_arg = struct_arg.load_cmd(cgen)
    code += co

    for idx, p in enumerate(sig.parameters):
        arg = struct_arg.get_arg(p)
        if arg.is_multi_part(cgen):
            co, new_regs, new_typ = arg.load_cmd(cgen, ptr_reg=regs[idx])
            code += co
            code += struct_arg.store_attr_cmd(cgen, p, new_typ, new_regs, ptr_reg=ptr_reg)
        else:
            code += struct_arg.store_attr_cmd(cgen, p, typs[idx], regs[idx], ptr_reg=ptr_reg)

    for arg in args:
        if arg is not None:
            cgen.release_tmp_arg(arg)
    return code, ptr_reg, ptr_arg


def process_callable_operand(cgen, operand, stack=[], ad_arg_typs=[]):
    if cgen.has_local_fn(operand.name):
        code, regs, typ = process_local_fn(cgen, operand, stack=stack, ad_arg_typs=ad_arg_typs)
        return code, regs, typ
    elif cgen.has_built_in(operand.name):
        code, regs, typ = process_built_in(cgen, operand, stack=stack, ad_arg_typs=ad_arg_typs)
        return code, regs, typ
    elif cgen.has_kernel(operand.name):
        code, regs, typ = process_kernel(cgen, operand, stack=stack, ad_arg_typs=ad_arg_typs)
        return code, regs, typ
    elif cgen.has_struct(operand.name):
        code, regs, typ = process_struct(cgen, operand)
        return code, regs, typ

    raise CompileError("Callable %s doesn't exist. " % operand.name)


def load_operand(cgen, operand, stack=[], ad_arg_typs=[]):
    if isinstance(operand, Const):
        return load_const_operand(cgen, operand.value)
    elif isinstance(operand, Name):
        arg = cgen.get_arg(operand)
        if arg is None:
            raise CompileError("Operand %s doesn't exist" % operand.name)
        return arg.load_cmd(cgen)
    elif isinstance(operand, Subscript):
        return load_subscript_operand(cgen, operand)
    elif isinstance(operand, Callable):
        return process_callable_operand(cgen, operand, stack=stack, ad_arg_typs=ad_arg_typs)
    elif isinstance(operand, Attribute):
        arg = cgen.get_arg(operand)
        if arg is None:
            raise CompileError("Operand %s doesn't exist" % operand.name)
        return arg.load_attr_cmd(cgen, operand.path)
    else:
        raise CompileError("Unsupported operand type.")


def can_be_removed_from_cache(operand, rest_oprs):
    key = operand.cache_key()
    if key is None:
        return False
    for operation in rest_oprs:
        left, right = operation.left, operation.right
        if left and left.cache_key() == key:
            return False
        if right and right.cache_key() == key:
            return False
    return True


def can_be_cached(operand, rest_oprs):
    key = operand.cache_key()
    if key is None:
        return False
    for operation in rest_oprs:
        left, right = operation.left, operation.right
        if left and left.cache_key() == key:
            return True
        if right and right.cache_key() == key:
            return True
    return False


def process_operand(cgen, operand, rest_oprs=[], stack=[], ad_arg_typs=[]):
    key = operand.cache_key()
    if cgen.in_cache(key):
        reg, typ = cgen.get_from_cache(key)
        code = ''
        if can_be_removed_from_cache(operand, rest_oprs):
            cgen.remove_from_cache(key)
    else:
        code, reg, typ = load_operand(cgen, operand, stack=stack, ad_arg_typs=ad_arg_typs)
        if isinstance(typ, tuple) and len(typ) == 1:
            reg, typ = reg[0], typ[0]

        if hasattr(operand, 'unary_op') and operand.unary_op:
            arg = cgen.arg_factory(typ)
            co, new_reg, new_typ = arg.do_unary_op(cgen, reg, operand.unary_op)
            code += co
            release_regs(cgen, new_reg, reg)
            reg = new_reg
        elif can_be_cached(operand, rest_oprs):  # NOTE: currently we don't put unary operands in cache - TODO!
            cgen.put_in_cache(key, reg, typ)

    return code, reg, typ


def can_convert_to(value, arg):
    if isinstance(value, (int, float)) and isinstance(arg, (Float32Arg, Float64Arg)):
        return True
    if isinstance(value, int) and isinstance(arg, (Int32Arg, Int64Arg)):
        return True
    return False


def load_const_of_type(cgen, value, arg):
    if isinstance(arg, Float32Arg):
        new_arg = Float32Arg(value=float32(value))
    elif isinstance(arg, Float64Arg):
        new_arg = Float64Arg(value=float64(value))
    elif isinstance(arg, Int32Arg):
        new_arg = Int32Arg(value=int32(value))
    elif isinstance(arg, Int64Arg):
        new_arg = Int64Arg(value=int64(value))
    elif isinstance(arg, (Float64VecBase, Float32VecBase)):
        new_arg = type(arg)(value=type(arg.value)(value))
    else:
        raise CompileError("Unsupported constant %s." % str(value))
    const_arg = cgen.create_const(new_arg)
    code, xmm, arg_type = const_arg.load_cmd(cgen)
    return code, const_arg, xmm


def handle_const_const(cgen, left, right, op, stack, rest_oprs, next_opr):
    operators = {'+': operator.add, '-': operator.sub,
                 '*': operator.mul, '/': operator.truediv,
                 '<<': operator.lshift, '>>': operator.rshift,
                 '^': operator.xor, '|': operator.or_,
                 '&': operator.and_, '%': operator.mod}

    if isinstance(left.value, float) or isinstance(right.value, float):
        val1, val2 = float(left.value), float(right.value)
        result = operators[op](val1, val2)
    else:
        val1, val2 = int(left.value), int(right.value)
        if op == '/':
            result = val1 // val2
        else:
            result = operators[op](left.value, right.value)

    code, reg, arg_type = load_const_operand(cgen, result)
    stack.append((reg, arg_type))
    return (code, reg, arg_type), False


def _can_fma(next_opr):
    left, right, op = next_opr.left, next_opr.right, next_opr.operator
    if op != '+' and op != '-':
        return False

    if left is not None and right is not None:
        return False

    return True


def _fma_operand(next_opr):
    left, right, op2 = next_opr.left, next_opr.right, next_opr.operator

    if left is None and right is None:
        reverse2 = True
        operand = None
    elif left is None:
        reverse2 = False
        operand = right
    elif right is None:
        reverse2 = True
        operand = left

    return operand, reverse2, op2


def _process_fma_operand(cgen, fma_op, stack, rest_oprs, req_arg, ad_arg_typs=[]):

    code3 = ''
    if fma_op is None:
        reg3, typ3 = stack.pop()
        arg3 = cgen.arg_factory(typ3)
    elif isinstance(fma_op, Name):
        co, arg3, reg3 = get_arg_from_storage(cgen, fma_op, rest_oprs)
        code3 += co
    else:
        if isinstance(fma_op, Const):
            if can_convert_to(fma_op.value, req_arg):
                code3, arg3, reg3 = load_const_of_type(cgen, fma_op.value, req_arg)
            else:
                raise CompileError("Fma const %s cannot be converted." % str(fma_op.value))
        else:
            code3, reg3, typ3 = process_operand(cgen, fma_op, rest_oprs=rest_oprs, stack=stack, ad_arg_typs=ad_arg_typs)
            arg3 = cgen.arg_factory(typ3)

    if not isinstance(arg3, type(req_arg)):
        raise CompileError("Operand type mismatch for FMA operation.")
    return code3, reg3, arg3


def _perform_fma(cgen, code, arg1, reg1, arg2, reg2, op, arg3, fma_op, stack, reverse, reg3, name):

    code4, reg4, typ4 = arg1.perform_fma(cgen, reg1, arg2, reg2, op, arg3, reverse, reg3=reg3, name=name)
    stack.append((reg4, typ4))
    release_regs(cgen, reg4, reg1, reg2, reg3)
    return (code + code4, reg4, typ4), True


def perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2):
    if arg1.fma_supported(cgen) and arg1.can_operate_with_arg(cgen, arg2, '*'):
        pass
    elif arg2.fma_supported(cgen) and arg2.can_operate_with_arg(cgen, arg1, '*'):
        arg1, reg1, arg2, reg2 = arg2, reg2, arg1, reg1
    else:
        raise CompileError("FMA operation cannot be handled.")

    fma_op, reverse, op2 = _fma_operand(next_opr)
    # TODO - Improved this - ArrayNFloats will not work??
    ad_arg_typs = [(reg1, type(arg1)), (reg2, type(arg2))]
    code3, reg3, arg3 = _process_fma_operand(cgen, fma_op, stack, rest_oprs, arg1, ad_arg_typs=ad_arg_typs)
    (reg1, arg_typ1), (reg2, arg_typ2) = ad_arg_typs
    code4, reg4, typ4 = arg1.fma_cmd(cgen, arg2, op2, reverse, arg3, reg1, reg2, reg3=reg3)
    stack.append((reg4, typ4))
    release_regs(cgen, reg4, reg1, reg2, reg3)
    return (code + code3 + code4, reg4, typ4), True


def handle_args(cgen, code, arg1, op, arg2, stack, rest_oprs, reg1=None, reg2=None, left_op=None, right_op=None):
    cml = ('+', '*', '&', '^', '|')
    co = ''

    if arg1.can_operate_with_arg(cgen, arg2, op):
        if reg1 is None and reg2 is not None and arg2.can_operate_with_arg(cgen, arg1, op) and op in cml:
            arg1, reg1, left_op, arg2, reg2, right_op = arg2, reg2, right_op, arg1, reg1, left_op
        elif reg1 is None:
            co, reg1, typ1 = process_operand(cgen, left_op, rest_oprs=rest_oprs)
    elif op in cml and arg2.can_operate_with_arg(cgen, arg1, op):
        arg1, reg1, left_op, arg2, reg2, right_op = arg2, reg2, right_op, arg1, reg1, left_op
        if reg1 is None:
            co, reg1, typ1 = process_operand(cgen, left_op, rest_oprs=rest_oprs)
    else:
        raise CompileError("Operation %s cannot be handled for type %s and %s." % (op, arg1.type_name(), arg2.type_name()))

    code3, reg3, typ3 = arg1.arith_arg_cmd(cgen, op, arg2, reg1, reg2=reg2)
    stack.append((reg3, typ3))
    release_regs(cgen, reg3, reg1, reg2)
    return (code + co + code3, reg3, typ3), False


def handle_args_reverse(cgen, code, arg1, op, arg2, stack, reverse, rest_oprs,
                        reg1=None, reg2=None, left_op=None, right_op=None):
    if reverse:
        return handle_args(cgen, code, arg2, op, arg1, stack, rest_oprs,
                           reg1=reg2, reg2=reg1, left_op=right_op, right_op=left_op)
    else:
        return handle_args(cgen, code, arg1, op, arg2, stack, rest_oprs,
                           reg1=reg1, reg2=reg2, left_op=left_op, right_op=right_op)


def handle_arg_const(cgen, code, arg1, reg1, value, op, stack):
    code2, reg2, typ2 = arg1.arith_with_const(cgen, reg1, op, value)
    stack.append((reg2, typ2))
    release_regs(cgen, reg2, reg1)
    return (code + code2, reg2, typ2), False


def handle_operand_const(cgen, code, arg1, reg1, op, con_op, reverse, stack, rest_oprs):
    cml = ('+', '*', '&', '^', '|')
    if reverse and op in cml and arg1.can_operate_with_const(cgen, op, con_op.value):
        return handle_arg_const(cgen, code, arg1, reg1, con_op.value, op, stack)
    elif reverse is False and arg1.can_operate_with_const(cgen, op, con_op.value):
        return handle_arg_const(cgen, code, arg1, reg1, con_op.value, op, stack)
    else:
        if can_convert_to(con_op.value, arg1):
            code2, arg2, reg2 = load_const_of_type(cgen, con_op.value, arg1)
        else:
            code2, reg2, typ2 = process_operand(cgen, con_op, rest_oprs=rest_oprs)
            arg2 = cgen.arg_factory(typ2)
        return handle_args_reverse(cgen, code + code2, arg1, op, arg2, stack, reverse, rest_oprs,
                                   reg1=reg1, reg2=reg2)


def handle_name_name(cgen, left, right, op, stack, rest_oprs, next_opr):
    co1, arg1, reg1 = get_arg_from_storage(cgen, left, rest_oprs)
    co2, arg2, reg2 = get_arg_from_storage(cgen, right, rest_oprs)
    code = co1 + co2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        code1 = code2 = ''
        if reg1 is None:
            code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs)
        if reg2 is None:
            code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
        return perform_fma_cmd(cgen, code + code1 + code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_args(cgen, code, arg1, op, arg2, stack, rest_oprs, reg1=reg1, reg2=reg2, left_op=left, right_op=right)


def handle_pure_args(cgen, code, arg1, reg1, op, arg2, reg2, stack):
    if not arg1.can_operate_with_arg(cgen, arg2, op):
        raise CompileError("Operation %s cannot be handled for type %s and %s." % (op, arg1.type_name(), arg2.type_name()))

    code3, reg3, typ3 = arg1.arith_with_arg(cgen, reg1, arg2, reg2, op)
    stack.append((reg3, typ3))
    release_regs(cgen, reg3, reg1, reg2)
    return (code + code3, reg3, typ3), False


def _handle_name_const(cgen, name_op, con_op, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, name_op, rest_oprs=rest_oprs)
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and arg1.fma_supported(cgen):
        code2, arg2, reg2 = load_const_of_type(cgen, con_op.value, arg1)
        return perform_fma_cmd(cgen, code1 + code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_operand_const(cgen, code1, arg1, reg1, op, con_op, reverse, stack, rest_oprs)


def handle_name_const(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_name_const(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_const_name(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_name_const(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def _fma_none_name(cgen, code, arg1, reg1, name_op, stack, next_opr, rest_oprs):
    arg2 = cgen.get_arg(name_op)
    fma_op, reverse, op = _fma_operand(next_opr)
    code2, reg2, typ2 = process_operand(cgen, name_op, rest_oprs=rest_oprs)
    code3, reg3, arg3, name = _process_fma_operand(cgen, fma_op, stack, rest_oprs, arg1)
    code = code + code2 + code3
    return _perform_fma(cgen, code, arg1, reg1, arg2, reg2,
                        op, arg3, fma_op, stack, reverse, reg3, name)


def _handle_none_name(cgen, name_op, op, stack, rest_oprs, next_opr, reverse):
    reg1, typ1 = stack.pop()
    arg1 = cgen.arg_factory(typ1)

    co, arg2, reg2 = get_arg_from_storage(cgen, name_op, rest_oprs)

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        code2 = co
        if reg2 is None:
            code2, reg2, typ2 = process_operand(cgen, name_op, rest_oprs=rest_oprs)
        return perform_fma_cmd(cgen, code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_args_reverse(cgen, co, arg1, op, arg2, stack, reverse, rest_oprs,
                               reg1=reg1, reg2=reg2, right_op=name_op)


def handle_none_name(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_name(cgen, right, op, stack, rest_oprs, next_opr, False)


def handle_name_none(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_name(cgen, left, op, stack, rest_oprs, next_opr, True)


def _fma_arg_arg(cgen, code, arg1, reg1, arg2, reg2, stack, next_opr, rest_oprs):
    fma_op, reverse, op = _fma_operand(next_opr)
    code3, reg3, arg3, name = _process_fma_operand(cgen, fma_op, stack, rest_oprs, arg1)
    return _perform_fma(cgen, code + code3, arg1, reg1, arg2, reg2, op, arg3, fma_op, stack, reverse, reg3, name)


def handle_both_args_fma(cgen, code, arg1, reg1, op, arg2, reg2, stack, next_opr, rest_oprs):
    if cgen.cpu.FMA and next_opr and op == '*' and _can_fma(next_opr):
        if arg1.fma_supported(cgen) and arg1.can_operate_with_arg(cgen, arg2, op):
            return _fma_arg_arg(cgen, code, arg1, reg1, arg2, reg2, stack, next_opr, rest_oprs)
    return handle_pure_args(cgen, code, arg1, reg1, op, arg2, reg2, stack)


def handle_none_none(cgen, left, right, op, stack, rest_oprs, next_opr):
    reg2, typ2 = stack.pop()
    arg2 = cgen.arg_factory(typ2)

    reg1, typ1 = stack.pop()
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, "", arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args(cgen, "", arg1, op, arg2, stack, rest_oprs, reg1=reg1, reg2=reg2)


def _handle_none_const(cgen, con_op, op, stack, rest_oprs, next_opr, reverse):

    reg1, typ1 = stack.pop()
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and arg1.fma_supported(cgen):
        code2, arg2, reg2 = load_const_of_type(cgen, con_op.value, arg1)
        return perform_fma_cmd(cgen, code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_operand_const(cgen, "", arg1, reg1, op, con_op, reverse, stack, rest_oprs)


def handle_none_const(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_const(cgen, right, op, stack, rest_oprs, next_opr, False)


def handle_const_none(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_const(cgen, left, op, stack, rest_oprs, next_opr, True)


def _handle_subscript_const(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and arg1.fma_supported(cgen):
        code2, arg2, reg2 = load_const_of_type(cgen, right.value, arg1)
        code = code1 + code2
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_operand_const(cgen, code1, arg1, reg1, op, right, reverse, stack, rest_oprs)


def handle_subscript_const(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_subscript_const(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_const_subscript(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_subscript_const(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def handle_subscript_subscript(cgen, left, right, op, stack, rest_oprs, next_opr):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)
    ad_arg_typs = [(reg1, typ1)]
    code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs, stack=stack, ad_arg_typs=ad_arg_typs)
    (reg1, typ1), = ad_arg_typs
    arg2 = cgen.arg_factory(typ2)
    code = code1 + code2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args(cgen, code, arg1, op, arg2, stack, rest_oprs, reg1=reg1, reg2=reg2)


def _handle_subscript_name(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)

    co, arg2, reg2 = get_arg_from_storage(cgen, right, rest_oprs)
    code1 += co

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        code2 = ''
        if reg2 is None:
            code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
        code = code1 + code2
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_args_reverse(cgen, code1, arg1, op, arg2, stack, reverse, rest_oprs,
                               reg1=reg1, reg2=reg2, right_op=right)


def handle_subscript_name(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_subscript_name(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_name_subscript(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_subscript_name(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def _handle_none_subscript(cgen, sub_op, op, stack, rest_oprs, next_opr, reverse):
    code2, reg2, typ2 = process_operand(cgen, sub_op, rest_oprs=rest_oprs, stack=stack)
    arg2 = cgen.arg_factory(typ2)
    reg1, typ1 = stack.pop()
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args_reverse(cgen, code2, arg1, op, arg2, stack, reverse, rest_oprs, reg1=reg1, reg2=reg2)


def handle_none_subscript(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_subscript(cgen, right, op, stack, rest_oprs, next_opr, False)


def handle_subscript_none(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_subscript(cgen, left, op, stack, rest_oprs, next_opr, True)


def _handle_callable_name(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)

    co, arg2, reg2 = get_arg_from_storage(cgen, right, rest_oprs)
    code1 += co

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        code2 = ''
        if reg2 is None:
            code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
        code = code1 + code2
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_args_reverse(cgen, code1, arg1, op, arg2, stack, reverse, rest_oprs,
                               reg1=reg1, reg2=reg2, right_op=right)


def handle_callable_name(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_name(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_name_callable(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_name(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def _handle_none_callable(cgen, call_op, op, stack, rest_oprs, next_opr, reverse):

    code2, reg2, typ2 = process_operand(cgen, call_op, rest_oprs=rest_oprs, stack=stack)
    arg2 = cgen.arg_factory(typ2)
    reg1, typ1 = stack.pop()
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args_reverse(cgen, code2, arg1, op, arg2, stack, reverse, rest_oprs, reg1=reg1, reg2=reg2)


def handle_none_callable(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_callable(cgen, right, op, stack, rest_oprs, next_opr, False)


def handle_callable_none(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_callable(cgen, left, op, stack, rest_oprs, next_opr, True)


def handle_callable_callable(cgen, left, right, op, stack, rest_oprs, next_opr):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)
    ad_arg_typs = [(reg1, typ1)]
    code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs, stack=stack, ad_arg_typs=ad_arg_typs)
    (reg1, typ1), = ad_arg_typs
    arg2 = cgen.arg_factory(typ2)
    code = code1 + code2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args(cgen, code, arg1, op, arg2, stack, rest_oprs, reg1=reg1, reg2=reg2)


def _handle_callable_const(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and arg1.fma_supported(cgen):
        code2, arg2, reg2 = load_const_of_type(cgen, right.value, arg1)
        code = code1 + code2
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_operand_const(cgen, code1, arg1, reg1, op, right, reverse, stack, rest_oprs)


def handle_callable_const(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_const(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_const_callable(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_const(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def handle_attr_attr(cgen, left, right, op, stack, rest_oprs, next_opr):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs)
    arg1 = cgen.arg_factory(typ1)
    code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
    arg2 = cgen.arg_factory(typ2)
    code = code1 + code2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args(cgen, code, arg1, op, arg2, stack, rest_oprs, reg1=reg1, reg2=reg2)


def _handle_callable_subscript(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)
    ad_arg_typs = [(reg1, typ1)]
    code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs, stack=stack, ad_arg_typs=ad_arg_typs)
    (reg1, typ1), = ad_arg_typs
    arg2 = cgen.arg_factory(typ2)
    code = code1 + code2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args_reverse(cgen, code, arg1, op, arg2, stack, reverse, rest_oprs, reg1=reg1, reg2=reg2)


def handle_callable_subscript(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_subscript(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_subscript_callable(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_subscript(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def _handle_attr_name(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs)
    arg1 = cgen.arg_factory(typ1)

    co, arg2, reg2 = get_arg_from_storage(cgen, right, rest_oprs)
    code1 += co

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        code2 = ''
        if reg2 is None:
            code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
        code = code1 + code2
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_args_reverse(cgen, code1, arg1, op, arg2, stack, reverse, rest_oprs,
                               reg1=reg1, reg2=reg2, right_op=right)


def handle_attr_name(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_attr_name(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_name_attr(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_attr_name(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def _handle_attr_const(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs)
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and arg1.fma_supported(cgen):
        code2, arg2, reg2 = load_const_of_type(cgen, right.value, arg1)
        code = code1 + code2
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)

    return handle_operand_const(cgen, code1, arg1, reg1, op, right, reverse, stack, rest_oprs)


def handle_attr_const(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_attr_const(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def handle_const_attr(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_attr_const(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def _handle_callable_attr(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)
    code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
    arg2 = cgen.arg_factory(typ2)
    code = code1 + code2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args_reverse(cgen, code, arg1, op, arg2, stack, reverse, rest_oprs, reg1=reg1, reg2=reg2)


def handle_attr_callable(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_attr(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def handle_callable_attr(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_callable_attr(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def _handle_none_attr(cgen, operand, op, stack, rest_oprs, next_opr, reverse):
    code2, reg2, typ2 = process_operand(cgen, operand, rest_oprs=rest_oprs)
    arg2 = cgen.arg_factory(typ2)
    reg1, typ1 = stack.pop()
    arg1 = cgen.arg_factory(typ1)

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code2, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args_reverse(cgen, code2, arg1, op, arg2, stack, reverse, rest_oprs, reg1=reg1, reg2=reg2)


def handle_attr_none(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_attr(cgen, left, op, stack, rest_oprs, next_opr, True)


def handle_none_attr(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_none_attr(cgen, right, op, stack, rest_oprs, next_opr, False)


def _handle_subscript_attr(cgen, left, right, op, stack, rest_oprs, next_opr, reverse):
    code1, reg1, typ1 = process_operand(cgen, left, rest_oprs=rest_oprs, stack=stack)
    arg1 = cgen.arg_factory(typ1)
    code2, reg2, typ2 = process_operand(cgen, right, rest_oprs=rest_oprs)
    arg2 = cgen.arg_factory(typ2)
    code = code1 + code2

    if next_opr and op == '*' and _can_fma(next_opr) and (arg1.fma_supported(cgen) and arg2.fma_supported(cgen)):
        return perform_fma_cmd(cgen, code, arg1, arg2, stack, rest_oprs, next_opr, reg1, reg2)
    return handle_args_reverse(cgen, code, arg1, op, arg2, stack, reverse, rest_oprs, reg1=reg1, reg2=reg2)


def handle_attr_subscript(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_subscript_attr(cgen, right, left, op, stack, rest_oprs, next_opr, True)


def handle_subscript_attr(cgen, left, right, op, stack, rest_oprs, next_opr):
    return _handle_subscript_attr(cgen, left, right, op, stack, rest_oprs, next_opr, False)


def process_operation(cgen, operation, stack=[], rest_oprs=[], next_opr=None):

    left, right, op = operation.left, operation.right, operation.operator

    key = (type(left), type(right))

    callbacks = {
        (Const, Const): handle_const_const,
        (Const, Name): handle_const_name,
        (Const, type(None)): handle_const_none,
        (Const, Subscript): handle_const_subscript,
        (Const, Callable): handle_const_callable,
        (Const, Attribute): handle_const_attr,
        (Name, Name): handle_name_name,
        (Name, Const): handle_name_const,
        (Name, type(None)): handle_name_none,
        (Name, Subscript): handle_name_subscript,
        (Name, Callable): handle_name_callable,
        (Name, Attribute): handle_name_attr,
        (type(None), Name): handle_none_name,
        (type(None), type(None)): handle_none_none,
        (type(None), Const): handle_none_const,
        (type(None), Subscript): handle_none_subscript,
        (type(None), Callable): handle_none_callable,
        (type(None), Attribute): handle_none_attr,
        (Subscript, Const): handle_subscript_const,
        (Subscript, Name): handle_subscript_name,
        (Subscript, Subscript): handle_subscript_subscript,
        (Subscript, type(None)): handle_subscript_none,
        (Subscript, Callable): handle_subscript_callable,
        (Subscript, Attribute): handle_subscript_attr,
        (Callable, Name): handle_callable_name,
        (Callable, type(None)): handle_callable_none,
        (Callable, Callable): handle_callable_callable,
        (Callable, Const): handle_callable_const,
        (Callable, Subscript): handle_callable_subscript,
        (Callable, Attribute): handle_callable_attr,
        (Attribute, Attribute): handle_attr_attr,
        (Attribute, Name): handle_attr_name,
        (Attribute, Const): handle_attr_const,
        (Attribute, Callable): handle_attr_callable,
        (Attribute, type(None)): handle_attr_none,
        (Attribute, Subscript): handle_attr_subscript,
    }

    if key not in callbacks:
        raise CompileError("Unsupported operation: Operation=%s, op1=%s, op2=%s" % (op, str(left), str(right)))

    return callbacks[key](cgen, left, right, op, stack, rest_oprs, next_opr)


def process_expression(cgen, expr, multiple=False):

    if isinstance(expr, Operations):
        stack = []
        code = ''
        oprs = expr.operations

        opr = oprs[0]
        index = 1

        while True:
            rest_oprs = oprs[index:] if index < len(oprs) else []
            next_opr = oprs[index] if index < len(oprs) else None
            index += 1
            (co, reg, arg_type), fma = process_operation(cgen, opr, stack, rest_oprs, next_opr)
            code += co

            if fma:
                opr = oprs[index] if index < len(oprs) else None
                index += 1
            else:
                opr = next_opr

            if opr is None:
                break
        return code, reg, arg_type
    else:
        return process_operand(cgen, expr)
