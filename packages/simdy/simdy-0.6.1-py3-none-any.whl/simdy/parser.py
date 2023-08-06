
import ast
from .holders import Name, Attribute, Subscript, Const, Callable,\
    Operation, Operations, Condition, Conditions, FuncArg
from .stms import StmAssign, StmAugAssign, MultStmAssign, StmIf, StmWhile,\
    StmBreak, StmContinue, StmPass, StmFunction, StmReturn, StmExpression, StmExternal, StmFor


def extract_operator(obj):
    o = {ast.Add: '+', ast.Mult: '*', ast.Sub: '-', ast.Div: '/',
         ast.Mod: '%', ast.LShift: '<<', ast.RShift: '>>', ast.BitAnd: '&',
         ast.BitOr: '|', ast.BitXor: '^'}
    return o[type(obj)]


def extract_path(obj, unary_op=None):

    comps = []
    while isinstance(obj, ast.Attribute):
        comps.insert(0, obj.attr)
        obj = obj.value
    path = ".".join(comps)
    if isinstance(obj, ast.Name):
        name = obj.id
    else:
        raise ValueError("Unknown target name, maybe subscript!", obj)

    return Attribute(name, path, unary_op=unary_op)


def extract_subscript(obj, unary_op=None):
    if isinstance(obj.value, ast.Name):
        name = Name(obj.value.id)
    elif isinstance(obj.value, ast.Attribute):
        name = extract_path(obj.value)
    else:
        raise ValueError("Unknown subscript type", obj.value)

    if isinstance(obj.slice.value, ast.BinOp):
        index = Operations(parse_arithmetic_expr(obj.slice.value, []))
    else:
        index = extract_operand(obj.slice.value)
    return Subscript(name, index, unary_op=unary_op)


def make_name(obj):
    if isinstance(obj, ast.Attribute):
        return extract_path(obj)
    elif isinstance(obj, ast.Name):
        return Name(obj.id)
    elif isinstance(obj, ast.Subscript):
        return extract_subscript(obj)
    else:
        raise ValueError("Unsuported source", obj)


def extract_unary(obj):
    o = {ast.USub: '-', ast.UAdd: '+', ast.Invert: '~'}
    return o[type(obj)]


def unary_number(obj):
    if not isinstance(obj.operand, ast.Num):
        raise ValueError("Constant unary number expected!", obj.operand)

    if isinstance(obj.operand.n, int):
        return Const(int(extract_unary(obj.op) + str(obj.operand.n)))
    elif isinstance(obj.operand.n, float):
        return Const(float(extract_unary(obj.op) + str(obj.operand.n)))
    else:
        raise ValueError('Unsuported unary constant', obj.operand.n)


def extract_numbers(obj):
    numbers = []
    for n in obj.elts:
        if isinstance(n, ast.Num):
            numbers.append(n.n)
        elif isinstance(n, ast.UnaryOp):
            if isinstance(n.operand, ast.Num):
                if isinstance(n.operand.n, int):
                    numbers.append(int(extract_unary(n.op) + str(n.operand.n)))
                elif isinstance(n.operand.n, float):
                    numbers.append(float(extract_unary(n.op) + str(n.operand.n)))
                else:
                    raise ValueError("Unknown constant", n.operand.n)
            else:
                raise ValueError("Wrong operand in Unaray operator", n.operand)
        else:
            raise ValueError("Its not a constant", n)
    return tuple(numbers)


def extract_operand(obj, unary_op=None):
    if isinstance(obj, ast.UnaryOp):
        if isinstance(obj.operand, ast.Num):
            return unary_number(obj)
        else:
            return extract_operand(obj.operand, unary_op=extract_unary(obj.op))
    if isinstance(obj, ast.Num):
        return Const(obj.n)
    elif isinstance(obj, ast.Name):
        return Name(obj.id, unary_op=unary_op)
    elif isinstance(obj, (ast.Tuple, ast.List)):
        return Const(extract_numbers(obj))
    elif isinstance(obj, ast.Attribute):
        return extract_path(obj, unary_op=unary_op)
    elif isinstance(obj, ast.Subscript):
        return extract_subscript(obj, unary_op=unary_op)
    elif isinstance(obj, ast.Call):
        func = obj.func.id
        args = []
        for arg in obj.args:
            if isinstance(arg, ast.BinOp):
                expr = Operations(parse_arithmetic_expr(arg, []))
            elif isinstance(arg, ast.Compare):
                expr = Operations(extract_expr_compare(arg, []))
            else:
                expr = extract_operand(arg)
            args.append(expr)
        return Callable(func, args, unary_op=unary_op)
    elif isinstance(obj, ast.NameConstant):
        return Const(obj.value)
    else:
        raise ValueError("Unsuported operand in binary arithmetic.", obj)


