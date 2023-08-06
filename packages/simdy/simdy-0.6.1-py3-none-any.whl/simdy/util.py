

_counter = 10000


def generate_name(prefix):
    global _counter
    _counter += 1
    return '%s_%i' % (prefix, _counter)
