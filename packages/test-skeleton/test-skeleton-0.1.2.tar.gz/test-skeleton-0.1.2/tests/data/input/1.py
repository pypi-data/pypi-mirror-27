import datetime as dt
import sys

# Comment

CONSTANT_VALUE = 'asd'


class Klass(object):
    klass_var = ''

    def __init__(self):
        self.a = ''

    @property
    def property1(self):
        pass

    @classmethod
    def klassmethod1(cls):
        pass

    def method_with_under_score(self):
        pass


def helper_function1():
    pass


class SubKlass(Klass):
    def __init__(self):
        pass

    def method1(self):
        pass

    def method2(self):
        pass

    def __repr__(self):
        return ''

    def __str__(self):
        return ''