def parse_arithmetic_expr(bin_op, operations):

    left = bin_op.left
    right = bin_op.right
    op = bin_op.op
    if not isinstance(left, (ast.Compare, ast.BinOp)) and not isinstance(right, (ast.Compare, ast.BinOp)):
        op1 = extract_operand(bin_op.left)
        op2 = extract_operand(bin_op.right)
        o = extract_operator(bin_op.op)
        operations.append(Operation(left=op1, operator=o, right=op2))
        return operations

    if isinstance(left, (ast.Compare, ast.BinOp)):
        if isinstance(left, ast.BinOp):
            parse_arithmetic_expr(left, operations)
        else:
            extract_expr_compare(left, operations)
        if isinstance(right, (ast.Compare, ast.BinOp)):
            if isinstance(right, ast.BinOp):
                parse_arithmetic_expr(right, operations)
            else:
                extract_expr_compare(right, operations)
            operations.append(Operation(None, extract_operator(op), None))
        else:
            op2 = extract_operand(right)
            operations.append(Operation(None, extract_operator(op), op2))
        return operations

    if isinstance(right, (ast.Compare, ast.BinOp)):
        if isinstance(right, ast.BinOp):
            parse_arithmetic_expr(right, operations)
        else:
            extract_expr_compare(right, operations)
        if isinstance(left, (ast.Compare, ast.BinOp)):
            if isinstance(left, ast.BinOp):
                parse_arithmetic_expr(left, operations)
            else:
                extract_expr_compare(left, operations)
            operations.append(Operation(None, extract_operator(op), None))
        else:
            op2 = extract_operand(left)
            operations.append(Operation(op2, extract_operator(op), None))
        return operations

    raise ValueError("Unsuported expression", left, right, op)


def extract_expr_compare(obj, operations):
    if len(obj.comparators) != 1:
        raise ValueError("Multiple comparators!!!", obj.comparators)

    if len(obj.ops) != 1:
        raise ValueError("Multiple conditions!", obj.ops)
    con_op = extract_con_op(obj.ops[0])

    if isinstance(obj.left, ast.BinOp) and isinstance(obj.comparators[0], ast.BinOp):
        operations = parse_arithmetic_expr(obj.left, operations)
        operations = parse_arithmetic_expr(obj.comparators[0], operations)
        last_op = Operation(left=None, operator=con_op, right=None)
        operations.append(last_op)
        return operations
    elif isinstance(obj.left, ast.BinOp):
        operations = parse_arithmetic_expr(obj.left, operations)
        right_op = extract_operand(obj.comparators[0])
        last_op = Operation(left=None, operator=con_op, right=right_op)
        operations.append(last_op)
        return operations
    elif isinstance(obj.comparators[0], ast.BinOp):
        operations = parse_arithmetic_expr(obj.comparators[0], operations)
        left_op = extract_operand(obj.left)
        last_op = Operation(left=left_op, operator=con_op, right=None)
        operations.append(last_op)
        return operations
    else:
        left_op = extract_operand(obj.left)
        right_op = extract_operand(obj.comparators[0])
        last_op = Operation(left=left_op, operator=con_op, right=right_op)
        operations.append(last_op)
        return operations


def parse_assign(statement, loop_stm=None):

    if len(statement.targets) > 1:
        raise ValueError("Multiple targets not supported.", statement.targets)
    target = statement.targets[0]

    if isinstance(statement.value, ast.BinOp):
        expr = Operations(parse_arithmetic_expr(statement.value, []))
    elif isinstance(statement.value, ast.Tuple) and isinstance(target, ast.Tuple):
        expr = []
        for elt in statement.value.elts:
            if isinstance(elt, ast.BinOp):
                expr.append(Operations(parse_arithmetic_expr(elt, [])))
            else:
                expr.append(extract_operand(elt))
        expr = tuple(expr)
    elif isinstance(statement.value, ast.Compare):
        expr = Operations(extract_expr_compare(statement.value, []))
    else:
        expr = extract_operand(statement.value)

    if isinstance(target, ast.Tuple):
        target_names = [make_name(elt) for elt in target.elts]
        return MultStmAssign(tuple(target_names), expr, lineno=statement.lineno)
    else:
        if isinstance(expr, Callable) and expr.name == 'external':
            return StmExternal(make_name(target).name, expr.args[0].name, lineno=statement.lineno)

        return StmAssign(make_name(target), expr, lineno=statement.lineno)


