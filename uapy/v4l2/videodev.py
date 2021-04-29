from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.common import *


class Video_Max(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    FRAME = 32
    PLANES = 8


def v4l2_fourcc(a, b, c, d):
    return ord(a) | (ord(b) << 8) | (ord(c) << 16) | (ord(d) << 24)


def v4l2_fourcc_be(a, b, c, d):
    return v4l2_fourcc(a, b, c, d) | (1 << 31)


class V4l2_Field(IntEnum):
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


class V4l2_Buf_Type(IntEnum):
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


class V4l2_Tuner_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (RADIO, ANALOG_TV, DIGITAL_TV, SDR, RF) = range(1, 6)
    ADC = SDR


class V4l2_Memory(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (
        MMAP,
        USERPTR,
        OVERLAY,
        DMABUF,
    ) = range(1, 5)


class V4l2_Colorspace(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, SMPTE170M, SMPTE240M, REC709, BT878, C470_SYSTEM_M,
     C470_SYSTEM_BG, JPEG, SRGB, OPRGB, BT2020, RAW, DCI_P3) = range(13)


def v4l2_map_colorspace_default(is_sdtv, is_hdtv):
    return ((V4l2_Colorspace.SRGB, V4l2_Colorspace.REC709)[is_hdtv],
            V4l2_Colorspace.SMPTE170M)[is_sdtv]


class V4l2_Xfer_Func(IntEnum):
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


class V4l2_Ycbcr_Enc(IntEnum):
    def __c_type__(IntEnum):
        return c_uint32

    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, Y601, Y709, XV601, XV709, SYCC, BT2020, BT2020_CONST_LUM,
     SMPTE240M) = range(9)


class V4l2_Hsv_Enc(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (H180, H256) = range(128, 130)


def v4l2_map_ycbcr_enc_default(colsp):
    return (((V4l2_Ycbcr_Enc.Y601,
              V4l2_Ycbcr_Enc.SMPTE240M)[colsp == V4l2_Colorspace.SMPTE240M],
             V4l2_Ycbcr_Enc.BT2020)[colsp == V4l2_Colorspace.BT2020],
            V4l2_Ycbcr_Enc.Y709)[colsp == V4l2_Colorspace.REC709
                                 or colsp == V4l2_Colorspace.DCI_P3]


class V4l2_Quantization(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DEFAULT, FULL_RANGE, LIM_RANGE) = range(3)


def v4l2_map_quantization_default(is_rgb_or_hsv, colsp, ycbcr_enc):
    return ((V4l2_Quantization.LIM_RANGE,
             V4l2_Quantization.FULL_RANGE)[((is_rgb_or_hsv) or
                                            (colsp) == V4l2_Colorspace.JPEG)],
            V4l2_Quantization.LIM_RANGE)[((is_rgb_or_hsv) and
                                          (colsp) == V4l2_Colorspace.BT2020)]


class V4l2_Priority(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (
        UNSET,
        BACKGROUND,
        INTERACTIVE,
        RECORD,
    ) = range(0, 4)
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


class V4l2_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    HIGHQUALITY = 0 << 1


class V4l2_Cap(IntEnum):
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
                ('pixelformat', c_uint32), ('field', c_uint32),
                ('bytesperline', c_uint32), ('sizeimage', c_uint32),
                ('colorspace', c_uint32), ('priv', c_uint32)]


class V4l2_Fmt_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (COMPRESSED, EMULATED, CONTINUOUS_BYTESTREAM,
     DYN_RESOLUTION) = [1 << x for x in range(4)]


class V4l2_Pix_Format(Structure):
    class _u(Union):
        _fields_ = [
            ('ycbcr_enc', c_uint32),
            ('hsv_enc', c_uint32),
        ]

    _fields_ = [
        ('width', c_uint32),
        ('height', c_uint32),
        ('pixelformat', c_uint32),
        ('field', c_uint32),
        ('bytesperline', c_uint32),
        ('sizeimage', c_uint32),
        ('colorspace', c_uint32),
        ('priv', c_uint32),
        ('flags', c_uint32),
        ('_u', _u),
        ('quantization', c_uint32),
        ('xfer_func', c_uint32),
    ]


class V4l2_Pix_Fmt(IntEnum):
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


class V4l2_Sdr_Fmt(IntEnum):
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


class V4l2_Tch_Fmt(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    DELTA_TD16 = v4l2_fourcc('T', 'D', '1', '6')
    DELTA_TD08 = v4l2_fourcc('T', 'D', '0', '8')
    TU16 = v4l2_fourcc('T', 'U', '1', '6')
    TU08 = v4l2_fourcc('T', 'U', '0', '8')


class V4l2_Meta_Fmt(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    VSP1_HGO = v4l2_fourcc('V', 'S', 'P', 'H')
    VSP1_HGT = v4l2_fourcc('V', 'S', 'P', 'T')
    UVC = v4l2_fourcc('U', 'V', 'C', 'H')
    D4XX = v4l2_fourcc('D', '4', 'X', 'X')
    VIVID = v4l2_fourcc('V', 'I', 'V', 'D')


class V4l2_Fmtdesc(Structure):
    _fields_ = [('index', c_uint32), ('type', c_uint32), ('flags', c_uint32),
                ('description', c_uint8 * 32), ('pixelformat', c_uint32),
                ('mbus_code', c_uint32), ('reserved', c_uint32 * 3)]


class V4l2_Frmsizetypes(IntEnum):
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


class V4l2_Frmivaltypes(IntEnum):
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


class V4l2_Tc_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (T24FPS, T25FPS, T30FPS, T50FPS, T60FPS) = range(1, 6)


class V4l2_Tc_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DROPFRAME, COLORFRAME) = [1 << x for x in range(2)]


class V4l2_Tc_Userbits(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    field = 0x000C
    USERDEFINED = 0x0000
    T8BITCHARS = 0x0008


class V4l2_Jpeg_Marker(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DHT, DQT, DRI, COM, APP) = [1 << x for x in range(3, 8)]


class V4l2_Jpegcompression(Structure):
    _fields_ = [('quality', c_int), ('APPn', c_int), ('APP_len', c_int),
                ('APP_data', c_char * 60), ('COM_len', c_int),
                ('COM_data', c_char * 60), ('jpeg_markers', c_uint32)]


class V4l2_Requestbuffers(Structure):
    _fields_ = [('count', c_uint32), ('type', c_uint32), ('memory', c_uint32),
                ('capabilities', c_uint32), ('reserved', c_uint32)]


class V4l2_Buf_Cap_Supports(IntEnum):
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


class V4l2_Buf_Flag(IntEnum):
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
    _fields_ = [('type', c_uint32), ('index', c_uint32), ('plane', c_uint32),
                ('flags', c_uint32), ('fd', c_int32),
                ('reserved', c_uint32 * 11)]


class V4l2_Framebuffer(Structure):
    _fields_ = [('capability', c_uint32), ('flags', c_uint32),
                ('base', c_void_p), ('fmt', V4l2_Fmt)]


class V4l2_Fbuf_Cap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (EXTERNOVERLAY, CHROMAKEY, LIST_CLIPPING, BITMAP_CLIPPING, LOCAL_ALPHA,
     GLOBAL_ALPHA, LOCAL_INV_ALPHA,
     SRC_CHROMAKEY) = [1 << x for x in range(8)]


class V4l2_Fbuf_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PRIMARY, OVERLAY, CHROMAKEY, LOCAL_ALPHA, GLOBAL_ALPHA, LOCAL_INV_ALPHA,
     SRC_CHROMAKEY) = [1 << x for x in range(7)]


class V4l2_Clip(Structure):
    _fields_ = [('c', V4l2_Rect)]


V4l2_Clip._fields_.append(('next', POINTER(V4l2_Clip)))


class V4l2_Window(Structure):
    _fields_ = [('w', V4l2_Rect), ('field', c_uint32), ('chromakey', c_uint32),
                ('clips', POINTER(V4l2_Clip)), ('clipcount', c_uint32),
                ('bitmap', c_void_p), ('global_alpha', c_uint8)]


class V4l2_Captureparm(Structure):
    _fields_ = [('capability', c_uint32), ('capturemode', c_uint32),
                ('timeperframe', V4l2_Fract), ('extendedmode', c_uint32),
                ('readbuffers', c_uint32), ('reserved', c_uint32 * 4)]


class V4l2_Outputparm(Structure):
    _fields_ = [('capability', c_uint32), ('outputmode', c_uint32),
                ('timeperframe', V4l2_Fract), ('extendedmode', c_uint32),
                ('writebuffers', c_uint32), ('reserved', c_uint32 * 4)]


class V4l2_Cropcap(Structure):
    _fields_ = [
        ('type', c_uint32),
        ('bounds', V4l2_Rect),
        ('defrect', V4l2_Rect),
        ('pixelaspect', V4l2_Fract),
    ]


class V4l2_Crop(Structure):
    _fields_ = [('type', c_uint32), ('c', V4l2_Rect)]


class V4l2_Selection(Structure):
    _fields_ = [('type', c_uint32), ('target', c_uint32), ('flags', c_uint32),
                ('r', V4l2_Rect), ('reserved', c_uint32)]


V4l2_Std_Id = c_uint64


class V4l2_Std(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PAL_B, PAL_B1, PAL_G, PAL_H, PAL_I, PAL_D, PAL_D1, PAL_K, PAL_M, PAL_N,
     PAL_Nc, PAL_60, NTSC_M, NTSC_M_JP, NTSC_443, NTSC_M_KR, SECAM_B, SECAM_D,
     SECAM_G, SECAM_H, SECAM_K, SECAM_K1, SECAM_L, SECAM_LC, ATSC_8_VSB,
     ATSC_16_VSB) = [V4l2_Std_Id(1 << x).value for x in range(26)]

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
    _pack_ = True


class V4l2_Dv(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (VSYNC_POS_POL, HSYNC_POS_POL) = [1 << x for x in range(2)]


class V4l2_Dv_Bt_Std(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (CEA861, DMT, CVT, GTF, SDI) = [1 << x for x in range(5)]


class V4l2_Dv_Fl(IntEnum):
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
    _fields_ = [('bt', V4l2_Bt_Timings), ('reserved', c_uint32 * 32)]
    _pack_ = True


class V4l2_Dv_Bt(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    D656_1120 = 0


class V4l2_Enum_Dv_Timings(Structure):
    _fields_ = [('index', c_uint32), ('pad', c_uint32),
                ('reserved', c_uint32 * 2), ('timings', V4l2_Dv_Timings)]
    _pack_ = True


class V4l2_Bt_Timings_Cap(Structure):
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
    _pack_ = True


class V4l2_Dv_Bt_Cap(IntEnum):
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
                ('audioset', c_uint32), ('tuner', c_uint32),
                ('std', V4l2_Std_Id), ('status', c_uint32),
                ('capabilities', c_uint32), ('reserved', c_uint32 * 3)]


class V4l2_Input_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (TUNER, CAMERA, TOUCH) = range(3)


class V4l2_In_St(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NO_POWER, NO_SIGNAL, NO_COLOR) = [1 << x for x in range(3)]
    (HFLIP, VFLIP) = [1 << x for x in range(4, 6)]
    (NO_H_LOCK, COLOR_KILL, NO_V_LOCK,
     NO_STD_LOCK) = [1 << x for x in range(8, 12)]
    (NO_SYNC, NO_EQU, NO_CARRIER) = [1 << x for x in range(16, 19)]
    (MACROVISION, NO_ACCESS, VTR) = [1 << x for x in range(24, 27)]


class V4l2_In_Cap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DV_TIMINGS, STD, NATIVE_SIZE) = [1 << x for x in range(1, 4)]
    CUSTOM_TIMINGS = DV_TIMINGS


class V4l2_Output(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8 * 32),
                ('type', c_uint32), ('audioset', c_uint32),
                ('modulator', c_uint32), ('std', V4l2_Std_Id),
                ('capabilities', c_uint32), ('reserved', c_uint32 * 3)]


class V4l2_Output_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (MODULATOR, ANALOG, ANALOGVGAOVERLAY) = range(1, 4)


class V4l2_Out_Cap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DV_TIMINGS, STD, NATIVE_SIZE) = [1 << x for x in range(1, 4)]
    CUSTOM_TIMINGS = DV_TIMINGS


class V4l2_Control(Structure):
    _fields_ = [('id', c_uint32), ('value', c_int32)]


class V4l2_Ext_Control(Structure):
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
    _pack_ = True


class V4l2_Ext_Controls(Structure):
    class _u(Union):
        _fields_ = [('which', c_uint32)]

    _fields_ = [('_u', _u), ('count', c_uint32), ('error_idx', c_uint32),
                ('request_fd', c_uint32), ('reserved', c_uint32),
                ('controls', POINTER(V4l2_Ext_Control))]


def v4l2_ctrl_id2which(id):
    c = 0x0fff0000
    return id & c_ulong(c).value


def v4l2_ctrl_driver_priv(id):
    return (((id) & 0xffff) >= 0x1000)


class V4l2_Ctrl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ID_MASK = 0x0fffffff
    MAX_DIMS = 4
    WHICH_CUR_VAL = 0
    WHICH_DEF_VAL = 0x0f000000
    WHICH_REQUEST_VAL = 0x0f010000


class V4l2_Ctrl_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (INTEGER, BOOLEAN, MENU, BUTTON, INTEGER64, CTRL_CLASS, STRING,
     BITMASK) = range(1, 9)
    COMPOUND_TYPES = 0x0100
    (U8, U16, U32) = [(1 << 8) + x for x in range(3)]
    AREA = 0x0106


class V4l2_Queryctrl(Structure):
    _fields_ = [('id', c_uint32), ('type', c_uint32), ('name', c_uint8 * 32),
                ('minimum', c_int32), ('maximum', c_int32), ('step', c_int32),
                ('default_value', c_int32), ('flags', c_uint32),
                ('reserved', c_uint32 * 2)]


class V4l2_Query_Ext_Ctrl(Structure):
    _fields_ = [('id', c_uint32), ('type', c_uint32), ('name', c_char * 32),
                ('minimum', c_int64), ('maximum', c_int64), ('step', c_uint64),
                ('default_value', c_int64), ('flags', c_uint32),
                ('elem_size', c_uint32), ('elems', c_uint32),
                ('nr_of_dims', c_uint32),
                ('dims', c_uint32 * V4l2_Ctrl.MAX_DIMS),
                ('reserved', c_uint32 * 32)]


class V4l2_Querymenu(Structure):
    class _u(Union):
        _fields_ = [('name', c_uint8 * 32), ('value', c_int64)]

    _fields_ = [('id', c_uint32), ('index', c_uint32), ('_u', _u),
                ('reserved', c_uint32)]
    _pack_ = True


class V4l2_Ctrl_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DISABLED, GRABBED, READ_ONLY, UPDATE, INACTIVE, SLIDER, WRITE_ONLY,
     VOLATILE, HAS_PAYLOAD, EXECUTE_ON_WRITE,
     MODIFY_LAYOUT) = [1 << x for x in range(11)]

    NEXT_COMPOUND = 0x40000000
    NEXT_CTRL = 0x80000000


class V4l2_Cid(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MAX_CTRLS = 0x400
    PRIVATE_BASE = 0x08000000


class V4l2_Tuner(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8 * 32),
                ('type', c_uint32), ('capability', c_uint32),
                ('rangelow', c_uint32), ('rangehigh', c_uint32),
                ('rxsubchans', c_uint32), ('audmode', c_uint32),
                ('signal', c_int32), ('afc', c_int32),
                ('reserved', c_uint32 * 4)]


class V4l2_Modulator(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8),
                ('capability', c_uint32), ('rangelow', c_uint32),
                ('rangehigh', c_uint32), ('txsubchans', c_uint32),
                ('type', c_uint32), ('reserved', c_uint32 * 3)]


