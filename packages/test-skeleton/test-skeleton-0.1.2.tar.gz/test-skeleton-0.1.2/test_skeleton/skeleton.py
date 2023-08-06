def create(parsed):
    res = ''
    for c in parsed.klasses:
        methods = [m for m in c.methods if not m.name.startswith('__')]
        if methods:
            res += 'class Test{}:\n'.format(c.name)
            for m in methods:
                res += '\tclass Test{}:\n'.format(_to_camel_case(m.name))
                res += '\t\tdef test_TODO(self):\n\t\t\tpass\n\n'

    for f in parsed.funcs:
        res += 'class Test{}:\n'.format(_to_camel_case(f.name))
        res += '\tdef test_TODO(self):\n\t\tpass\n\n'

    return res


def _to_camel_case(s):
    return ''.join(x for x in s.title() if not x.isspace()).replace('_', '')
