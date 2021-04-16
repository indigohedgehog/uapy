from ctypes import *
from enum import Enum


#to do: move to another module
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
#to do


def c_type(arg):
    return arg._Type.value


def v4l2_fourcc(a, b, c, d):
    return ord(a) | (ord(b) << 8) | (ord(c) << 16) | (ord(d) << 24)


def v4l2_fourcc_be(a, b, c, d):
    return v4l2_fourcc(a, b, c, d) | (1 << 31)


class V4l2_Field(Enum):
    _Type = c_uint32

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


def v4l2_field_has_top(field):
    return (field == V4l2_Field.TOP or field == V4l2_Field.INTERLACED
            or field == V4l2_Field.INTERLACED_TB
            or field == V4l2_Field.INTERLACED_BT or field == V4l2_Field.SEQ_TB
            or field == V4l2_Field.SEQ_BT)


def v4l2_field_has_bottom(field):
    return (field == V4l2_Field.BOTTOM or field == V4l2_Field.INTERLACED
            or field == V4l2_Field.INTERLACED_TB
            or field == V4l2_Field.INTERLACED_BT or field == V4l2_Field.SEQ_TB
            or field == V4l2_Field.SEQ_BT)


def v4l2_field_has_both(field):
    return (field == V4l2_Field.INTERLACED or field == V4l2_Field.INTERLACED_TB
            or field == V4l2_Field.INTERLACED_BT or field == V4l2_Field.SEQ_TB
            or field == V4l2_Field.SEQ_BT)


def v4l2_field_has_t_or_b(field):
    return (field == V4l2_Field.BOTTOM or field == V4l2_Field.TOP
            or field == V4l2_Field.ALTERNATE)


def v4l2_field_is_interlaced(field):
    return (field == V4l2_Field.INTERLACED or field == V4l2_Field.INTERLACED_TB
            or field == V4l2_Field.INTERLACED_BT)


def v4l2_field_is_sequential(field):
    return (field == V4l2_Field.SEQ_TB or field == V4l2_Field.SEQ_BT)


