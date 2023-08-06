

from .holders import Const, Name, CompileError
from .expr import process_expression
from .flt_arg import Float32Arg
from .dbl_arg import Float64Arg


def gen_one_condition(cgen, con, jump_label, satisfied):
    left, op, right = con.left, con.operator, con.right

    code1, reg1, typ1 = process_expression(cgen, con.left)
    arg1 = cgen.arg_factory(typ1)

    if op is None:
        if arg1.can_cond_with_zero(cgen):
            code = arg1.cond_with_zero(cgen, reg1, jump_label, satisfied)
            cgen.release_reg(reg1)
            return code1 + code
        raise CompileError("Condition can't be generated.")
    else:
        if isinstance(right, Const) and arg1.can_cond_with_const(cgen, right.value, op):
            code = arg1.cond_with_const(cgen, reg1, right.value, op, jump_label, satisfied)
            cgen.release_reg(reg1)
            return code1 + code

        if isinstance(right, Name):
            arg2 = cgen.get_arg(right)
            if arg1.can_cond_with_mem(cgen, arg2, op):
                code = arg1.cond_with_mem(cgen, reg1, op, arg2, jump_label, satisfied)
                cgen.release_reg(reg1)
                return code1 + code

        code2, reg2, typ2 = process_expression(cgen, right)
        arg2 = cgen.arg_factory(typ2)

        if arg1.can_cond_with_arg(cgen, arg2, op):
            code = arg1.cond_with_arg(cgen, reg1, arg2, reg2, op, jump_label, satisfied)

            cgen.release_reg(reg1)
            cgen.release_reg(reg2)
            return code1 + code2 + code

        # TODO try implicit conversion arg1 to type(arg2) and than new_arg.can_cond_with_arg
        raise CompileError("Condition can't be generated.")


COUNTER = 0


def gen_lbl_name(prefix):
    global COUNTER
    COUNTER += 1
    return '%s_%i_%i' % (prefix, id(COUNTER), COUNTER)


def generate_test(cgen, conditions, end_label):

    start_label = gen_lbl_name('start_con')

    def short_circut_eval(start_label, conds):
        code = ''
        i = 0
        next_logic = conds.logic_ops[0]
        while i < len(conds.conditions):
            if next_logic == 'or':
                code += gen_one_condition(cgen, conds.conditions[i], start_label, True)
                i += 1
                if i == len(conds.conditions):
                    break
                if i >= len(conds.logic_ops):  # last condition
                    code += gen_one_condition(cgen, conds.conditions[-1], start_label, True)
                    break
                next_logic = conds.logic_ops[i]
            elif next_logic == 'and':
                middle_lbl = gen_lbl_name('middle_con')
                while True:
                    code += gen_one_condition(cgen, conds.conditions[i], middle_lbl, False)
                    i += 1
                    if i == len(conds.logic_ops):
                        code += gen_one_condition(cgen, conds.conditions[-1], middle_lbl, False)
                        i += 2
                        break
                    next_logic = conds.logic_ops[i]
                    if next_logic == 'or':
                        code += gen_one_condition(cgen, conds.conditions[i], middle_lbl, False)
                        i += 1
                        break
                code += 'jmp %s\n' % start_label
                code += '%s:\n' % middle_lbl
            else:
                raise ValueError("Unknown condition type", next_logic)

        code += 'jmp %s\n' % end_label
        return code

    if len(conditions.conditions) == 1:
        code = gen_one_condition(cgen, conditions.conditions[0], end_label, False)
    elif len(conditions.conditions) == 2:
        logic_op = conditions.logic_ops[0]
        if logic_op == 'or':
            code = gen_one_condition(cgen, conditions.conditions[0], start_label, True)
            code += gen_one_condition(cgen, conditions.conditions[1], start_label, True)
            code += 'jmp %s\n' % end_label
            code += '%s:\n' % start_label
        elif logic_op == 'and':
            code = gen_one_condition(cgen, conditions.conditions[0], end_label, False)
            code += gen_one_condition(cgen, conditions.conditions[1], end_label, False)
        else:
            raise ValueError("Only and/or logic supported for now.")
    elif len(conditions.conditions) == 3:
        logic_op1 = conditions.logic_ops[0]
        logic_op2 = conditions.logic_ops[1]
        if logic_op1 == logic_op2 == 'or':
            code = gen_one_condition(cgen, conditions.conditions[0], start_label, True)
            code += gen_one_condition(cgen, conditions.conditions[1], start_label, True)
            code += gen_one_condition(cgen, conditions.conditions[2], start_label, True)
            code += 'jmp %s\n' % end_label
            code += '%s:\n' % start_label
        elif logic_op1 == logic_op2 == 'and':
            code = gen_one_condition(cgen, conditions.conditions[0], end_label, False)
            code += gen_one_condition(cgen, conditions.conditions[1], end_label, False)
            code += gen_one_condition(cgen, conditions.conditions[2], end_label, False)
        else:
            code = short_circut_eval(start_label, conditions)
            code += '%s:\n' % start_label
    else:
        code = short_circut_eval(start_label, conditions)
        code += '%s:\n' % start_label

    return code
