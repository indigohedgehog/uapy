from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.common import *


class Pulse(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    BIT = 0x01000000
    MASK = 0x00FFFFFF


class Lirc_Mode2(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    SPACE = 0x00000000
    PULSE = 0x01000000
    FREQUENCY = 0x02000000
    TIMEOUT = 0x03000000
    MASK = 0xFF000000


class Lirc_Value(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MASK = 0x00FFFFFF


def lirc_space(val):
    return (((val) & Lirc_Value.MASK) | Lirc_Mode2.SPACE)


def lirc_pulse(val):
    return (((val) & Lirc_Value.MASK) | Lirc_Mode2.PULSE)


def lirc_frequency(val):
    return (((val) & Lirc_Value.MASK) | Lirc_Mode2.FREQUENCY)


def lirc_timeout(val):
    return (((val) & Lirc_Value.MASK) | Lirc_Mode2.TIMEOUT)


def lirc_value(val):
    return ((val) & Lirc_Value.MASK)


def lirc_mode2(val):
    return ((val) & Lirc_Mode2.MASK)


def lirc_is_space(val):
    return (lirc_mode2(val) == Lirc_Mode2.SPACE)


def lirc_is_pulse(val):
    return (lirc_mode2(val) == Lirc_Mode2.PULSE)


def lirc_is_frequency(val):
    return (lirc_mode2(val) == Lirc_Mode2.FREQUENCY)


def lirc_is_timeout(val):
    return (lirc_mode2(val) == Lirc_Mode2.TIMEOUT)


lirc_t = int


def lirc_mode2send(x):
    return (x)


def lirc_send2mode(x):
    return (x)


def lirc_mode2rec(x):
    return ((x) << 16)


def lirc_rec2mode(x):
    return ((x) >> 16)


class Lirc_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (RAW, PULSE, MODE2, SCANCODE, LIRCCODE) = [1 << x for x in range(5)]


class Lirc_Can(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    SEND_RAW = lirc_mode2send(Lirc_Mode.RAW)
    SEND_PULSE = lirc_mode2send(Lirc_Mode.PULSE)
    SEND_MODE2 = lirc_mode2send(Lirc_Mode.MODE2)
    SEND_LIRCCODE = lirc_mode2send(Lirc_Mode.LIRCCODE)
    SEND_MASK = 0x0000003f
    SET_SEND_CARRIER = 0x00000100
    SET_SEND_DUTY_CYCLE = 0x00000200
    SET_TRANSMITTER_MASK = 0x00000400
    REC_RAW = lirc_mode2rec(Lirc_Mode.RAW)
    REC_PULSE = lirc_mode2rec(Lirc_Mode.PULSE)
    REC_MODE2 = lirc_mode2rec(Lirc_Mode.MODE2)
    REC_SCANCODE = lirc_mode2rec(Lirc_Mode.SCANCODE)
    REC_LIRCCODE = lirc_mode2rec(Lirc_Mode.LIRCCODE)
    REC_MASK = lirc_mode2rec(SEND_MASK)
    SET_REC_CARRIER = (SET_SEND_CARRIER << 16)
    SET_REC_DUTY_CYCLE = (SET_SEND_DUTY_CYCLE << 16)
    SET_REC_DUTY_CYCLE_RANGE = 0x40000000
    SET_REC_CARRIER_RANGE = 0x80000000
    GET_REC_RESOLUTION = 0x20000000
    SET_REC_TIMEOUT = 0x10000000
    SET_REC_FILTER = 0x08000000
    MEASURE_CARRIER = 0x02000000
    USE_WIDEBAND_RECEIVER = 0x04000000
    NOTIFY_DECODE = 0x01000000


def lirc_can_send(x):
    return ((x) & Lirc_Can.SEND_MASK)


def lirc_can_rec(x):
    return ((x) & Lirc_Can.REC_MASK)


class Lirc(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    GET_FEATURES = ior('i', 0x00000000, c_uint32)
    GET_SEND_MODE = ior('i', 0x00000001, c_uint32)
    GET_REC_MODE = ior('i', 0x00000002, c_uint32)
    GET_REC_RESOLUTION = ior('i', 0x00000007, c_uint32)
    GET_MIN_TIMEOUT = ior('i', 0x00000008, c_uint32)
    GET_MAX_TIMEOUT = ior('i', 0x00000009, c_uint32)
    GET_LENGTH = ior('i', 0x0000000f, c_uint32)
    SET_SEND_MODE = iow('i', 0x00000011, c_uint32)
    SET_REC_MODE = iow('i', 0x00000012, c_uint32)
    SET_SEND_CARRIER = iow('i', 0x00000013, c_uint32)
    SET_REC_CARRIER = iow('i', 0x00000014, c_uint32)
    SET_SEND_DUTY_CYCLE = iow('i', 0x00000015, c_uint32)
    SET_TRANSMITTER_MASK = iow('i', 0x00000017, c_uint32)
    SET_REC_TIMEOUT = iow('i', 0x00000018, c_uint32)
    SET_REC_TIMEOUT_REPORTS = iow('i', 0x00000019, c_uint32)
    SET_MEASURE_CARRIER_MODE = iow('i', 0x0000001d, c_uint32)
    SET_REC_CARRIER_RANGE = iow('i', 0x0000001f, c_uint32)
    SET_WIDEBAND_RECEIVER = iow('i', 0x00000023, c_uint32)
    GET_REC_TIMEOUT = ior('i', 0x00000024, c_uint32)


class Lirc_Scancode(Structure):
    _fields_ = [('timestamp', c_uint64), ('flags', c_uint16),
                ('rc_proto', c_uint16), ('keycode', c_uint32),
                ('scancode', c_uint64)]


class Lirc_Scancode_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (TOGGLE, REPEAT) = range(1, 3)


class Rc_Proto(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (UNKNOWN, OTHER, RC5, RC5X_20, RC5_SZ, JVC, SONY12, SONY15, SONY20, NEC,
     NECX, NEC32, SANYO, MCIR2_KBD, MCIR2_MSE, RC6_0, RC6_6A_20, RC6_6A_24,
     RC6_6A_32, RC6_MCE, SHARP, XMP, CEC, IMON, RCMM12, RCMM24, RCMM32,
     XBOX_DVD) = range(28)
