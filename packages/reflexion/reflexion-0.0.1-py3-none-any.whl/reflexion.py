__author__ = 'Constantine Parkhimovich'
__copyright__ = 'Copyright 2017 Constantine Parkhimovich'
__license__ = 'MIT'
__title__ = 'reflexion'
__version__ = '0.0.1'


from inspect import getattr_static


def back(obj):
    return obj.__bak__()


class Reflexion:
    def __init__(self, obj, prev=None):
        self.__current__ = obj
        self.__prev__ = prev

    def __back__(self):
        return self.__prev__

    def __getattr__(self, name):
        attr = getattr_static(self.__current__, name)
        new = Reflexion(attr, self)
        return new


# test

class C:
    pass


class D:
    c = C()
