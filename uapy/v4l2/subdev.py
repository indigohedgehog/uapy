from ctypes import *
from enum import IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.mediabus import *
from v4l2.videodev import *


class V4l2_Subdev_Format_Whence(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (TRY, ACTIVE) = range(2)


class V4l2_Subdev_Format(Structure):
    _fields_ = [('which', c_uint32), ('pad', c_uint32),
                ('format', V4l2_Mbus_Framefmt), ('reserved', c_uint32 * 8)]


class V4l2_Subdev_Crop(Structure):
    _fields_ = [('which', c_uint32), ('pad', c_uint32), ('rect', V4l2_Rect),
                ('reserved', c_uint32 * 8)]


class V4l2_Subdev_Mbus_Code_Enum(Structure):
    _fields_ = [('pad', c_uint32), ('index', c_uint32), ('code', c_uint32),
                ('which', c_uint32), ('reserved', c_uint32 * 8)]


class V4l2_Subdev_Frame_Size_Enum(Structure):
    _fields_ = [('index', c_uint32), ('pad', c_uint32), ('code', c_uint32),
                ('min_width', c_uint32), ('max_width', c_uint32),
                ('min_height', c_uint32), ('max_height', c_uint32),
                ('which', c_uint32), ('reserved', c_uint32 * 8)]


class V4l2_Subdev_Frame_Interval(Structure):
    _fields_ = [('pad', c_uint32), ('interval', V4l2_Fract),
                ('reserved', c_uint32 * 9)]


class V4l2_Subdev_Frame_Interval_Enum(Structure):
    _fields_ = [('index', c_uint32), ('pad', c_uint32), ('code', c_uint32),
                ('width', c_uint32), ('height', c_uint32),
                ('interval', V4l2_Fract), ('which', c_uint32),
                ('reserved', c_uint32 * 8)]


class V4l2_Subdev_Selection(Structure):
    _fields_ = [
        ('which', c_uint32),
        ('pad', c_uint32),
        ('target', c_uint32),
        ('flags', c_uint32),
        ('r', V4l2_Rect),
        ('reserved', c_uint32 * 8),
    ]


class V4l2_Subdev_Capability(Structure):
    _fields_ = [('version', c_uint32), ('capabilities', c_uint32),
                ('reserved', c_uint32 * 14)]


class V4l2_Subdev_Cap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    RO_SUBDEV = 0x00000001


V4l2_Subdev_Edid = V4l2_Edid


class Vidioc_Subdev(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    QUERYCAP = ior('V', 0, V4l2_Subdev_Capability)
    G_FMT = iowr('V', 4, V4l2_Subdev_Format)
    S_FMT = iowr('V', 5, V4l2_Subdev_Format)
    G_FRAME_INTERVAL = iowr('V', 21, V4l2_Subdev_Frame_Interval)
    S_FRAME_INTERVAL = iowr('V', 22, V4l2_Subdev_Frame_Interval)
    ENUM_MBUS_CODE = iowr('V', 2, V4l2_Subdev_Mbus_Code_Enum)
    ENUM_FRAME_SIZE = iowr('V', 74, V4l2_Subdev_Frame_Size_Enum)
    ENUM_FRAME_INTERVAL = iowr('V', 75, V4l2_Subdev_Frame_Interval_Enum)
    G_CROP = iowr('V', 59, V4l2_Subdev_Crop)
    S_CROP = iowr('V', 60, V4l2_Subdev_Crop)
    G_SELECTION = iowr('V', 61, V4l2_Subdev_Selection)
    S_SELECTION = iowr('V', 62, V4l2_Subdev_Selection)
    G_STD = ior('V', 23, V4l2_Std_Id)
    S_STD = iow('V', 24, V4l2_Std_Id)
    ENUMSTD = iowr('V', 25, V4l2_Standard)
    G_EDID = iowr('V', 40, V4l2_Edid)
    S_EDID = iowr('V', 41, V4l2_Edid)
    QUERYSTD = ior('V', 63, V4l2_Std_Id)
    S_DV_TIMINGS = iowr('V', 87, V4l2_Dv_Timings)
    G_DV_TIMINGS = iowr('V', 88, V4l2_Dv_Timings)
    ENUM_DV_TIMINGS = iowr('V', 98, V4l2_Enum_Dv_Timings)
    QUERY_DV_TIMINGS = ior('V', 99, V4l2_Dv_Timings)
    DV_TIMINGS_CAP = iowr('V', 100, V4l2_Dv_Timings_Cap)
