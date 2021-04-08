from ctypes import *
from enum import Enum

def v4l2_fourcc(a, b, c, d):
    return ord(a) | (ord(b) << 8) | (ord(c) << 16) | (ord(d) << 24)

def v4l2_fourcc_be(a, b, c, d):
    return v4l2_fourcc(a, b, c, d) | (c_uint(1) << 31)

class V4L2_FIELD(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (
        ANY,
        NONE,
        TOP,
        BOTTOM,
        INTERLACED,
        SEQ_TB,
        SEQ_BT,
        ALTERNATE,
        INTERLACED_TB,
        INTERLACED_BT,
    ) = range(10)

def V4L2_FIELD_HAS_TOP(field):
    return (
	field == V4L2_FIELD.TOP or
	field == V4L2_FIELD.INTERLACED or
	field == V4L2_FIELD.INTERLACED_TB or
	field == V4L2_FIELD.INTERLACED_BT or
	field == V4L2_FIELD.SEQ_TB or
	field == V4L2_FIELD.SEQ_BT)


def V4L2_FIELD_HAS_BOTTOM(field):
    return (
        field == V4L2_FIELD.BOTTOM or
        field == V4L2_FIELD.INTERLACED or
        field == V4L2_FIELD.INTERLACED_TB or
        field == V4L2_FIELD.INTERLACED_BT or
        field == V4L2_FIELD.SEQ_TB or
        field == V4L2_FIELD.SEQ_BT)


def V4L2_FIELD_HAS_BOTH(field):
    return (
        field == V4L2_FIELD.INTERLACED or
        field == V4L2_FIELD.INTERLACED_TB or
        field == V4L2_FIELD.INTERLACED_BT or
        field == V4L2_FIELD.SEQ_TB or
        field == V4L2_FIELD.SEQ_BT)

def V4L2_FIELD_HAS_T_OR_B(field):
	return (
        field == V4L2_FIELD.BOTTOM or
	    field == V4L2_FIELD.TOP or
	    field == V4L2_FIELD.ALTERNATE)

def V4L2_FIELD_IS_INTERLACED(field):
	return (
        field == V4L2_FIELD.INTERLACED or
	    field == V4L2_FIELD.INTERLACED_TB or
	    field == V4L2_FIELD.INTERLACED_BT)

def V4L2_FIELD_IS_SEQUENTIAL(field):
	return (
        field == V4L2_FIELD.SEQ_TB or
	    field == V4L2_FIELD.SEQ_BT)        

class V4L2_BUF_TYPE(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (   
        VIDEO_CAPTURE,
	    VIDEO_OUTPUT,
        VIDEO_OVERLAY,
        VBI_CAPTURE,
        VBI_OUTPUT,
        SLICED_VBI_CAPTURE,
        SLICED_VBI_OUTPUT,
        VIDEO_OUTPUT_OVERLAY,
        VIDEO_CAPTURE_MPLANE,
        VIDEO_OUTPUT_MPLANE,
        SDR_CAPTURE,
        SDR_OUTPUT,
        META_CAPTURE,
        META_OUTPUT,
        PRIVATE
    ) = list(range(1, 15)) + [0x80]

def V4L2_TYPE_IS_MULTIPLANAR(type):
    return (
        type == V4L2_BUF_TYPE.VIDEO_CAPTURE_MPLANE or
	    type == V4L2_BUF_TYPE.VIDEO_OUTPUT_MPLANE)

def V4L2_TYPE_IS_OUTPUT(type):
	return (
        type == V4L2_BUF_TYPE.VIDEO_OUTPUT or
        type == V4L2_BUF_TYPE.VIDEO_OUTPUT_MPLANE or
        type == V4L2_BUF_TYPE.VIDEO_OVERLAY or
        type == V4L2_BUF_TYPE.VIDEO_OUTPUT_OVERLAY or
        type == V4L2_BUF_TYPE.VBI_OUTPUT or
        type == V4L2_BUF_TYPE.SLICED_VBI_OUTPUT or
        type == V4L2_BUF_TYPE.SDR_OUTPUT or
        type == V4L2_BUF_TYPE.META_OUTPUT)

class V4L2_TUNER(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (
        RADIO,
        ANALOG_TV,
        DIGITAL_TV,
        SDR,
        RF
    ) = range(1, 6)

def V4L2_TUNER_ADC():
    return V4L2_TUNER.SDR

class V4L2_MEMORY(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (
        MMAP,
        USERPTR,
        OVERLAY,
        DMABUF,
    ) = range(1,5)

class V4L2_COLORSPACE(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (
        DEFAULT,
        SMPTE170M,
        SMPTE240M,
        REC709,
        BT878,
        _470_SYSTEM_M,
        _470_SYSTEM_BG,
        JPEG,
        SRGB,
        OPRGB,
        BT2020,
        RAW,
        DCI_P3
    ) = range(13)

def V4L2_MAP_COLORSPACE_DEFAULT(is_sdtv, is_hdtv):
    return(
        (V4L2_COLORSPACE.SRGB, 
        V4L2_COLORSPACE.REC709)[is_hdtv],
        V4L2_COLORSPACE.SMPTE170M)[is_sdtv]

class V4L2_XFER_FUNC(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (
        DEFAULT,
        _709,
        SRGB,
        OPRGB,
        SMPTE240M,
        NONE,
        DCI_P3,
        SMPTE2084
    ) = range(8)

def V4L2_MAP_XFER_FUNC_DEFAULT(colsp):
    (((((V4L2_XFER_FUNC._709, V4L2_XFER_FUNC.SRGB)[colsp == V4L2_COLORSPACE.SRGB or 
    colsp == V4L2_COLORSPACE.JPEG], 
    V4L2_XFER_FUNC.NONE)[colsp == V4L2_COLORSPACE.RAW], 
    V4L2_XFER_FUNC.DCI_P3)[colsp == V4L2_COLORSPACE.DCI_P3], 
    V4L2_XFER_FUNC.SMPTE240M)[colsp == V4L2_COLORSPACE.SMPTE240M], 
    V4L2_XFER_FUNC.OPRGB)[colsp == V4L2_COLORSPACE.OPRGB]

class V4L2_YCBCR_ENC(Enum):
    def __str__(self):
        return '{0}'.format(self.value)
    (
        DEFAULT,
        _601,
        _709,
        XV601,
        XV709,
        SYCC,
        BT2020,
        BT2020_CONST_LUM,
        SMPTE240M
    ) = range(9)
