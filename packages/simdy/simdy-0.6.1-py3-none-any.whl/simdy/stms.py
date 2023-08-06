
from abc import ABCMeta, abstractmethod
from .holders import Operations, Operation, Const, Name, Subscript, Attribute,\
    Callable, Condition, Conditions, CompileError
from .expr import process_expression, convert_to_fn_arg
from .int_arg import Int32Arg, Int64Arg
from .test import generate_test, gen_one_condition
from .acum import move_regs_to_acums


class Statement(metaclass=ABCMeta):
    """Abstract base class that define interface for statements."""

    def __init__(self, lineno=None):
        self.lineno = lineno

    @abstractmethod
    def asm_code(self, cgen):
        """
        Generate assembly code for this statement.

        @param cgen - code generator
        """
        pass

    def is_return(self):
        return False

    def is_function(self):
        return False

    def is_assign(self):
        return False

    def is_aug_assign(self):
        return False

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        pass


def store_name_arg(cgen, dest, arg_type, src_reg):
    arg = cgen.create_arg(dest, arg_type)
    code = arg.store_cmd(cgen, src_reg)
    return code


def store_subscript_arg(cgen, dest, arg_type, src_reg):
    arg = cgen.get_arg(dest.path)
    ptr_reg = None
    if arg is None:
        raise ValueError("Operand %s doesn't exist" % dest.path.name)

    index, reg, code = None, None, ''
    if isinstance(dest.index, Const) and isinstance(dest.index.value, int):
        index = dest.index.value
    else:
        code, reg, idx_type = process_expression(cgen, dest.index)
        if idx_type is not Int32Arg and idx_type is not Int64Arg:
            raise CompileError("Subscript index must be integer.")

    if isinstance(dest.path, Attribute):
        code2 = arg.store_attr_item_cmd(cgen, arg_type, src_reg, dest.path.path, index=index, reg=reg, ptr_reg=ptr_reg)
    else:
        code2 = arg.store_item_cmd(cgen, arg_type, src_reg, index=index, reg=reg, ptr_reg=ptr_reg)
    return code + code2


def store_attribute_arg(cgen, dest, arg_type, src_reg):
    arg = cgen.get_arg(dest)
    if arg is None:
        raise CompileError("Missing %s argument" % dest.name)
    return arg.store_attr_cmd(cgen, dest.path, arg_type, src_reg)


def store_result(cgen, dest, arg_type, src_reg):
    if isinstance(dest, Name):
        return store_name_arg(cgen, dest, arg_type, src_reg)
    elif isinstance(dest, Subscript):
        return store_subscript_arg(cgen, dest, arg_type, src_reg)
    elif isinstance(dest, Attribute):
        return store_attribute_arg(cgen, dest, arg_type, src_reg)
    else:
        raise ValueError("Unsupported destination type! ", dest)


def analyze_vars(expr, index, local_vars):
    if isinstance(expr, Name):
        local_vars[expr.name].append(index)
    elif isinstance(expr, Attribute):
        local_vars[expr.name].append(index)
    elif isinstance(expr, Subscript):
        analyze_vars(expr.path, index, local_vars)
        analyze_vars(expr.index, index, local_vars)
    elif isinstance(expr, Operations):
        for opr in expr.operations:
            analyze_vars(opr, index, local_vars)
    elif isinstance(expr, Operation):
        analyze_vars(expr.left, index, local_vars)
        analyze_vars(expr.right, index, local_vars)
    elif isinstance(expr, Callable):
        for arg in expr.args:
            analyze_vars(arg, index, local_vars)
    elif isinstance(expr, Conditions):
        for cond in expr.conditions:
            analyze_vars(cond, index, local_vars)
    elif isinstance(expr, Condition):
        analyze_vars(expr.left, index, local_vars)
        analyze_vars(expr.right, index, local_vars)


class StmAssign(Statement):
    def __init__(self, dest, expr, lineno=None):
        super(StmAssign, self).__init__(lineno=lineno)
        self.dest = dest
        self.expr = expr

    def asm_code(self, cgen):

        # TODO -- create instance of user defined type
        # if isinstance(self.expr, Callable) and cgen.is_user_type(self.expr):
        #     cgen.create_arg(self.dest, self.expr)
        #     return ''

        code, reg, arg_type = process_expression(cgen, self.expr)
        code2 = store_result(cgen, self.dest, arg_type, reg)
        return code + code2

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        analyze_vars(self.expr, index, read_vars)
        analyze_vars(self.dest, index, store_vars)
        if isinstance(self.dest, Subscript):
            analyze_vars(self.dest.index, index, read_vars)

    def is_assign(self):
        return True


