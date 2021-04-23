from ctypes import *
from enum import IntEnum


def c_type(arg):
    return arg.__c_type__()


class Ioc(IntEnum):
    def __c_type__():
        return c_int32

    def __str__(self):
        return '{0}'.format(self.value)

    NRBITS = 8
    TYPEBITS = 8
    SIZEBITS = 14
    DIRBITS = 2

    NRMASK = ((1 << NRBITS) - 1)
    TYPEMASK = ((1 << TYPEBITS) - 1)
    SIZEMASK = ((1 << SIZEBITS) - 1)
    DIRMASK = ((1 << DIRBITS) - 1)

    NRSHIFT = 0
    TYPESHIFT = NRSHIFT + NRBITS
    SIZESHIFT = TYPESHIFT + TYPEBITS
    DIRSHIFT = SIZESHIFT + SIZEBITS

    NONE = 0
    WRITE = 1
    READ = 2

    IN = (WRITE << DIRSHIFT)
    OUT = (READ << DIRSHIFT)
    INOUT = ((WRITE | READ) << DIRSHIFT)
    SIZE_MASK = (SIZEMASK << SIZESHIFT)
    SIZE_SHIFT = (SIZESHIFT)


def ioc(dir_, type_, nr, size):
    return ((dir_ << Ioc.DIRSHIFT) | (ord(type_) << Ioc.TYPESHIFT) |
            (nr << Ioc.NRSHIFT) | (size << Ioc.SIZESHIFT))


def ioc_typecheck(t):
    return sizeof(t)


def io(type_, nr):
    return ioc(Ioc.NONE, type_, nr, 0)


def iow(type_, nr, size):
    return ioc(Ioc.WRITE, type_, nr, ioc_typecheck(size))


def ior(type_, nr, size):
    return ioc(Ioc.READ, type_, nr, ioc_typecheck(size))


def iowr(type_, nr, size):
    return ioc(Ioc.READ | Ioc.WRITE, type_, nr, ioc_typecheck(size))


def ior_bad(type_, nr, size):
    ioc(Ioc.READ, (type_), (nr), sizeof(size))


def iow_bad(type_, nr, size):
    ioc(Ioc.WRITE, (type_), (nr), sizeof(size))


def iowr_bad(type_, nr, size):
    ioc(Ioc.READ | Ioc.WRITE, (type_), (nr), sizeof(size))


def ioc_dir(nr):
    (((nr) >> Ioc.DIRSHIFT) & Ioc.DIRMASK)


def ioc_type(nr):
    (((nr) >> Ioc.TYPESHIFT) & Ioc.TYPEMASK)


def ioc_nr(nr):
    (((nr) >> Ioc.NRSHIFT) & Ioc.NRMASK)


def ioc_size(nr):
    (((nr) >> Ioc.SIZESHIFT) & Ioc.SIZEMASK)