class V4l2_Tuner_Cap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (LOW, NORM, HWSEEK_BOUNDED, HWSEEK_WRAP, STEREO, LANG2, LANG1, RDS,
     RDS_BLOCK_IO, RDS_CONTROLS, FREQ_BANDS, HWSEEK_PROG_LIM,
     T1HZ) = [1 << x for x in range(13)]
    SAP = (1 << 5)


class V4l2_Tuner_Sub(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (MONO, STEREO, LANG2, LANG1, RDS) = [1 << x for x in range(5)]
    SAP = (1 << 2)


class V4l2_Tuner_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (MONO, STEREO, LANG2, LANG1, LANG1_LANG2) = range(5)

    SAP = 0x0002


class V4l2_Frequency(Structure):
    _fields_ = [
        ('tuner', c_uint32),
        ('type', c_uint32),
        ('frecuency', c_uint32),
        ('reserved', c_uint32 * 8),
    ]


class V4l2_Band_Modulation(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (VSB, FM, AM) = [1 << x for x in range(3)]


class V4l2_Frequency_Band(Structure):
    _fields_ = [
        ('tuner', c_uint32),
        ('type', c_uint32),
        ('index', c_uint32),
        ('capability', c_uint32),
        ('rangelow', c_uint32),
        ('rangehigh', c_uint32),
        ('modulation', c_uint32),
        ('reserved', c_uint32 * 9),
    ]


class V4l2_Hw_Freq_Seek(Structure):
    _fields_ = [('tuner', c_uint32), ('type', c_uint32),
                ('seek_upward', c_uint32), ('wrap_around', c_uint32),
                ('spacing', c_uint32), ('rangelow', c_uint32),
                ('rangehigh', c_uint32), ('reserved', c_uint32 * 5)]


class V4l2_Rds_Data(Structure):
    _fields_ = [('lsb', c_uint8), ('msb', c_uint8), ('block', c_uint8)]
    _pack_ = True


class V4l2_Rds_Block(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MSK = 0x7
    (A, B, C, D, C_ALT) = range(5)
    INVALID = 7
    (CORRECTED, ERROR) = [1 << x for x in range(6, 8)]


class V4l2_Audio(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8),
                ('capability', c_uint32), ('mode', c_uint32),
                ('reserved', c_uint32 * 2)]


class V4l2_Audcap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (STEREO, AVL) = [1 << x for x in range(2)]


class V4l2_Audmode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    AVL = 0x00001


class V4l2_Audioout(Structure):
    _fields_ = [('index', c_uint32), ('name', c_uint8),
                ('capability', c_uint32), ('mode', c_uint32),
                ('reserved', c_uint32 * 2)]


class V4l2_Enc_Idx_Frame(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (I, P, B) = range(3)
    MASK = (0xf)


class V4l2_Enc_Idx_Entry(Structure):
    _fields_ = [('offset', c_uint64), ('pts', c_uint64), ('length', c_uint32),
                ('flags', c_uint32), ('reserved', c_uint32 * 2)]


class V4l2_Enc_Idx(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ENTRIES = 64


class V4l2_Enc_Idx(Structure):
    _fields_ = [('entries', c_uint32), ('entries_cap', c_uint32),
                ('reserved', c_uint32 * 4),
                ('entry', V4l2_Enc_Idx_Entry * V4l2_Enc_Idx.ENTRIES)]


class V4l2_Enc_Cmd(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (START, STOP, PAUSE, RESUME) = range(4)
    STOP_AT_GOP_END = (1 << 0)


class V4l2_Encoder_Cmd(Structure):
    class _u(Union):
        class _s(Structure):
            _fields_ = [
                ('data', c_uint32 * 8),
            ]

        _fields_ = [
            ('raw', _s),
        ]

    _fields_ = [('cmd', c_uint32), ('flags', c_uint32), ('_u', _u)]


class V4l2_Dec_Cmd(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (START, STOP, PAUSE, RESUME, FLUSH) = range(5)

    (START_MUTE_AUDIO, PAUSE_TO_BLACK, STOP_TO_BLACK) = [(1 << 0)] * 3
    STOP_IMMEDIATELY = (1 << 1)


class V4l2_Dec_Start_Fmt(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    NONE = 0
    GOP = 1


class V4l2_Decoder_Cmd(Structure):
    class _u(Union):
        class _stop(Structure):
            _fields_ = [
                ('pts', c_uint64),
            ]

        class _start(Structure):
            _fields_ = [
                ('speed', c_int32),
                ('format', c_uint32),
            ]

        class _raw(Structure):
            _fields_ = [
                ('data', c_uint32 * 16),
            ]

        _fields_ = [('stop', _stop), ('start', _start), ('raw', _raw)]

    _fields_ = [('cmd', c_uint32), ('flags', c_uint32), ('_u', _u)]


class V4l2_Vbi(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    UNSYNC = (1 << 0)
    INTERLACED = (1 << 1)
    ITU_525_F1_START = (1)
    ITU_525_F2_START = (264)
    ITU_625_F1_START = (1)
    ITU_625_F2_START = (314)


class V4l2_Vbi_Format(Structure):
    _fields_ = [('sampling_rate', c_uint32), ('offset', c_uint32),
                ('samples_per_line', c_uint32), ('sample_format', c_uint32),
                ('start', c_int32 * 2), ('count', c_uint32 * 2),
                ('flags', c_uint32), ('reserved', c_uint32 * 2)]


class V4l2_Sliced_Vbi_Format(Structure):
    _fields_ = [('service_set', c_uint16),
                ('service_lines', c_uint16 * 2 * 24), ('io_size', c_uint32),
                ('reserved', c_uint32 * 2)]


class V4l2_Sliced(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    TELETEXT_B = 0x0001
    VPS = 0x0400
    CAPTION_525 = 0x1000
    WSS_625 = 0x4000
    VBI_525 = CAPTION_525
    VBI_625 = (TELETEXT_B | VPS | WSS_625)


class V4l2_Sliced_Vbi_Cap(Structure):
    _fields_ = [('service_set', c_uint16),
                ('service_lines', c_uint16 * 2 * 24), ('type', c_uint32),
                ('reserved', c_uint32 * 3)]


class V4l2_Sliced_Vbi_Data(Structure):
    _fields_ = [
        ('id', c_uint32),
        ('field', c_uint32),
        ('line', c_uint32),
        ('reserved', c_uint32),
        ('data', c_uint8 * 48),
    ]


class V4l2_Mpeg_Vbi_Ivtv(IntEnum):
    def __c_type__():
        return c_uint8

    def __str__(self):
        return '{0}'.format(self.value)

    TELETEXT_B = 1
    CAPTION_525 = 4
    WSS_625 = 5
    VPS = 7


class V4l2_Mpeg_Vbi_Ivtv_Magic(Enum):
    def __str__(self):
        return '{0}'.format(self.value)

    M0 = "itv0"
    M1 = "ITV0"


class V4l2_Mpeg_Vbi_Itv0_Line(Structure):
    _fields_ = [('id', c_uint8), ('data', c_uint8 * 42)]
    _pack_ = True


class V4l2_Mpeg_Vbi_Itv0(Structure):
    class _s(LittleEndianStructure):
        _fields_ = [('linemask', c_uint32)]

    _fields_ = [('_s', _s * 2), ('line', V4l2_Mpeg_Vbi_Itv0_Line * 35)]
    _pack_ = True


class V4l2_Mpeg_Vbi_ITV0(Structure):
    _fields_ = [('line', V4l2_Mpeg_Vbi_Itv0_Line * 35)]
    _pack_ = True


class V4l2_Mpeg_Vbi_Fmt_Ivtv(Structure):
    class _u(Union):
        _fields_ = [('itv0', V4l2_Mpeg_Vbi_Itv0), ('ITV0', V4l2_Mpeg_Vbi_ITV0)]

    _fields_ = [('magic', c_uint8 * 4), ('_u', _u)]
    _pack_ = True


class V4l2_Plane_Pix_Format(Structure):
    _fields_ = [('sizeimage', c_uint32), ('bytesperline', c_uint32),
                ('reserved', c_uint16 * 6)]
    _pack_ = True


class V4l2_Pix_Format_Mplane(Structure):
    class _u(Union):
        _fields_ = [('ycbcr_enc', c_uint8), ('hsv_enc', c_uint8)]

    _fields_ = [('width', c_uint32), ('height', c_uint32),
                ('pixelformat', c_uint32), ('field', c_uint32),
                ('colorspace', c_uint32),
                ('plane_fmt',
                 V4l2_Plane_Pix_Format * Video_Max.PLANES),
                ('num_planes', c_uint8), ('flags', c_uint8), ('_u', _u),
                ('quantization', c_uint8), ('xfer_func', c_uint8),
                ('reserved', c_uint8 * 7)]

    _pack_ = True


class V4l2_Sdr_Format(Structure):
    _fields_ = [('pixelformat', c_uint32), ('buffersize', c_uint32),
                ('reserved', c_uint8 * 24)]
    _pack_ = True


class V4l2_Meta_Format(Structure):
    _fields_ = [('dataformat', c_uint32), ('buffersize', c_uint32)]
    _pack_ = True


class V4l2_Format(Structure):
    class _fmt(Union):
        _fields_ = [
            ('pix', V4l2_Pix_Format), ('pix_mp', V4l2_Pix_Format_Mplane),
            ('win', V4l2_Window), ('vbi', V4l2_Vbi_Format),
            ('sliced', V4l2_Sliced_Vbi_Format), ('sdr', V4l2_Sdr_Format),
            ('meta', V4l2_Meta_Format), ('raw_data', c_uint8 * 200)
        ]

    _fields_ = [('type', c_uint32), ('fmt', _fmt)]


class V4l2_Streamparm(Structure):
    class _parm(Union):
        _fields_ = [('capture', V4l2_Captureparm), ('output', V4l2_Outputparm),
                    ('raw_data', c_uint8 * 200)]

    _fields_ = [('type', c_uint32), ('parm', _parm)]


class V4l2_Event(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ALL, VSYNC, EOS, CTRL, FRAME_SYNC, SOURCE_CHANGE, MOTION_DET) = range(7)

    PRIVATE_START = 0x08000000


class V4l2_Event_Vsync(Structure):
    _fields_ = [('field', c_uint32)]
    _pack_ = True


class V4l2_Event_Ctrl_Ch(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (VALUE, FLAGS, RANGE) = [1 << x for x in range(3)]


class V4l2_Event_Ctrl(Structure):
    class _u(Union):
        _fields_ = [('value', c_int32), ('value64', c_int64)]

    _fields_ = [('changes', c_uint32), ('type', c_uint32), ('_u', _u),
                ('flags', c_uint32), ('minimum', c_int32),
                ('maximum', c_int32), ('step', c_int32),
                ('default_value', c_int32)]


class V4l2_Event_Frame_Sync(Structure):
    _fields_ = [('frame_sequence', c_uint32)]


class V4l2_Event_Src_Ch(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    RESOLUTION = (1 << 0)


class V4l2_Event_Src_Change(Structure):
    _fields_ = [('changes', c_uint32)]


class V4l2_Event_Md_Fl_Have(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    FRAME_SEQ = (1 << 0)


class V4l2_Event_Motion_Det(Structure):
    _fields_ = [('flags', c_uint32), ('frame_sequence', c_uint32),
                ('region_mask', c_uint32)]


class V4l2_Event(Structure):
    class timespec(Structure):
        _fields_ = [('tv_sec', c_long), ('tv_nsec', c_long)]

    class _u(Union):
        _fields_ = [('vsync', V4l2_Event_Vsync), ('ctrl', V4l2_Event_Ctrl),
                    ('frame_sync', V4l2_Event_Frame_Sync),
                    ('src_change', V4l2_Event_Src_Change),
                    ('motion_det', V4l2_Event_Motion_Det),
                    ('data', c_uint8 * 64)]

    _fields_ = [('type', c_uint32), ('u', _u), ('pending', c_uint32),
                ('sequence', c_uint32), ('timestamp', timespec),
                ('id', c_uint32), ('reserved', c_uint32 * 8)]


class V4l2_Event_Sub_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SEND_INITIAL, ALLOW_FEEDBACK) = [1 << x for x in range(2)]


class V4l2_Event_Subscription(Structure):
    _fields_ = [
        ('type', c_uint32),
        ('id', c_uint32),
        ('flags', c_uint32),
        ('reserved', c_uint32 * 5),
    ]


class V4l2_Chip_Match(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (BRIDGE, I2C_DRIVER, I2C_ADDR, AC97, SUBDEV) = range(5)
    HOST = BRIDGE


class V4l2_Dbg_Match(Structure):
    class _u(Union):
        _fields_ = [('addr', c_uint32), ('name', c_char * 32)]

    _fields_ = [('type', c_uint32), ('_u', _u)]
    _pack_ = True


class V4l2_Dbg_Register(Structure):
    _fields_ = [('match', V4l2_Dbg_Match), ('size', c_uint32),
                ('reg', c_uint64), ('val', c_uint64)]
    _pack_ = True


class V4l2_Chip_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (READABLE, WRITABLE) = range(2)


class V4l2_Dbg_Chip_Info(Structure):
    _fields_ = [('match', V4l2_Dbg_Match), ('name', c_char * 32),
                ('flags', c_uint32), ('reserved', c_uint32 * 32)]
    _pack_ = True


class V4l2_Create_Buffers(Structure):
    _fields_ = [('index', c_uint32), ('count', c_uint32), ('memory', c_uint32),
                ('format', V4l2_Format), ('capabilities', c_uint32),
                ('reserved', c_uint32 * 7)]


class Vidioc(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    QUERYCAP = ior('V', 0, V4l2_Capability)
    ENUM_FMT = iow('V', 2, V4l2_Fmtdesc)
    G_FMT = iowr('V', 4, V4l2_Format)
    S_FMT = iowr('V', 5, V4l2_Format)
    REQBUFS = iowr('V', 8, V4l2_Requestbuffers)
    QUERYBUF = iowr('V', 9, V4l2_Buffer)
    G_FBUF = ior('V', 10, V4l2_Framebuffer)
    S_FBUF = iow('V', 11, V4l2_Framebuffer)
    OVERLAY = iow('V', 14, c_int)
    QBUF = iowr('V', 15, V4l2_Buffer)
    EXPBUF = iowr('V', 16, V4l2_Exportbuffer)
    DQBUF = iowr('V', 17, V4l2_Buffer)
    STREAMON = iow('V', 18, c_int)
    STREAMOFF = iow('V', 19, c_int)
    G_PARM = iowr('V', 21, V4l2_Streamparm)
    S_PARM = iowr('V', 22, V4l2_Streamparm)
    G_STD = ior('V', 23, V4l2_Std_Id)
    S_STD = iow('V', 24, V4l2_Std_Id)
    ENUMSTD = iowr('V', 25, V4l2_Standard)
    ENUMINPUT = iowr('V', 26, V4l2_Input)
    G_CTRL = iowr('V', 27, V4l2_Control)
    S_CTRL = iowr('V', 28, V4l2_Control)
    G_TUNER = iowr('V', 29, V4l2_Tuner)
    S_TUNER = iow('V', 30, V4l2_Tuner)
    G_AUDIO = ior('V', 33, V4l2_Audio)
    S_AUDIO = iow('V', 34, V4l2_Audio)
    QUERYCTRL = iowr('V', 36, V4l2_Queryctrl)
    QUERYMENU = iowr('V', 37, V4l2_Querymenu)
    G_INPUT = ior('V', 38, c_int)
    S_INPUT = iowr('V', 39, c_int)
    G_EDID = iowr('V', 40, V4l2_Edid)
    S_EDID = iowr('V', 41, V4l2_Edid)
    G_OUTPUT = ior('V', 46, c_int)
    S_OUTPUT = iowr('V', 47, c_int)
    ENUMOUTPUT = iowr('V', 48, V4l2_Output)
    G_AUDOUT = ior('V', 49, V4l2_Audioout)
    S_AUDOUT = iow('V', 50, V4l2_Audioout)
    G_MODULATOR = iowr('V', 54, V4l2_Modulator)
    S_MODULATOR = iow('V', 55, V4l2_Modulator)
    G_FREQUENCY = iowr('V', 56, V4l2_Frequency)
    S_FREQUENCY = iow('V', 57, V4l2_Frequency)
    CROPCAP = iowr('V', 58, V4l2_Cropcap)
    G_CROP = iowr('V', 59, V4l2_Crop)
    S_CROP = iow('V', 60, V4l2_Crop)
    G_JPEGCOMP = ior('V', 61, V4l2_Jpegcompression)
    S_JPEGCOMP = iow('V', 62, V4l2_Jpegcompression)
    QUERYSTD = ior('V', 63, V4l2_Std_Id)
    TRY_FMT = iowr('V', 64, V4l2_Format)
    ENUMAUDIO = iowr('V', 65, V4l2_Audio)
    ENUMAUDOUT = iowr('V', 66, V4l2_Audioout)
    G_PRIORITY = ior('V', 67, c_uint32)
    S_PRIORITY = iow('V', 68, c_uint32)
    G_SLICED_VBI_CAP = iowr('V', 69, V4l2_Sliced_Vbi_Cap)
    LOG_STATUS = io('V', 70)
    G_EXT_CTRLS = iowr('V', 71, V4l2_Ext_Controls)
    S_EXT_CTRLS = iowr('V', 72, V4l2_Ext_Controls)
    TRY_EXT_CTRLS = iowr('V', 73, V4l2_Ext_Controls)
    ENUM_FRAMESIZES = iowr('V', 74, V4l2_Frmsizeenum)
    ENUM_FRAMEINTERVALS = iowr('V', 75, V4l2_Frmivalenum)
    G_ENC_INDEX = ior('V', 76, V4l2_Enc_Idx)
    ENCODER_CMD = iowr('V', 77, V4l2_Encoder_Cmd)
    TRY_ENCODER_CMD = iowr('V', 78, V4l2_Encoder_Cmd)
    DBG_S_REGISTER = iow('V', 79, V4l2_Dbg_Register)
    DBG_G_REGISTER = iowr('V', 80, V4l2_Dbg_Register)
    S_HW_FREQ_SEEK = iow('V', 82, V4l2_Hw_Freq_Seek)
    S_DV_TIMINGS = iowr('V', 87, V4l2_Dv_Timings)
    G_DV_TIMINGS = iowr('V', 88, V4l2_Dv_Timings)
    DQEVENT = ior('V', 89, V4l2_Event)
    SUBSCRIBE_EVENT = iow('V', 90, V4l2_Event_Subscription)
    UNSUBSCRIBE_EVENT = iow('V', 91, V4l2_Event_Subscription)
    CREATE_BUFS = iowr('V', 92, V4l2_Create_Buffers)
    PREPARE_BUF = iowr('V', 93, V4l2_Buffer)
    G_SELECTION = iowr('V', 94, V4l2_Selection)
    S_SELECTION = iowr('V', 95, V4l2_Selection)
    DECODER_CMD = iowr('V', 96, V4l2_Decoder_Cmd)
    TRY_DECODER_CMD = iowr('V', 97, V4l2_Decoder_Cmd)
    ENUM_DV_TIMINGS = iowr('V', 98, V4l2_Enum_Dv_Timings)
    QUERY_DV_TIMINGS = ior('V', 99, V4l2_Dv_Timings)
    DV_TIMINGS_CAP = iowr('V', 100, V4l2_Dv_Timings_Cap)
    ENUM_FREQ_BANDS = iowr('V', 101, V4l2_Frequency_Band)
    DBG_G_CHIP_INFO = iowr('V', 102, V4l2_Dbg_Chip_Info)
    QUERY_EXT_CTRL = iowr('V', 103, V4l2_Query_Ext_Ctrl)


class BASE_VIDIOC(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    PRIVATE = 192