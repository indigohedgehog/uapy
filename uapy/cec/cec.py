from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.common import *


class Cec_Max(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MSG_SIZE = 16


class Cec_Msg(Structure):
    _fields_ = [('tx_ts', c_uint64), ('rx_ts', c_uint64), ('len', c_uint32),
                ('timeout', c_uint32), ('sequence', c_uint32),
                ('flags', c_uint32), ('msg', c_uint8 * Cec_Max.MSG_SIZE),
                ('reply', c_uint8), ('rx_status', c_uint8),
                ('tx_status', c_uint8), ('tx_arb_lost_cnt', c_uint8),
                ('tx_nack_cnt', c_uint8), ('tx_low_drive_cnt', c_uint8),
                ('tx_error_cnt', c_uint8)]


def cec_msg_initiator(msg: POINTER(Cec_Msg)) -> c_uint8:
    return msg.contents.tx_ts >> 4


def cec_msg_destination(msg: POINTER(Cec_Msg)) -> c_uint8:
    return msg.contents.tx_ts & 0xf


def cec_msg_opcode(msg: POINTER(Cec_Msg)) -> c_int:
    return (-1, msg.contents.rx_ts)[msg.contents.len > 1]


def cec_msg_is_broadcast(msg: POINTER(Cec_Msg)) -> c_int:
    return (msg.contents.tx_ts & 0xf) == 0xf


def cec_msg_init(
        msg: POINTER(Cec_Msg), initiator: c_uint8, destination: c_uint8):
    memset(msg, 0, sizeof(pointer(msg)))
    msg.contents.tx_ts = (initiator << 4) | destination
    msg.contents.len = 1


def cec_msg_set_reply_to(msg: POINTER(Cec_Msg), orig: POINTER(Cec_Msg)):
    msg.contents.tx_ts = (
        cec_msg_destination(orig) << 4) | cec_msg_initiator(orig)
    msg.contents.reply = msg.timeout = 0


#define CEC_MSG_FL_REPLY_TO_FOLLOWERS	(1 << 0)
#define CEC_MSG_FL_RAW			(1 << 1)


class Cec_Tx_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OK, ARB_LOST, NACK, LOW_DRIVE, ERROR, MAX_RETRIES, ABORTED,
     TIMEOUT) = [1 << x for x in range(8)]


class Cec_Rx_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OK, TIMEOUT, FEATURE_ABORT, ABORTED) = [1 << x for x in range(4)]


def cec_msg_status_is_ok(msg: POINTER(Cec_Msg)) -> c_int:
    if (msg.tx_status and not (msg.tx_status & Cec_Tx_Status.OK)):
        return 0
    if (msg.rx_status and not (msg.rx_status & Cec_Rx_Status.OK)):
        return 0
    if (not msg.tx_status and not msg.rx_status):
        return 0
    return not (msg.rx_status & Cec_Rx_Status.FEATURE_ABORT)


#define CEC_PHYS_ADDR_INVALID		0xffff

#define CEC_MAX_LOG_ADDRS 4


class Cec_Log_Addr(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    INVALID = 0xff
    (TV, RECORD_1, RECORD_2, TUNER_1, PLAYBACK_1, AUDIOSYSTEM, TUNER_2,
     TUNER_3, PLAYBACK_2, RECORD_3, TUNER_4, PLAYBACK_3, BACKUP_1, BACKUP_2,
     SPECIFIC, UNREGISTERED) = range(16)
    BROADCAST = 15


class Cec_Log_Addr_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (TV, RECORD, TUNER, PLAYBACK, AUDIOSYSTEM, SPECIFIC,
     UNREGISTERED) = range(7)


class Cec_Log_Addr_Mask(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    TV = (1 << Cec_Log_Addr.TV)
    RECORD = ((1 << Cec_Log_Addr.RECORD_1) | (1 << Cec_Log_Addr.RECORD_2) |
              (1 << Cec_Log_Addr.RECORD_3))
    TUNER = ((1 << Cec_Log_Addr.TUNER_1) | (1 << Cec_Log_Addr.TUNER_2) |
             (1 << Cec_Log_Addr.TUNER_3) | (1 << Cec_Log_Addr.TUNER_4))
    PLAYBACK = ((1 << Cec_Log_Addr.PLAYBACK_1) | (1 << Cec_Log_Addr.PLAYBACK_2)
                | (1 << Cec_Log_Addr.PLAYBACK_3))
    AUDIOSYSTEM = (1 << Cec_Log_Addr.AUDIOSYSTEM)
    BACKUP = ((1 << Cec_Log_Addr.BACKUP_1) | (1 << Cec_Log_Addr.BACKUP_2))
    SPECIFIC = (1 << Cec_Log_Addr.SPECIFIC)
    UNREGISTERED = (1 << Cec_Log_Addr.UNREGISTERED)


def cec_has_tv(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.TV


def cec_has_record(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.RECORD


def cec_has_tuner(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.TUNER


def cec_has_playback(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.PLAYBACK


def cec_has_audiosystem(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.AUDIOSYSTEM


def cec_has_backup(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.BACKUP


def cec_has_specific(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.SPECIFIC


def cec_is_unregistered(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask & Cec_Log_Addr_Mask.UNREGISTERED


def cec_is_unconfigured(log_addr_mask: c_uint16) -> c_int:
    return log_addr_mask == 0
