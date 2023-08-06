

class Attribute:
    """Class represents attribute(field) in structure."""

    def __init__(self, name, path, unary_op=None):
        self.name = name  # name of struct
        self.path = path  # path to member in struct
        self.unary_op = unary_op

    def cache_key(self):
        return '%s_%s' % (self.name, self.path)


class Callable:
    """Class represents function in language."""

    def __init__(self, name, args, unary_op=None):
        self.name = name
        self.args = args
        self.unary_op = unary_op

    def cache_key(self):
        return None


class FuncArg:
    """Class represents function argument."""

    def __init__(self, name, type_name=None):
        self.name = name
        self.type_name = type_name


class Const:
    """
    Class represents constant(int, float, ...).

    Const can also hold tuple of values.
    """

    def __init__(self, value):
        self.value = value

    def cache_key(self):
        return None


class Name:
    """Class represents name(variable) in language."""

    def __init__(self, name, unary_op=None):
        self.name = name
        self.unary_op = unary_op

    def cache_key(self):
        return self.name


class Subscript:
    """Class represents item in array."""

    def __init__(self, path, index, unary_op=None):
        self.path = path  # Path can be Name or Attribute
        self.index = index
        self.unary_op = unary_op

    def cache_key(self):
        return None


class Operation:
    """Class that represent simple arithmetic operation."""

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Operations:
    """Class that holds list of arithmetic operations."""

    def __init__(self, operations):
        self.operations = operations


class Condition:
    """Class that one simple logic condition."""

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class Conditions:
    """Class that holds list of logic conditions."""

    def __init__(self, conditions, logic_ops):
        assert len(conditions) == len(logic_ops) + 1
        self.conditions = conditions
        self.logic_ops = logic_ops


class CompileError(Exception):
    def __init__(self, message, lineno=None):
        self.message = message
        self.lineno = lineno
        self.source = None

    def __str__(self):
        err_line = ''
        if self.lineno:
            if self.source:
                err_line = 'Error on Line %i: %s\n' % (self.lineno, self.source.splitlines()[self.lineno - 1])
            else:
                err_line = "Error on line %i:\n" % self.lineno
        msg = "%s\n%s" % (self.message, err_line)
        return msg