class V4l2_Buf_Type(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (VIDEO_CAPTURE, VIDEO_OUTPUT, VIDEO_OVERLAY, VBI_CAPTURE, VBI_OUTPUT,
     SLICED_VBI_CAPTURE, SLICED_VBI_OUTPUT, VIDEO_OUTPUT_OVERLAY,
     VIDEO_CAPTURE_MPLANE, VIDEO_OUTPUT_MPLANE, SDR_CAPTURE, SDR_OUTPUT,
     META_CAPTURE, META_OUTPUT, PRIVATE) = list(range(1, 15)) + [0x80]


def v4l2_type_is_multiplanar(type):
    return (type == V4l2_Buf_Type.VIDEO_CAPTURE_MPLANE
            or type == V4l2_Buf_Type.VIDEO_OUTPUT_MPLANE)


def v4l2_type_is_output(type):
    return (type == V4l2_Buf_Type.VIDEO_OUTPUT
            or type == V4l2_Buf_Type.VIDEO_OUTPUT_MPLANE
            or type == V4l2_Buf_Type.VIDEO_OVERLAY
            or type == V4l2_Buf_Type.VIDEO_OUTPUT_OVERLAY
            or type == V4l2_Buf_Type.VBI_OUTPUT
            or type == V4l2_Buf_Type.SLICED_VBI_OUTPUT
            or type == V4l2_Buf_Type.SDR_OUTPUT
            or type == V4l2_Buf_Type.META_OUTPUT)


class V4l2_Tuner_Type(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (RADIO, ANALOG_TV, DIGITAL_TV, SDR, RF) = range(1, 6)
    ADC = SDR


class V4l2_Memory(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (
        MMAP,
        USERPTR,
        OVERLAY,
        DMABUF,
    ) = range(1, 5)


class V4l2_Colorspace(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, SMPTE170M, SMPTE240M, REC709, BT878, C470_SYSTEM_M,
     C470_SYSTEM_BG, JPEG, SRGB, OPRGB, BT2020, RAW, DCI_P3) = range(13)


def v4l2_map_colorspace_default(is_sdtv, is_hdtv):
    return ((V4l2_Colorspace.SRGB, V4l2_Colorspace.REC709)[is_hdtv],
            V4l2_Colorspace.SMPTE170M)[is_sdtv]


class V4l2_Xfer_Func(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, X709, SRGB, OPRGB, SMPTE240M, NONE, DCI_P3, SMPTE2084) = range(8)


def v4l2_map_xfer_func_default(colsp):
    return (((((V4l2_Xfer_Func.X709,
                V4l2_Xfer_Func.SRGB)[colsp == V4l2_Colorspace.SRGB
                                     or colsp == V4l2_Colorspace.JPEG],
               V4l2_Xfer_Func.NONE)[colsp == V4l2_Colorspace.RAW],
              V4l2_Xfer_Func.DCI_P3)[colsp == V4l2_Colorspace.DCI_P3],
             V4l2_Xfer_Func.SMPTE240M)[colsp == V4l2_Colorspace.SMPTE240M],
            V4l2_Xfer_Func.OPRGB)[colsp == V4l2_Colorspace.OPRGB]


class V4l2_Ycbcr_Enc(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, Y601, Y709, XV601, XV709, SYCC, BT2020, BT2020_CONST_LUM,
     SMPTE240M) = range(9)


class V4l2_Hsv_Enc(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (H180, H256) = range(128, 130)


def v4l2_map_ycbcr_enc_default(colsp):
    return (((V4l2_Ycbcr_Enc.Y601,
              V4l2_Ycbcr_Enc.SMPTE240M)[colsp == V4l2_Colorspace.SMPTE240M],
             V4l2_Ycbcr_Enc.BT2020)[colsp == V4l2_Colorspace.BT2020],
            V4l2_Ycbcr_Enc.Y709)[colsp == V4l2_Colorspace.REC709
                                 or colsp == V4l2_Colorspace.DCI_P3]


class V4l2_Quantization(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, FULL_RANGE, LIM_RANGE) = range(3)


def v4l2_map_quantization_default(is_rgb_or_hsv, colsp, ycbcr_enc):
    return ((V4l2_Quantization.LIM_RANGE,
             V4l2_Quantization.FULL_RANGE)[((is_rgb_or_hsv) or
                                            (colsp) == V4l2_Colorspace.JPEG)],
            V4l2_Quantization.LIM_RANGE)[((is_rgb_or_hsv) and
                                          (colsp) == V4l2_Colorspace.BT2020)]


class V4l2_Priority(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (
        UNSET,
        BACKGROUND,
        INTERACTIVE,
        RECORD,
    ) = list(range(0, 4))
    DEFAULT = INTERACTIVE


class V4l2_Rect(Structure):
    _fields_ = [
        ('left', c_int32),
        ('top', c_int32),
        ('width', c_uint32),
        ('height', c_uint32),
    ]


class V4l2_Fract(Structure):
    _fields_ = [
        ('numerator', c_uint32),
        ('denominator', c_uint32),
    ]


class V4l2_Area(Structure):
    _fields_ = [
        ('width', c_uint32),
        ('height', c_uint32),
    ]


class V4l2_Capability(Structure):
    _fields_ = [('driver', c_uint8 * 16), ('card', c_uint8 * 32),
                ('bus_info', c_uint8 * 32), ('version', c_uint32),
                ('capabilities', c_uint32), ('device_caps', c_uint32),
                ('reserved', c_uint32 * 3)]


class V4l2_Mode(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    HIGHQUALITY = 0 << 1


class V4l2_Cap(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (VIDEO_CAPTURE, VIDEO_OUTPUT, VIDEO_OVERLAY, VBI_CAPTURE, VBI_OUTPUT,
     SLICED_VBI_CAPTURE, SLICED_VBI_OUTPUT, RDS_CAPTURE, VIDEO_OUTPUT_OVERLAY,
     HW_FREQ_SEEK, RDS_OUTPUT, VIDEO_CAPTURE_MPLANE, VIDEO_OUTPUT_MPLANE,
     VIDEO_M2M_MPLANE, VIDEO_M2M, TUNER, AUDIO, RADIO, MODULATOR, SDR_CAPTURE,
     EXT_PIX_FORMAT, SDR_OUTPUT, META_CAPTURE, READWRITE, ASYNCIO, STREAMING,
     META_OUTPUT, TOUCH, IO_MC) = [1 << x for x in range(29)]
    DEVICE_CAPS = 1 << 30
    TIMEPERFRAME = 1 << 13


class V4l2_Fmt(Structure):
    _fields_ = [('width', c_uint32), ('height', c_uint32),
                ('pixelformat', c_uint32), ('field', c_type(V4l2_Field)),
                ('bytesperline', c_uint32), ('sizeimage', c_uint32),
                ('colorspace', c_type(V4l2_Colorspace)), ('priv', c_uint32)]


class V4l2_Fmt_Flag(Enum):
    _Type = c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (COMPRESSED, EMULATED, CONTINUOUS_BYTESTREAM,
     DYN_RESOLUTION) = [1 << x for x in range(4)]


class V4l2_Pix_Format(Structure):
    class _u(Union):
        _fields_ = [('ycbcr_enc', c_type(V4l2_Ycbcr_Enc)),
                    ('hsv_enc', c_type(V4l2_Hsv_Enc))]

    _fields_ = V4l2_Fmt._fields_ + [
        ('flags', c_type(V4l2_Fmt_Flag)),
        ('_u', _u),
        ('quantization', c_type(V4l2_Quantization)),
        ('xfer_func', c_type(V4l2_Xfer_Func)),
    ]


class V4l2_Pix_Fmt(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    RGB332 = v4l2_fourcc('R', 'G', 'B', '1')
    RGB444 = v4l2_fourcc('R', '4', '4', '4')
    ARGB444 = v4l2_fourcc('A', 'R', '1', '2')
    XRGB444 = v4l2_fourcc('X', 'R', '1', '2')
    RGBA444 = v4l2_fourcc('R', 'A', '1', '2')
    RGBX444 = v4l2_fourcc('R', 'X', '1', '2')
    ABGR444 = v4l2_fourcc('A', 'B', '1', '2')
    XBGR444 = v4l2_fourcc('X', 'B', '1', '2')
    BGRX444 = v4l2_fourcc('B', 'X', '1', '2')
    RGB555 = v4l2_fourcc('R', 'G', 'B', 'O')
    ARGB555 = v4l2_fourcc('A', 'R', '1', '5')
    XRGB555 = v4l2_fourcc('X', 'R', '1', '5')
    RGBA555 = v4l2_fourcc('R', 'A', '1', '5')
    RGBX555 = v4l2_fourcc('R', 'X', '1', '5')
    ABGR555 = v4l2_fourcc('A', 'B', '1', '5')
    XBGR555 = v4l2_fourcc('X', 'B', '1', '5')
    BGRA555 = v4l2_fourcc('B', 'A', '1', '5')
    BGRX555 = v4l2_fourcc('B', 'X', '1', '5')
    RGB565 = v4l2_fourcc('R', 'G', 'B', 'P')
    RGB555X = v4l2_fourcc('R', 'G', 'B', 'Q')
    ARGB555X = v4l2_fourcc_be('A', 'R', '1', '5')
    XRGB555X = v4l2_fourcc_be('X', 'R', '1', '5')
    RGB565X = v4l2_fourcc('R', 'G', 'B', 'R')
    BGR666 = v4l2_fourcc('B', 'G', 'R', 'H')
    BGR24 = v4l2_fourcc('B', 'G', 'R', '3')
    RGB24 = v4l2_fourcc('R', 'G', 'B', '3')
    BGR32 = v4l2_fourcc('B', 'G', 'R', '4')
    ABGR32 = v4l2_fourcc('A', 'R', '2', '4')
    XBGR32 = v4l2_fourcc('X', 'R', '2', '4')
    BGRA32 = v4l2_fourcc('R', 'A', '2', '4')
    BGRX32 = v4l2_fourcc('R', 'X', '2', '4')
    RGB32 = v4l2_fourcc('R', 'G', 'B', '4')
    RGBA32 = v4l2_fourcc('A', 'B', '2', '4')
    RGBX32 = v4l2_fourcc('X', 'B', '2', '4')
    ARGB32 = v4l2_fourcc('B', 'A', '2', '4')
    XRGB32 = v4l2_fourcc('B', 'X', '2', '4')
    GREY = v4l2_fourcc('G', 'R', 'E', 'Y')
    Y4 = v4l2_fourcc('Y', '0', '4', ' ')
    Y6 = v4l2_fourcc('Y', '0', '6', ' ')
    Y10 = v4l2_fourcc('Y', '1', '0', ' ')
    Y12 = v4l2_fourcc('Y', '1', '2', ' ')
    Y14 = v4l2_fourcc('Y', '1', '4', ' ')
    Y16 = v4l2_fourcc('Y', '1', '6', ' ')
    Y16_BE = v4l2_fourcc_be('Y', '1', '6', ' ')
    Y10BPACK = v4l2_fourcc('Y', '1', '0', 'B')
    Y10P = v4l2_fourcc('Y', '1', '0', 'P')
    PAL8 = v4l2_fourcc('P', 'A', 'L', '8')
    UV8 = v4l2_fourcc('U', 'V', '8', ' ')
    YUYV = v4l2_fourcc('Y', 'U', 'Y', 'V')
    YYUV = v4l2_fourcc('Y', 'Y', 'U', 'V')
    YVYU = v4l2_fourcc('Y', 'V', 'Y', 'U')
    UYVY = v4l2_fourcc('U', 'Y', 'V', 'Y')
    VYUY = v4l2_fourcc('V', 'Y', 'U', 'Y')
    Y41P = v4l2_fourcc('Y', '4', '1', 'P')
    YUV444 = v4l2_fourcc('Y', '4', '4', '4')
    YUV555 = v4l2_fourcc('Y', 'U', 'V', 'O')
    YUV565 = v4l2_fourcc('Y', 'U', 'V', 'P')
    YUV32 = v4l2_fourcc('Y', 'U', 'V', '4')
    AYUV32 = v4l2_fourcc('A', 'Y', 'U', 'V')
    XYUV32 = v4l2_fourcc('X', 'Y', 'U', 'V')
    VUYA32 = v4l2_fourcc('V', 'U', 'Y', 'A')
    VUYX32 = v4l2_fourcc('V', 'U', 'Y', 'X')
    HI240 = v4l2_fourcc('H', 'I', '2', '4')
    HM12 = v4l2_fourcc('H', 'M', '1', '2')
    M420 = v4l2_fourcc('M', '4', '2', '0')
    NV12 = v4l2_fourcc('N', 'V', '1', '2')
    NV21 = v4l2_fourcc('N', 'V', '2', '1')
    NV16 = v4l2_fourcc('N', 'V', '1', '6')
    NV61 = v4l2_fourcc('N', 'V', '6', '1')
    NV24 = v4l2_fourcc('N', 'V', '2', '4')
    NV42 = v4l2_fourcc('N', 'V', '4', '2')
    NV12M = v4l2_fourcc('N', 'M', '1', '2')
    NV21M = v4l2_fourcc('N', 'M', '2', '1')
    NV16M = v4l2_fourcc('N', 'M', '1', '6')
    NV61M = v4l2_fourcc('N', 'M', '6', '1')
    NV12MT = v4l2_fourcc('T', 'M', '1', '2')
    NV12MT_16X16 = v4l2_fourcc('V', 'M', '1', '2')
    YUV410 = v4l2_fourcc('Y', 'U', 'V', '9')
    YVU410 = v4l2_fourcc('Y', 'V', 'U', '9')
    YUV411P = v4l2_fourcc('4', '1', '1', 'P')
    YUV420 = v4l2_fourcc('Y', 'U', '1', '2')
    YVU420 = v4l2_fourcc('Y', 'V', '1', '2')
    YUV422P = v4l2_fourcc('4', '2', '2', 'P')
    YUV420M = v4l2_fourcc('Y', 'M', '1', '2')
    YVU420M = v4l2_fourcc('Y', 'M', '2', '1')
    YUV422M = v4l2_fourcc('Y', 'M', '1', '6')
    YVU422M = v4l2_fourcc('Y', 'M', '6', '1')
    YUV444M = v4l2_fourcc('Y', 'M', '2', '4')
    YVU444M = v4l2_fourcc('Y', 'M', '4', '2')
    SBGGR8 = v4l2_fourcc('B', 'A', '8', '1')
    SGBRG8 = v4l2_fourcc('G', 'B', 'R', 'G')
    SGRBG8 = v4l2_fourcc('G', 'R', 'B', 'G')
    SRGGB8 = v4l2_fourcc('R', 'G', 'G', 'B')
    SBGGR10 = v4l2_fourcc('B', 'G', '1', '0')
    SGBRG10 = v4l2_fourcc('G', 'B', '1', '0')
    SGRBG10 = v4l2_fourcc('B', 'A', '1', '0')
    SRGGB10 = v4l2_fourcc('R', 'G', '1', '0')
    SBGGR10P = v4l2_fourcc('p', 'B', 'A', 'A')
    SGBRG10P = v4l2_fourcc('p', 'G', 'A', 'A')
    SGRBG10P = v4l2_fourcc('p', 'g', 'A', 'A')
    SRGGB10P = v4l2_fourcc('p', 'R', 'A', 'A')
    SBGGR10ALAW8 = v4l2_fourcc('a', 'B', 'A', '8')
    SGBRG10ALAW8 = v4l2_fourcc('a', 'G', 'A', '8')
    SGRBG10ALAW8 = v4l2_fourcc('a', 'g', 'A', '8')
    SRGGB10ALAW8 = v4l2_fourcc('a', 'R', 'A', '8')
    SBGGR10DPCM8 = v4l2_fourcc('b', 'B', 'A', '8')
    SGBRG10DPCM8 = v4l2_fourcc('b', 'G', 'A', '8')
    SGRBG10DPCM8 = v4l2_fourcc('B', 'D', '1', '0')
    SRGGB10DPCM8 = v4l2_fourcc('b', 'R', 'A', '8')
    SBGGR12 = v4l2_fourcc('B', 'G', '1', '2')
    SGBRG12 = v4l2_fourcc('G', 'B', '1', '2')
    SGRBG12 = v4l2_fourcc('B', 'A', '1', '2')
    SRGGB12 = v4l2_fourcc('R', 'G', '1', '2')
    SBGGR12P = v4l2_fourcc('p', 'B', 'C', 'C')
    SGBRG12P = v4l2_fourcc('p', 'G', 'C', 'C')
    SGRBG12P = v4l2_fourcc('p', 'g', 'C', 'C')
    SRGGB12P = v4l2_fourcc('p', 'R', 'C', 'C')
    SBGGR14 = v4l2_fourcc('B', 'G', '1', '4')
    SGBRG14 = v4l2_fourcc('G', 'B', '1', '4')
    SGRBG14 = v4l2_fourcc('G', 'R', '1', '4')
    SRGGB14 = v4l2_fourcc('R', 'G', '1', '4')
    SBGGR14P = v4l2_fourcc('p', 'B', 'E', 'E')
    SGBRG14P = v4l2_fourcc('p', 'G', 'E', 'E')
    SGRBG14P = v4l2_fourcc('p', 'g', 'E', 'E')
    SRGGB14P = v4l2_fourcc('p', 'R', 'E', 'E')
    SBGGR16 = v4l2_fourcc('B', 'Y', 'R', '2')
    SGBRG16 = v4l2_fourcc('G', 'B', '1', '6')
    SGRBG16 = v4l2_fourcc('G', 'R', '1', '6')
    SRGGB16 = v4l2_fourcc('R', 'G', '1', '6')
    HSV24 = v4l2_fourcc('H', 'S', 'V', '3')
    HSV32 = v4l2_fourcc('H', 'S', 'V', '4')
    MJPEG = v4l2_fourcc('M', 'J', 'P', 'G')
    JPEG = v4l2_fourcc('J', 'P', 'E', 'G')
    DV = v4l2_fourcc('d', 'v', 's', 'd')
    MPEG = v4l2_fourcc('M', 'P', 'E', 'G')
    H264 = v4l2_fourcc('H', '2', '6', '4')
    H264_NO_SC = v4l2_fourcc('A', 'V', 'C', '1')
    H264_MVC = v4l2_fourcc('M', '2', '6', '4')
    H263 = v4l2_fourcc('H', '2', '6', '3')
    MPEG1 = v4l2_fourcc('M', 'P', 'G', '1')
    MPEG2 = v4l2_fourcc('M', 'P', 'G', '2')
    MPEG2_SLICE = v4l2_fourcc('M', 'G', '2', 'S')
    MPEG4 = v4l2_fourcc('M', 'P', 'G', '4')
    XVID = v4l2_fourcc('X', 'V', 'I', 'D')
    VC1_ANNEX_G = v4l2_fourcc('V', 'C', '1', 'G')
    VC1_ANNEX_L = v4l2_fourcc('V', 'C', '1', 'L')
    VP8 = v4l2_fourcc('V', 'P', '8', '0')
    VP9 = v4l2_fourcc('V', 'P', '9', '0')
    HEVC = v4l2_fourcc('H', 'E', 'V', 'C')
    FWHT = v4l2_fourcc('F', 'W', 'H', 'T')
    FWHT_STATELESS = v4l2_fourcc('S', 'F', 'W', 'H')
    CPIA1 = v4l2_fourcc('C', 'P', 'I', 'A')
    WNVA = v4l2_fourcc('W', 'N', 'V', 'A')
    SN9C10X = v4l2_fourcc('S', '9', '1', '0')
    SN9C20X_I420 = v4l2_fourcc('S', '9', '2', '0')
    PWC1 = v4l2_fourcc('P', 'W', 'C', '1')
    PWC2 = v4l2_fourcc('P', 'W', 'C', '2')
    ET61X251 = v4l2_fourcc('E', '6', '2', '5')
    SPCA501 = v4l2_fourcc('S', '5', '0', '1')
    SPCA505 = v4l2_fourcc('S', '5', '0', '5')
    SPCA508 = v4l2_fourcc('S', '5', '0', '8')
    SPCA561 = v4l2_fourcc('S', '5', '6', '1')
    PAC207 = v4l2_fourcc('P', '2', '0', '7')
    MR97310A = v4l2_fourcc('M', '3', '1', '0')
    JL2005BCD = v4l2_fourcc('J', 'L', '2', '0')
    SN9C2028 = v4l2_fourcc('S', 'O', 'N', 'X')
    SQ905C = v4l2_fourcc('9', '0', '5', 'C')
    PJPG = v4l2_fourcc('P', 'J', 'P', 'G')
    OV511 = v4l2_fourcc('O', '5', '1', '1')
    OV518 = v4l2_fourcc('O', '5', '1', '8')
    STV0680 = v4l2_fourcc('S', '6', '8', '0')
    TM6000 = v4l2_fourcc('T', 'M', '6', '0')
    CIT_YYVYUY = v4l2_fourcc('C', 'I', 'T', 'V')
    KONICA420 = v4l2_fourcc('K', 'O', 'N', 'I')
    JPGL = v4l2_fourcc('J', 'P', 'G', 'L')
    SE401 = v4l2_fourcc('S', '4', '0', '1')
    S5C_UYVY_JPG = v4l2_fourcc('S', '5', 'C', 'I')
    Y8I = v4l2_fourcc('Y', '8', 'I', ' ')
    Y12I = v4l2_fourcc('Y', '1', '2', 'I')
    Z16 = v4l2_fourcc('Z', '1', '6', ' ')
    MT21C = v4l2_fourcc('M', 'T', '2', '1')
    INZI = v4l2_fourcc('I', 'N', 'Z', 'I')
    SUNXI_TILED_NV12 = v4l2_fourcc('S', 'T', '1', '2')
    CNF4 = v4l2_fourcc('C', 'N', 'F', '4')
    IPU3_SBGGR10 = v4l2_fourcc('i', 'p', '3', 'b')
    IPU3_SGBRG10 = v4l2_fourcc('i', 'p', '3', 'g')
    IPU3_SGRBG10 = v4l2_fourcc('i', 'p', '3', 'G')
    IPU3_SRGGB10 = v4l2_fourcc('i', 'p', '3', 'r')
    PRIV_MAGIC = 0xfeedcafe
    FLAG_PREMUL_ALPHA = 0x00000001


class V4l2_Sdr_Fmt(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    CU8 = v4l2_fourcc('C', 'U', '0', '8')
    CU16LE = v4l2_fourcc('C', 'U', '1', '6')
    CS8 = v4l2_fourcc('C', 'S', '0', '8')
    CS14LE = v4l2_fourcc('C', 'S', '1', '4')
    RU12LE = v4l2_fourcc('R', 'U', '1', '2')
    PCU16BE = v4l2_fourcc('P', 'C', '1', '6')
    PCU18BE = v4l2_fourcc('P', 'C', '1', '8')
    PCU20BE = v4l2_fourcc('P', 'C', '2', '0')


class V4l2_Tch_Fmt(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    DELTA_TD16 = v4l2_fourcc('T', 'D', '1', '6')
    DELTA_TD08 = v4l2_fourcc('T', 'D', '0', '8')
    TU16 = v4l2_fourcc('T', 'U', '1', '6')
    TU08 = v4l2_fourcc('T', 'U', '0', '8')


class V4l2_Meta_Fmt(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    VSP1_HGO = v4l2_fourcc('V', 'S', 'P', 'H')
    VSP1_HGT = v4l2_fourcc('V', 'S', 'P', 'T')
    UVC = v4l2_fourcc('U', 'V', 'C', 'H')
    D4XX = v4l2_fourcc('D', '4', 'X', 'X')
    VIVID = v4l2_fourcc('V', 'I', 'V', 'D')


class V4l2_Fmtdesc(Structure):
    _fields_ = [('index', c_uint32), ('type', c_type(V4l2_Buf_Type)),
                ('flags', c_uint32), ('description', c_uint8 * 32),
                ('pixelformat', c_uint32), ('mbus_code', c_uint32),
                ('reserved', c_uint32 * 3)]


class V4l2_Frmsizetypes(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DISCRETE, CONTINUOUS, STEPWISE) = range(1, 4)


class V4l2_Frmsize_Discrete(Structure):
    _fields_ = [('width', c_uint32), ('height', c_uint32)]


class V4l2_Frmsize_Stepwise(Structure):
    _fields_ = [('min_width', c_uint32), ('max_width', c_uint32),
                ('step_width', c_uint32), ('min_height', c_uint32),
                ('max_height', c_uint32), ('step_height', c_uint32)]


class V4l2_Frmsizeenum(Structure):
    class _u(Union):
        _fields_ = [('discrete', V4l2_Frmsize_Discrete),
                    ('stepwise', V4l2_Frmsize_Stepwise)]

    _fields_ = [('index', c_uint32), ('pixel_format', c_uint32),
                ('type', c_uint32), ('_u', _u), ('reserved', c_uint32 * 2)]


class V4l2_Frmivaltypes(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DISCRETE, CONTINUOUS, STEPWISE) = range(1, 4)


class V4l2_Frmival_Stepwise(Structure):
    _fields_ = [('min', V4l2_Fract), ('max', V4l2_Fract), ('step', V4l2_Fract)]


class V4l2_Frmivalenum(Structure):
    class _u(Union):
        _fields_ = [('discrete', V4l2_Fract),
                    ('stepwise', V4l2_Frmsize_Stepwise)]

    _fields_ = [('index', c_uint32), ('pixel_format', c_uint32),
                ('width', c_uint32), ('height', c_uint32), ('type', c_uint32),
                ('_u', _u), ('reserved', c_uint32 * 2)]


class V4l2_Frmival_Stepwise(Structure):
    _fields_ = [('type', c_uint32), ('flags', c_uint32), ('frames', c_uint8),
                ('seconds', c_uint8), ('minutes', c_uint8), ('hours', c_uint8),
                ('userbits', c_uint8 * 4)]


class v4l2_Timecode(Structure):
    _fields_ = [('type', c_uint32), ('flags', c_uint32), ('frames', c_uint8),
                ('seconds', c_uint8), ('minutes', c_uint8), ('hours', c_uint8),
                ('userbits', c_uint8 * 4)]


class V4l2_Tc_Type(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (T24FPS, T25FPS, T30FPS, T50FPS, T60FPS) = range(1, 6)


class V4l2_Tc_Flag(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DROPFRAME, COLORFRAME) = [1 << x for x in range(2)]


class V4l2_Tc_Userbits(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    field = 0x000C
    USERDEFINED = 0x0000
    T8BITCHARS = 0x0008


class V4l2_Jpeg_Marker(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DHT, DQT, DRI, COM, APP) = [1 << x for x in range(3, 8)]


class V4l2_Jpegcompression(Structure):
    _fields_ = [('quality', c_int), ('APPn', c_int), ('APP_len', c_int),
                ('APP_data', c_char * 60), ('COM_len', c_int),
                ('COM_data', c_char * 60), ('jpeg_markers', c_uint32)]


class V4l2_Requestbuffers(Structure):
    _fields_ = [('count', c_uint32), ('type', c_type(V4l2_Buf_Type)),
                ('memory', c_type(V4l2_Memory)), ('capabilities', c_uint32),
                ('reserved', c_uint32)]


class V4l2_Buf_Cap_Supports(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (MMAP, USERPTR, DMABUF, REQUESTS, ORPHANED_BUFS,
     M2M_HOLD_CAPTURE_BUF) = [1 << x for x in range(6)]


class V4l2_Plane(Structure):
    class _u(Union):
        _fields_ = [('mem_offset', c_uint32), ('userptr', c_ulong),
                    ('fd', c_int32)]

    _fields_ = [('bytesused', c_uint32), ('length', c_uint32), ('_u', _u),
                ('data_offset', c_uint32), ('reserved', c_uint32 * 11)]


class Timeval(Structure):
    _fields_ = [
        ('secs', c_long),
        ('usecs', c_long),
    ]


class V4l2_Buffer(Structure):
    class _u(Union):
        _fields_ = [('offset', c_uint32), ('userptr', c_ulong),
                    ('planes', V4l2_Plane), ('fd', c_int32)]

    class _v(Union):
        _fields_ = [('request_fd', c_int32), ('reserved', c_uint32)]

    _fields_ = [('index', c_uint32), ('type', c_uint32),
                ('bytesused', c_uint32), ('flags', c_uint32),
                ('field', c_uint32), ('timestamp', Timeval),
                ('timecode', v4l2_Timecode), ('sequence', c_uint32),
                ('memory', c_uint32), ('_u', _u), ('length', c_uint32),
                ('reserved2', c_uint32), ('_v', _v)]


class V4l2_Buf_Flag(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (MAPPED, QUEUED, DONE, KEYFRAME, PFRAME, BFRAME, ERROR, IN_REQUEST,
     TIMECODE, M2M_HOLD_CAPTURE_BUF, PREPARED, NO_CACHE_INVALIDATE,
     NO_CACHE_CLEAN, TIMESTAMP_MONOTONIC,
     TIMESTAMP_COPY) = [1 << x for x in range(15)]
    TIMESTAMP_UNKNOWN = TSTAMP_SRC_EOF = 0x00000000
    TIMESTAMP_MASK = 0x0000e000
    TSTAMP_SRC_MASK = 0x00070000
    TSTAMP_SRC_SOE = 0x00010000
    LAST = 0x00100000
    REQUEST_FD = 0x00800000


class V4l2_Exportbuffer(Structure):
    _fields_ = [('type', c_type(V4l2_Buf_Type)), ('index', c_uint32),
                ('plane', c_uint32), ('flags', c_uint32), ('fd', c_int32),
                ('reserved', c_uint32 * 11)]


class V4l2_Framebuffer(Structure):
    _fields_ = [('capability', c_uint32), ('flags', c_uint32),
                ('base', c_void_p), ('fmt', V4l2_Fmt)]


class V4l2_Fbuf_Cap(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (EXTERNOVERLAY, CHROMAKEY, LIST_CLIPPING, BITMAP_CLIPPING, LOCAL_ALPHA,
     GLOBAL_ALPHA, LOCAL_INV_ALPHA,
     SRC_CHROMAKEY) = [1 << x for x in range(8)]


class V4l2_Fbuf_Flag(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PRIMARY, OVERLAY, CHROMAKEY, LOCAL_ALPHA, GLOBAL_ALPHA, LOCAL_INV_ALPHA,
     SRC_CHROMAKEY) = [1 << x for x in range(7)]


class V4l2_Clip(Structure):
    _fields_ = [('c', V4l2_Rect)]


V4l2_Clip._fields_.append(('next', POINTER(V4l2_Clip)))


class V4l2_Window(Structure):
    _fields_ = [('w', V4l2_Rect), ('field', c_type(V4l2_Field)),
                ('chromakey', c_uint32), ('clips', POINTER(V4l2_Clip)),
                ('clipcount', c_uint), ('bitmap', POINTER(c_void_p)),
                ('global_alpha', c_uint8)]


class V4l2_Captureparm(Structure):
    _fields_ = [('capability', c_uint32), ('capturemode', c_uint32),
                ('timeperframe', V4l2_Fract), ('extendedmode', c_uint32),
                ('readbuffers', c_uint32), ('reserved', c_uint32 * 4)]


class V4l2_Captureparm(Structure):
    _fields_ = [('capability', c_uint32), ('outputmode', c_uint32),
                ('timeperframe', V4l2_Fract), ('extendedmode', c_uint32),
                ('writebuffers', c_uint32), ('reserved', c_uint32 * 4)]


class V4l2_Cropcap(Structure):
    _fields_ = [
        ('type', c_type(V4l2_Buf_Type)),
        ('bounds', V4l2_Rect),
        ('defrect', V4l2_Rect),
        ('pixelaspect', V4l2_Fract),
    ]


class V4l2_Crop(Structure):
    _fields_ = [('type', c_type(V4l2_Buf_Type)), ('c', V4l2_Rect)]


class V4l2_Selection(Structure):
    _fields_ = [('type', c_uint32), ('target', c_uint32), ('flags', c_uint32),
                ('r', V4l2_Rect), ('reserved', c_uint32)]


V4l2_Std_Id = c_uint64


class V4l2_Std(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PAL_B, PAL_B1, PAL_G, PAL_H, PAL_I, PAL_D, PAL_D1, PAL_K, PAL_M, PAL_N,
     PAL_Nc, PAL_60, NTSC_M, NTSC_M_JP, NTSC_443, NTSC_M_KR, SECAM_B, SECAM_D,
     SECAM_G, SECAM_H, SECAM_K, SECAM_K1, SECAM_L, SECAM_LC, ATSC_8_VSB,
     ATSC_16_VSB) = [V4l2_Std_Id(1 << x) for x in range(26)]

    NTSC = (NTSC_M | NTSC_M_JP | NTSC_M_KR)
    SECAM_DK = (SECAM_D | SECAM_K | SECAM_K1)
    SECAM = (SECAM_B | SECAM_G | SECAM_H | SECAM_DK | SECAM_L | SECAM_LC)
    PAL_BG = (PAL_B | PAL_B1 | PAL_G)
    PAL_DK = (PAL_D | PAL_D1 | PAL_K)
    PAL = (PAL_BG | PAL_DK | PAL_H | PAL_I)
    B = (PAL_B | PAL_B1 | SECAM_B)
    G = (PAL_G | SECAM_G)
    H = (PAL_H | SECAM_H)
    L = (SECAM_L | SECAM_LC)
    GH = (G | H)
    DK = (PAL_DK | SECAM_DK)
    BG = (B | G)
    MN = (PAL_M | PAL_N | PAL_Nc | NTSC)
    MTS = (NTSC_M | PAL_M | PAL_N | PAL_Nc)
    S525_60 = (PAL_M | PAL_60 | NTSC | NTSC_443)
    S625_50 = (PAL | PAL_N | PAL_Nc | SECAM)
    ATSC = (ATSC_8_VSB | ATSC_16_VSB)
    UNKNOWN = 0
    ALL = (S525_60 | S625_50)


class V4l2_Standard(Structure):
    _fields_ = [('index', c_uint32), ('id', V4l2_Std_Id),
                ('name', c_uint8 * 24), ('frameperiod', V4l2_Fract),
                ('framelines', c_uint32), ('reserved', c_uint32 * 4)]


class V4l2_Bt_Timings(Structure):
    _pack_ = True
    _fields_ = [('width', c_uint32), ('height', c_uint32),
                ('interlaced', c_uint32), ('polarities', c_uint32),
                ('pixelclock', c_uint64), ('hfrontporch', c_uint32),
                ('hsync', c_uint32), ('hbackporch', c_uint32),
                ('vfrontporch', c_uint32), ('vsync', c_uint32),
                ('vbackporch', c_uint32), ('il_vfrontporch', c_uint32),
                ('il_vsync', c_uint32), ('il_vbackporch', c_uint32),
                ('standards', c_uint32), ('flags', c_uint32),
                ('picture_aspect', V4l2_Fract), ('cea861_vic', c_uint8),
                ('hdmi_vic', c_uint8), ('reserved', c_uint8 * 46)]


class V4l2_Dv(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (VSYNC_POS_POL, HSYNC_POS_POL) = [1 << x for x in range(2)]
    PROGRESSIVE = 0
    INTERLACED = 1


class V4l2_Dv_Bt_Std(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (CEA861, DMT, CVT, GTF, SDI) = [1 << x for x in range(5)]


class V4l2_Dv_Fl(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (REDUCED_BLANKING, CAN_REDUCE_FPS, REDUCED_FPS, HALF_LINE, IS_CE_VIDEO,
     FIRST_FIELD_EXTRA_LINE, HAS_PICTURE_ASPECT, HAS_CEA861_VIC, HAS_HDMI_VIC,
     CAN_DETECT_REDUCED_FPS) = [1 << x for x in range(10)]


def v4l2_dv_bt_blanking_width(bt: V4l2_Bt_Timings):
    return (bt.hfrontporch + bt.hsync + bt.hbackporch)


def v4l2_dv_bt_frame_width(bt: V4l2_Bt_Timings):
    return (bt.width + v4l2_dv_bt_blanking_width(bt))


def v4l2_dv_bt_blanking_height(bt: V4l2_Bt_Timings):
    return (bt.vfrontporch + bt.vsync + bt.vbackporch + bt.il_vfrontporch +
            bt.il_vsync + bt.il_vbackporch)


def v4l2_dv_bt_frame_height(bt: V4l2_Bt_Timings):
    return (bt.height + v4l2_dv_bt_blanking_height(bt))


class V4l2_Dv_Timings(Structure):
    _pack_ = True
    _fields_ = [('bt', V4l2_Bt_Timings), ('reserved', c_uint32 * 32)]


class V4l2_Dv_Bt(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    D656_1120 = 0


class V4l2_Enum_Dv_Timings(Structure):
    _pack_ = True
    _fields_ = [('index', c_uint32), ('pad', c_uint32),
                ('reserved', c_uint32 * 2), ('timings', V4l2_Dv_Timings)]


class V4l2_Bt_Timings_Cap(Structure):
    _pack_ = True
    _fields_ = [
        ('min_width', c_uint32),
        ('max_width', c_uint32),
        ('min_height', c_uint32),
        ('max_height', c_uint32),
        ('min_pixelclock', c_uint32),
        ('max_pixelclock', c_uint32),
        ('standards', c_uint32),
        ('capabilities', c_uint32),
        ('reserved', c_uint32 * 16),
    ]


class V4l2_Dv_Bt_Cap(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (INTERLACED, PROGRESSIVE, REDUCED_BLANKING,
     CUSTOM) = [1 << x for x in range(4)]


class V4l2_Dv_Timings_Cap(Structure):
    class _u(Union):
        _fields_ = [('bt', V4l2_Bt_Timings), ('raw_data', c_uint32 * 32)]

    _fields_ = [
        ('type', c_uint32),
        ('pad', c_uint32),
        ('reserved', c_uint32 * 2),
        ('_u', _u),
    ]


class V4l2_Input(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8), ('type', c_uint32),
                ('audioset', c_uint32), ('tuner', c_type(V4l2_Tuner_Type)),
                ('std', V4l2_Std_Id), ('status', c_uint32),
                ('capabilities', c_uint32), ('reserved', c_uint32 * 3)]


class V4l2_Input_Type(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (TUNER, CAMERA, TOUCH) = range(3)


class V4l2_In_St(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NO_POWER, NO_SIGNAL, NO_COLOR) = [1 << x for x in range(3)]
    (HFLIP, VFLIP) = [1 << x for x in range(4, 6)]
    (NO_H_LOCK, COLOR_KILL, NO_V_LOCK,
     NO_STD_LOCK) = [1 << x for x in range(8, 12)]
    (NO_SYNC, NO_EQU, NO_CARRIER) = [1 << x for x in range(16, 19)]
    (MACROVISION, NO_ACCESS, VTR) = [1 << x for x in range(24, 27)]


class V4l2_In_Cap(Enum):
    def __str__(self):
        return '{0}'.format(self.value)


#define V4L2_IN_CAP_DV_TIMINGS		0x00000002
#define V4L2_IN_CAP_CUSTOM_TIMINGS	V4L2_IN_CAP_DV_TIMINGS
#define V4L2_IN_CAP_STD			0x00000004
#define V4L2_IN_CAP_NATIVE_SIZE		0x00000008


class V4l2_Output(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8 * 32),
                ('type', c_uint32), ('audioset', c_uint32),
                ('modulator', c_uint32), ('std', V4l2_Std_Id),
                ('capabilities', c_uint32), ('reserved', c_uint32 * 3)]


class V4l2_Output_Type(Enum):
    def __str__(self):
        return '{0}'.format(self.value)


#define V4L2_OUTPUT_TYPE_MODULATOR		1
#define V4L2_OUTPUT_TYPE_ANALOG			2
#define V4L2_OUTPUT_TYPE_ANALOGVGAOVERLAY	3


class V4l2_Out_Cap(Enum):
    def __str__(self):
        return '{0}'.format(self.value)


#define V4L2_OUT_CAP_DV_TIMINGS		0x00000002 /* Supports S_DV_TIMINGS */
#define V4L2_OUT_CAP_CUSTOM_TIMINGS	V4L2_OUT_CAP_DV_TIMINGS /* For compatibility */
#define V4L2_OUT_CAP_STD		0x00000004 /* Supports S_STD */
#define V4L2_OUT_CAP_NATIVE_SIZE	0x00000008 /* Supports setting native size */


class V4l2_Control(Structure):
    _fields_ = [('id', c_uint32), ('value', c_int32)]


class V4l2_Ext_Control(Structure):
    _pack_ = True

    class _u(Union):
        _fields_ = [('value', c_int32), ('value64', c_int64),
                    ('string', POINTER(c_char)), ('p_u8', POINTER(c_uint8)),
                    ('p_u16', POINTER(c_uint16)), ('p_u32', POINTER(c_uint32)),
                    ('p_area', POINTER(V4l2_Area)), ('ptr', POINTER(c_void_p))]

    _fields_ = [
        ('id', c_uint32),
        ('size', c_uint32),
        ('reserved2', c_uint32),
        ('_u', _u),
    ]


class V4l2_Ext_Controls(Structure):
    class _u(Union):
        _fields_ = [('which', c_uint32)]

    _fields_ = [('_u', _u), ('count', c_uint32), ('error_idx', c_uint32),
                ('request_fd', c_uint32), ('reserved', c_uint32),
                ('controls', POINTER(V4l2_Ext_Control))]