class StmExpression(Statement):
    def __init__(self, expr, lineno=None):
        super(StmExpression, self).__init__(lineno=lineno)
        self.expr = expr

    def asm_code(self, cgen):
        code, reg, arg_type = process_expression(cgen, self.expr)
        return code

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        analyze_vars(self.expr, index, read_vars)


class MultStmAssign(Statement):
    def __init__(self, dests, exprs, lineno=None):
        super(MultStmAssign, self).__init__(lineno=lineno)
        self.dests = dests
        self.exprs = exprs

    def asm_code(self, cgen):
        all_code = ''
        sources = []
        if isinstance(self.exprs, tuple):
            for expr in self.exprs:
                code, reg, arg_type = process_expression(cgen, expr)
                all_code += code
                sources.append((reg, arg_type))
        else:
            code, reg, arg_type = process_expression(cgen, self.exprs, multiple=True)
            all_code += code
            if isinstance(arg_type, tuple):
                sources = [(r, a) for r, a in zip(reg, arg_type)]
            else:
                sources = [(reg, arg_type)]

        if len(self.dests) != len(sources):
            raise ValueError("Multiple assign failed. ", len(self.dests), len(sources))

        for dest, (reg, arg_type) in zip(self.dests, sources):
            all_code += store_result(cgen, dest, arg_type, reg)

        return all_code

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        if isinstance(self.exprs, tuple):
            for expr in self.exprs:
                analyze_vars(expr, index, read_vars)
        else:
            analyze_vars(self.exprs, index, read_vars)

        if isinstance(self.dests, tuple):
            for dest in self.dests:
                analyze_vars(dest, index, store_vars)
                if isinstance(dest, Subscript):
                    analyze_vars(dest.index, index, read_vars)
        else:
            analyze_vars(self.dests, index, store_vars)
            if isinstance(self.dests, Subscript):
                analyze_vars(self.dests.index, index, read_vars)


class StmAugAssign(Statement):
    def __init__(self, dest, expr, op, lineno=None):
        super(StmAugAssign, self).__init__(lineno=lineno)
        self.dest = dest
        self.expr = expr
        self.op = op

    def asm_code(self, cgen):

        if isinstance(self.expr, Operations):
            expr = self.expr.operations + [Operation(self.dest, self.op, None)]
            expr = Operations(expr)
        else:
            operation = Operation(self.dest, self.op, self.expr)
            expr = Operations([operation])

        code, reg, arg_type = process_expression(cgen, expr)
        code2 = store_result(cgen, self.dest, arg_type, reg)
        return code + code2

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        if isinstance(self.expr, Operations):
            expr = self.expr.operations + [Operation(self.dest, self.op, None)]
            expr = Operations(expr)
        else:
            operation = Operation(self.dest, self.op, self.expr)
            expr = Operations([operation])

        analyze_vars(expr, index, read_vars)
        analyze_vars(self.dest, index, store_vars)
        if isinstance(self.dest, Subscript):
            analyze_vars(self.dest.index, index, read_vars)

    def is_aug_assign(self):
        return True


# NOTE orelse contains else body or another StmIf object

class StmIf(Statement):
    def __init__(self, conditions, body, orelse=None, lineno=None):
        super(StmIf, self).__init__(lineno=lineno)
        self.conditions = conditions
        self.body = body
        self.orelse = orelse
        self._count = 0

    def asm_code(self, cgen):
        self._count += 1

        orelse_label = 'orelse_%i_%i' % (id(self), self._count)
        endif_label = 'endif_%i_%i' % (id(self), self._count)

        if self.orelse is None:
            code = generate_test(cgen, self.conditions, endif_label)
        else:
            code = generate_test(cgen, self.conditions, orelse_label)
        code += ''.join(cgen.stm_code(stm) for stm in self.body)
        if self.orelse is not None:
            code += "jmp %s\n" % endif_label
            code += "%s:\n" % orelse_label
            if isinstance(self.orelse, StmIf):
                code += cgen.stm_code(self.orelse)
            else:
                code += ''.join(cgen.stm_code(stm) for stm in self.orelse)
            code += "%s:\n" % endif_label
        else:
            code += "%s:\n" % endif_label

        return code

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        analyze_vars(self.conditions, index, read_vars)
        cgen._analyze_stms(self.body)
        if self.orelse is not None:
            if isinstance(self.orelse, StmIf):
                self.orelse.analyze_vars(cgen, index, read_vars, store_vars)
            else:
                cgen._analyze_stms(self.orelse)