def parse_aug_assign(statement, loop_stm=None):

    if isinstance(statement.value, ast.BinOp):
        expr = Operations(parse_arithmetic_expr(statement.value, []))
    else:
        expr = extract_operand(statement.value)
    op = extract_operator(statement.op)
    return StmAugAssign(make_name(statement.target), expr, op, lineno=statement.lineno)


def parse_pass(statement, loop_stm=None):
    return StmPass(lineno=statement.lineno)


def _parse_expression(value, loop_stm=None, lineno=None):
    if isinstance(value, ast.BinOp):
        expr = Operations(parse_arithmetic_expr(value, []))
    elif isinstance(value, ast.Tuple):
        expr = []
        for elt in value.elts:
            if isinstance(elt, ast.BinOp):
                expr.append(Operations(parse_arithmetic_expr(elt, [])))
            else:
                expr.append(extract_operand(elt))
        expr = tuple(expr)
    elif isinstance(value, ast.Compare):
        expr = Operations(extract_expr_compare(value, []))
    else:
        expr = extract_operand(value)
    return StmExpression(expr, lineno=lineno)


def parse_expression(statement, loop_stm=None):
    return _parse_expression(statement.value, loop_stm=loop_stm, lineno=statement.lineno)


def extract_con_op(obj):
    o = {ast.Lt: '<', ast.Gt: '>', ast.Eq: '==', ast.LtE: '<=',
         ast.GtE: '>=', ast.NotEq: '!='}
    return o[type(obj)]


def extract_compare(obj):
    if len(obj.comparators) != 1:
        raise ValueError("Multiple comparators!!!", obj.comparators)

    if isinstance(obj.left, ast.BinOp):
        left_op = Operations(parse_arithmetic_expr(obj.left, []))
    else:
        left_op = extract_operand(obj.left)

    if isinstance(obj.comparators[0], ast.BinOp):
        right_op = Operations(parse_arithmetic_expr(obj.comparators[0], []))
    else:
        right_op = extract_operand(obj.comparators[0])

    if len(obj.ops) != 1:
        raise ValueError("Multiple conditions!", obj.ops)

    con_op = extract_con_op(obj.ops[0])
    con = Condition(left_op, con_op, right_op)
    return con


def extract_condition(obj):
    if isinstance(obj, ast.Compare):
        condition = extract_compare(obj)
    elif isinstance(obj, ast.BinOp):
        left = Operations(parse_arithmetic_expr(obj, []))
        condition = Condition(left, None, None)
    else:
        left = extract_operand(obj)
        condition = Condition(left, None, None)
    return condition


def extract_logic_op(obj):
    o = {ast.And: 'and', ast.Or: 'or'}
    return o[type(obj)]


def extract_bool_op(obj, conditions, logic_ops):
    for val in obj.values:
        if isinstance(val, ast.BoolOp):
            if len(conditions) != len(logic_ops):
                logic_ops.append(extract_logic_op(obj.op))
            extract_bool_op(val, conditions, logic_ops)
        else:
            if len(conditions) > len(logic_ops):
                log_op = extract_logic_op(obj.op)
                logic_ops.append(log_op)
            con1 = extract_condition(val)
            conditions.append(con1)
    return conditions, logic_ops


def extract_conditions(obj):
    if isinstance(obj, ast.BoolOp):
        conds, logic_ops = extract_bool_op(obj, [], [])
        conditions = Conditions(conds, logic_ops)
    else:
        condition = extract_condition(obj)
        conditions = Conditions([condition], [])
    return conditions


def parse_while(statement, loop_stm=None):
    if statement.orelse:
        raise ValueError("Orelse in while still not suported")

    conditions = extract_conditions(statement.test)
    loop_stm = StmWhile([], conditions, lineno=statement.lineno)
    body = [parse_statement(stm, loop_stm=loop_stm) for stm in statement.body]
    loop_stm.body = body
    return loop_stm


def parse_if(statement, loop_stm=None):

    body = [parse_statement(stm, loop_stm=loop_stm) for stm in statement.body]
    conditions = extract_conditions(statement.test)

    orelse = None
    if len(statement.orelse) == 1 and isinstance(statement.orelse[0], ast.If):
        orelse = parse_if(statement.orelse[0], loop_stm=loop_stm)
    elif len(statement.orelse) > 0:
        orelse = [parse_statement(stm, loop_stm=loop_stm) for stm in statement.orelse]

    return StmIf(conditions, body, orelse=orelse, lineno=statement.lineno)


