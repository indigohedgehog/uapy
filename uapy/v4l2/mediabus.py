from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.videodev import *


class V4l2_Mbus_Framefmt(Structure):
    _fields_ = [('width', c_uint32), ('height', c_uint32), ('code', c_uint),
                ('field', c_uint32), ('colorspace', c_uint32),
                ('ycbcr_enc', c_uint16), ('quantization', c_uint16),
                ('xfer_func', c_uint16), ('reserved', c_uint16 * 11)]
