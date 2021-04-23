from ctypes import *

def _or(self, other):
    if hasattr(other, 'value'):
        other = other.value
    return c_uint64(self.value | other)


def _coerce(self, other):
    try:
        return self, self.__class__(other)
    except TypeError:
        return NotImplemented


c_uint64.__or__ = _or
c_uint64.__coerce__ = _coerce

def c_type(arg):
    return arg.__c_type__()