
from tdasm import translate
from .args import ComplexArgument


_user_types = {}


def register_user_type(user_type, factory):
    value = factory()
    struc_arg = value.arg_class(value=value)
    asm = struc_arg.struct_desc()
    struc_descs = set()
    for a in struc_arg.args:
        if isinstance(a, ComplexArgument):
            sdesc = a.struct_desc()
            if sdesc not in struc_descs:
                struc_descs.add(sdesc)
                asm = sdesc + asm
    asm = "#DATA\n" + asm
    code = translate(asm)
    desc = code.get_struct_desc(struc_arg.type_name())
    struc_arg.struct_descs[struc_arg.type_name()] = desc

    _user_types[user_type.__name__] = factory


def get_user_type_factory(type_name):
    return _user_types.get(type_name, None)