class StmWhile(Statement):
    def __init__(self, body, conditions, lineno=None):
        super(StmWhile, self).__init__(lineno=lineno)
        self.body = body
        self.conditions = conditions
        self._count = 0

    def asm_code(self, cgen):
        self._count += 1
        self._begin_label = begin_label = 'while_%i_%i' % (id(self), self._count)
        self._end_label = end_label = 'endwhile_%i_%i' % (id(self), self._count)

        code = "%s:\n" % begin_label
        code += generate_test(cgen, self.conditions, end_label)
        code += ''.join(cgen.stm_code(stm) for stm in self.body)
        code += "jmp %s\n" % begin_label
        code += "%s:\n" % end_label
        return code

        # code = generate_test(cgen, self.conditions, end_label)
        # code += "%s:\n" % begin_label
        # code += ''.join(cgen.stm_code(stm) for stm in self.body)
        # code += gen_one_condition(cgen, self.conditions.conditions[0], begin_label, True)
        # code += "%s:\n" % end_label
        # return code

    def break_label(self):
        return self._end_label

    def start_label(self):
        return self._begin_label

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        analyze_vars(self.conditions, index, read_vars)
        cgen._analyze_stms(self.body)


class StmBreak(Statement):
    def __init__(self, loop_stm, lineno=None):
        super(StmBreak, self).__init__(lineno=lineno)
        self.loop_stm = loop_stm

    def asm_code(self, cgen):
        return "jmp %s\n" % self.loop_stm.break_label()


class StmContinue(Statement):
    def __init__(self, loop_stm, lineno=None):
        super(StmContinue, self).__init__(lineno=lineno)
        self.loop_stm = loop_stm

    def asm_code(self, cgen):
        return "jmp %s\n" % self.loop_stm.start_label()


class StmPass(Statement):
    def asm_code(self, cgen, lineno=None):
        return ''


class StmFunction(Statement):
    def __init__(self, name, args, body, ret_type_names=[], lineno=None):
        super(StmFunction, self).__init__(lineno=lineno)
        self.name = name
        self.args = tuple(args)
        self.body = body
        self.ret_type_names = tuple(ret_type_names)

    def asm_code(self, cgen):
        cgen.register_local_func(self)
        return ''

    def is_function(self):
        return True


class StmReturn(Statement):
    def __init__(self, exprs, lineno=None):
        super(StmReturn, self).__init__(lineno=lineno)
        self.exprs = exprs
        self.last_stm = False

    def asm_code(self, cgen):
        code = ''
        if len(self.exprs) == 1:
            # just if it is only oprand multiple can be true
            code, reg, arg_type = process_expression(cgen, self.exprs[0], multiple=True)
            if isinstance(arg_type, tuple):
                regs, ret_types = list(reg), list(arg_type)
            else:
                regs, ret_types = [reg], [arg_type]
        else:
            regs, ret_types = [], []
            for expr in self.exprs:
                co, reg, arg_type = process_expression(cgen, expr)
                code += co
                regs.append(reg)
                ret_types.append(arg_type)

        for i in range(len(ret_types)):
            co, new_reg = convert_to_fn_arg(ret_types[i], cgen, regs[i])
            code += co
            regs[i] = new_reg

        regs, ret_types = tuple(regs), tuple(ret_types)
        code += move_regs_to_acums(cgen, regs)
        cgen.register_ret_type(ret_types)
        if not self.last_stm:
            code += 'jmp %s\n' % cgen.return_label()
        return code

    def is_return(self):
        return True

    def analyze_vars(self, cgen, index, read_vars, store_vars):
        if len(self.exprs) == 1:
            analyze_vars(self.exprs, index, read_vars)
        else:
            for expr in self.exprs:
                analyze_vars(expr, index, read_vars)


class StmExternal(Statement):
    def __init__(self, name, type_name, lineno=None):
        super(StmExternal, self).__init__(lineno=lineno)
        self.name = Name(name)
        self.type_name = type_name

    def asm_code(self, cgen):
        if not cgen.is_user_arg(self.name):
            raise ValueError("External parameter %s doesn't exist." % self.name.name)

        arg = cgen.get_arg(self.name)
        if arg.type_name() != self.type_name:
            raise ValueError("Parameter %s exist, type mismatch %s != %s " % (self.name.name, self.type_name, arg.type_name()))
        return ''