def parse_return(statement, loop_stm=None):
    if isinstance(statement.value, ast.BinOp):
        exprs = [Operations(parse_arithmetic_expr(statement.value, []))]
    elif isinstance(statement.value, ast.Tuple):
        exprs = []
        for elt in statement.value.elts:
            if isinstance(elt, ast.BinOp):
                exprs.append(Operations(parse_arithmetic_expr(elt, [])))
            else:
                exprs.append(extract_operand(elt))
    else:
        exprs = [extract_operand(statement.value)]
    return StmReturn(exprs, lineno=statement.lineno)


def parse_break(statement, loop_stm=None):
    return StmBreak(loop_stm, lineno=statement.lineno)


def parse_continue(statement, loop_stm=None):
    return StmContinue(loop_stm, lineno=statement.lineno)


def parse_function(statement, loop_stm=None):

    name = statement.name
    args = []
    for arg in statement.args.args:
        arg_name = arg.arg
        arg_type = None
        if arg.annotation is not None:
            if not isinstance(arg.annotation, ast.Name):
                raise ValueError("Unsupported annotation. ", arg.annotation)
            arg_type = arg.annotation.id
        args.append(FuncArg(arg_name, arg_type))
    body = [parse_statement(stm, loop_stm=loop_stm) for stm in statement.body]
    ret_type_names = []
    if statement.returns is not None:
        if isinstance(statement.returns, ast.Name):
            ret_type_names.append(statement.returns.id)
        elif isinstance(statement.returns, ast.Tuple):
            for elt in statement.returns.elts:
                if not isinstance(elt, ast.Name):
                    raise ValueError("Incorrect return type.", elt)
                ret_type_names.append(elt.id)
        else:
            raise ValueError("Incorrect return type.", statement.returns)
    return StmFunction(name, args, body, ret_type_names, lineno=statement.lineno)


# NOTE - for now imports are just ignored
def parse_import(statement, loop_stm=None):
    return StmPass(lineno=statement.lineno)


def parse_import_from(statement, loop_stm=None):
    module = statement.module
    __import__(module)
    return StmPass(lineno=statement.lineno)


def parse_for(statement, loop_stm=None):
    if not isinstance(statement.target, ast.Name):
        raise ValueError("In For loop target must be Name", statement.target)
    target = make_name(statement.target)
    if not isinstance(statement.iter, ast.Call):
        raise ValueError("In For loop iter must be range callable.", statement.iter)
    if statement.iter.func.id != 'range':
        raise ValueError("In For loop iter must be range callable.", statement.iter.func.id)

    start = end = step = None
    if len(statement.iter.args) == 1:
        end = _parse_expression(statement.iter.args[0], loop_stm=loop_stm, lineno=statement.lineno)
    elif len(statement.iter.args) == 2:
        start = _parse_expression(statement.iter.args[0], loop_stm=loop_stm, lineno=statement.lineno)
        end = _parse_expression(statement.iter.args[1], loop_stm=loop_stm, lineno=statement.lineno)
    else:
        start = _parse_expression(statement.iter.args[0], loop_stm=loop_stm, lineno=statement.lineno)
        end = _parse_expression(statement.iter.args[1], loop_stm=loop_stm, lineno=statement.lineno)
        step = _parse_expression(statement.iter.args[2], loop_stm=loop_stm, lineno=statement.lineno)

    loop_stm = StmFor(target, end, start=start, step=step, lineno=statement.lineno)
    body = [parse_statement(stm, loop_stm=loop_stm) for stm in statement.body]
    loop_stm.body = body
    return loop_stm


def parse_statement(statement, loop_stm=None):

    stm_callbacks = {
        ast.Assign: parse_assign,
        ast.AugAssign: parse_aug_assign,
        ast.While: parse_while,
        ast.Pass: parse_pass,
        ast.Expr: parse_expression,
        ast.If: parse_if,
        ast.Return: parse_return,
        ast.Break: parse_break,
        ast.Continue: parse_continue,
        ast.FunctionDef: parse_function,
        ast.Import: parse_import,
        ast.ImportFrom: parse_import_from,
        ast.For: parse_for,
    }

    if type(statement) not in stm_callbacks:
        raise ValueError("Statement not supported!", statement)

    return stm_callbacks[type(statement)](statement, loop_stm=loop_stm)


def parse(source):

    code = ast.parse(source)

    if not isinstance(code, ast.Module):
        raise ValueError('Source is not instance of ast.Module', code)

    stms = [parse_statement(stm) for stm in code.body]
    return stms
