from ctypes import *
from enum import IntEnum


class V4l2_Sel_Tgt(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    CROP = 0x0000

    (CROP_DEFAULT, CROP_BOUNDS, NATIVE_SIZE) = [(1 << 0) + x for x in range(3)]

    (COMPOSE, COMPOSE_DEFAULT, COMPOSE_BOUNDS,
     COMPOSE_PADDED) = [(1 << 8) + x for x in range(4)]


class V4l2_Sel_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (GE, LE, KEEP_CONFIG) = [1 << x for x in range(3)]


class V4l2_Edid(Structure):
    _fields_ = [('pad', c_uint32), ('start_block', c_uint32),
                ('blocks', c_uint32), ('reserved', c_uint32 * 5),
                ('edid', POINTER(c_uint8))]