class StmFor(Statement):
    def __init__(self, target, end, start=None, step=None, lineno=None):
        super(StmFor, self).__init__(lineno=lineno)
        self.target = target
        self.start = start
        self.end = end
        self.step = step
        self._count = 0
        self.body = []

    def asm_code(self, cgen):
        self._count += 1
        self._begin_label = begin_label = 'for_%i_%i' % (id(self), self._count)
        self._continue_label = continue_label = 'continue_for_%i_%i' % (id(self), self._count)
        self._end_label = end_label = 'endfor_%i_%i' % (id(self), self._count)
        end_name = Name('end_name_%i_%i' % (id(self), self._count))
        step_name = Name('step_name_%i_%i' % (id(self), self._count))

        if self.start is None:
            code1, reg, arg_type = process_expression(cgen, self.end.expr)
            code2 = store_result(cgen, end_name, arg_type, reg)
            code = code1 + code2
            if arg_type not in (Int32Arg, Int64Arg):
                raise CompileError("Counter in for loop must be of type int32 or int64.", lineno=self.lineno)
            code += 'xor %s, %s\n' % (reg, reg)
            code += store_result(cgen, self.target, arg_type, reg)
            cgen.release_reg(reg)
        else:
            code1, reg1, arg_type1 = process_expression(cgen, self.start.expr)
            code1 += store_result(cgen, self.target, arg_type1, reg1)
            cgen.release_reg(reg1)
            code2, reg2, arg_type2 = process_expression(cgen, self.end.expr)
            code2 += store_result(cgen, end_name, arg_type2, reg2)
            cgen.release_reg(reg2)
            code = code1 + code2
            if arg_type1 not in (Int32Arg, Int64Arg):
                raise CompileError("Counter in for loop must be of type int32 or int64.", lineno=self.lineno)
            if arg_type2 not in (Int32Arg, Int64Arg):
                raise CompileError("Counter in for loop must be of type int32 or int64.", lineno=self.lineno)
            if arg_type1 is not arg_type2:
                raise CompileError("Mismatch types, start and end in for must be of same type.", lineno=self.lineno)

        if self.step is not None:
            co, reg, arg_type = process_expression(cgen, self.step.expr)
            code += co
            code += store_result(cgen, step_name, arg_type, reg)
            cgen.release_reg(reg)
            if arg_type not in (Int32Arg, Int64Arg):
                raise CompileError("Step in for loop must be of type int32 or int64.", lineno=self.lineno)

        code += "%s:\n" % begin_label
        arg = cgen.get_arg(end_name)
        counter_arg = cgen.get_arg(self.target)
        if isinstance(arg, Int32Arg):
            reg = cgen.register('general')
            code += 'mov %s, dword[%s]\n' % (reg, counter_arg.name)
            code += 'cmp %s, dword[%s]\n' % (reg, arg.name)
            cgen.release_reg(reg)
        else:
            reg = cgen.register('general64')
            code += 'mov %s, qword[%s]\n' % (reg, counter_arg.name)
            code += 'cmp %s, qword[%s]\n' % (reg, arg.name)
            cgen.release_reg(reg)

        code += "jge %s\n" % end_label
        code += ''.join(cgen.stm_code(stm) for stm in self.body)
        code += "%s:\n" % continue_label
        if self.step is not None:
            step_arg = cgen.get_arg(step_name)
            if type(step_arg) is not type(counter_arg):
                raise CompileError("Mismatch types, start and step in for must be of same type.", lineno=self.lineno)
            if isinstance(step_arg, Int32Arg):
                reg = cgen.register('general')
                code += 'mov %s, dword[%s]\n' % (reg, step_arg.name)
                code += 'add dword[%s], %s\n' % (counter_arg.name, reg)
                cgen.release_reg(reg)
            else:
                reg = cgen.register('general64')
                code += 'mov %s, qword[%s]\n' % (reg, step_arg.name)
                code += 'add qword[%s], %s\n' % (counter_arg.name, reg)
                cgen.release_reg(reg)
        else:
            if isinstance(counter_arg, Int32Arg):
                code += 'add dword[%s], 1\n' % counter_arg.name
            else:
                code += 'add qword[%s], 1\n' % counter_arg.name
        code += "jmp %s\n" % begin_label
        code += "%s:\n" % end_label

        return code

    def break_label(self):
        return self._end_label

    def start_label(self):
        return self._continue_label
