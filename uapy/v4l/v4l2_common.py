from ctypes import *
from enum import Enum

class V4l2_Sel_Tgt(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    CROP = 0x0000
    CROP_DEFAULT = 0x0001
    CROP_BOUNDS = 0x0002
    NATIVE_SIZE = 0x0003
    COMPOSE = 0x0100
    COMPOSE_DEFAULT = 0x0101
    COMPOSE_BOUNDS = 0x0102
    COMPOSE_PADDED = 0x0103


class V4l2_Sel_Flag(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (GE, LE, KEEP_CONFIG) = [1 << x for x in range(3)]


class V4l2_Edid(Structure):
    _fields_ = [('pad', c_uint32), ('start_block', c_uint32),
                ('blocks', c_uint32), ('reserved', c_uint32 * 5),
                ('edid', POINTER(c_uint8))]
