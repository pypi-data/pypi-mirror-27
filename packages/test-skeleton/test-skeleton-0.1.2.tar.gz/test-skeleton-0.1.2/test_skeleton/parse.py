import os
import ast


class ParseResult(object):
    def __init__(self, funcs, klasses):
        self.funcs = funcs
        self.klasses = klasses


class ParsedClass(object):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class ParsedFunc(object):
    def __init__(self, name):
        self.name = name


def parse(input_path):
    abs_path = os.path.abspath(input_path)
    if not os.path.isfile(abs_path):
        raise ValueError('{} is not a file'.format(abs_path))

    with open(abs_path, 'r') as f:
        content = f.read()
        mod = ast.parse(content)
        funcs = [ParsedFunc(f.name) for f in _get_funcs(mod.body)]
        klasses = []
        for c in _get_classes(mod.body):
            methods = [ParsedFunc(f.name) for f in _get_funcs(c.body)]
            klasses.append(ParsedClass(c.name, methods))

    return ParseResult(funcs, klasses)


def _get_classes(body):
    return [c for c in body if isinstance(c, ast.ClassDef)]


def _get_funcs(body):
    return [f for f in body if isinstance(f, ast.FunctionDef)]
