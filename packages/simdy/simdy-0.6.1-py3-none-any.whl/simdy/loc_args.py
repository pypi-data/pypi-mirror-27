
from collections import defaultdict


class LocalArgs:
    def __init__(self):
        self._free_args = defaultdict(set)
        self._used_args = {}

    def get_arg(self, name):
        return self._used_args.get(name, None)

    def add(self, name, arg):
        loc_arg = self.get_arg(name)
        if loc_arg and self._tname(loc_arg) == self._tname(arg):
            return loc_arg

        if loc_arg is not None:
            self._free_args[self._tname(loc_arg)].add(loc_arg)

        loc_arg = self._get_free_arg(arg)
        if loc_arg is None:
            loc_arg = arg

        self._used_args[name] = loc_arg
        return loc_arg

    def _get_free_arg(self, arg):
        # TODO: Problems can ocur, further investigation needed, below is example that can cause problem
        # for i in range(10):
        #   if some_event:
        #       obj = objects[i]
        # usage of obj outside of for loop
        return None

        try:
            return self._free_args[self._tname(arg)].pop()
        except KeyError:
            return None

    def _tname(self, arg):
        if arg.is_pointer():
            return arg.type_name() + arg.arg.type_name()
        return arg.type_name()

    def __iter__(self):
        for arg in self._used_args.values():
            yield arg

        for arg_type, args in self._free_args.items():
            for arg in args:
                yield arg

    def add_free_args(self, args):
        for arg in args:
            self._free_args[self._tname(arg)].add(arg)

    def grab_free_args(self):
        args = []
        for a in self._free_args.values():
            args.extend(list(a))
        self._free_args.clear()
        return args
