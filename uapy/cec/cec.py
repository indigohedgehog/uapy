from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.common import *


class Cec_Max(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MSG_SIZE = 16
    LOG_ADDRS = 4


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


class Cec_Msg_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (REPLY_TO_FOLLOWERS, RAW) = [1 << x for x in range(2)]


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


class Cec_Phys_Addr(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    INVALID = 0xffff


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


class Cec_Vendor(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ID_NONE = 0xffffffff


class Cec_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NO_INITIATOR, INITIATOR, EXCL_INITIATOR) = [x << 0 for x in range(3)]

    INITIATOR_MSK = 0x0f

    (NO_FOLLOWER, FOLLOWER, EXCL_FOLLOWER,
     EXCL_FOLLOWER_PASSTHRU) = [x << 4 for x in range(4)]

    (MONITOR_PIN, MONITOR, MONITOR_ALL) = [x << 4 for x in range(13, 16)]

    FOLLOWER_MSK = 0xf0


class Cec_Cap(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PHYS_ADDR, LOG_ADDRS, TRANSMIT, PASSTHROUGH, RC, MONITOR_ALL, NEEDS_HPD,
     MONITOR_PIN) = [1 << x for x in range(8)]


class Cec_Caps(Structure):
    _fields_ = [
        ('driver', c_char * 32),
        ('name', c_char * 32),
        ('available_log_addrs', c_uint32),
        ('capabilities', c_uint32),
        ('version', c_uint32),
    ]


class Cec_Log_Addrs(Structure):
    _fields_ = [('log_addr', c_uint8 * Cec_Max.LOG_ADDRS),
                ('log_addr_mask', c_uint16), ('cec_version', c_uint8),
                ('num_log_addrs', c_uint8), ('vendor_id', c_uint32),
                ('flags', c_uint32), ('osd_name', c_char * 15),
                ('primary_device_type', c_uint8 * Cec_Max.LOG_ADDRS),
                ('log_addr_type', c_uint8 * Cec_Max.LOG_ADDRS),
                ('all_device_types', c_uint8 * Cec_Max.LOG_ADDRS),
                ('features', c_uint8 * Cec_Max.LOG_ADDRS * 12)]


class Cec_Log_Addrs_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ALLOW_UNREG_FALLBACK, ALLOW_RC_PASSTHRU,
     CDC_ONLY) = [1 << x for x in range(3)]


class Cec_Event_Enum(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (STATE_CHANGE, LOST_MSGS, PIN_CEC_LOW, PIN_CEC_HIGH, PIN_HPD_LOW,
     PIN_HPD_HIGH, PIN_5V_LOW, PIN_5V_HIGH) = range(1, 9)


class Cec_Event_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (INITIAL_STATE, DROPPED_EVENTS) = [1 << x for x in range(2)]


class Cec_Event_State_Change(Structure):
    _fields_ = [('phys_addr', c_uint16), ('log_addr_mask', c_uint16)]


class Cec_Event_Lost_Msgs(Structure):
    _fields_ = [('lost_msgs', c_uint32)]


class Cec_Event(Structure):
    class _u(Union):
        _field_ = [('state_change', Cec_Event_State_Change),
                   ('lost_msgs', Cec_Event_Lost_Msgs), ('raw', c_uint32)]

    _fields_ = [('ts', c_uint64), ('event', c_uint32), ('flags', c_uint32),
                ('_u', _u)]


class Cec(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ADAP_G_CAPS = iowr('a', 0, Cec_Caps)
    ADAP_G_PHYS_ADDR = ior('a', 1, c_uint16)
    ADAP_S_PHYS_ADDR = iow('a', 2, c_uint16)
    ADAP_G_LOG_ADDRS = ior('a', 3, Cec_Log_Addrs)
    ADAP_S_LOG_ADDRS = iowr('a', 4, Cec_Log_Addrs)
    TRANSMIT = iowr('a', 5, Cec_Msg)
    RECEIVE = iowr('a', 6, Cec_Msg)
    DQEVENT = iowr('a', 7, Cec_Event)
    G_MODE = ior('a', 8, c_uint32)
    S_MODE = iow('a', 9, c_uint32)


class Cec_Msg_Enum(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ACTIVE_SOURCE = 0x82
    IMAGE_VIEW_ON = 0x04
    TEXT_VIEW_ON = 0x0d
    INACTIVE_SOURCE = 0x9d
    REQUEST_ACTIVE_SOURCE = 0x85
    ROUTING_CHANGE = 0x80
    ROUTING_INFORMATION = 0x81
    SET_STREAM_PATH = 0x86
    STANDBY = 0x36
    RECORD_OFF = 0x0b
    RECORD_ON = 0x09
    RECORD_STATUS = 0x0a
    RECORD_TV_SCREEN = 0x0f
    CLEAR_ANALOGUE_TIMER = 0x33
    CLEAR_DIGITAL_TIMER = 0x99
    CLEAR_EXT_TIMER = 0xa1
    SET_ANALOGUE_TIMER = 0x34
    SET_DIGITAL_TIMER = 0x97
    SET_EXT_TIMER = 0xa2
    SET_TIMER_PROGRAM_TITLE = 0x67
    TIMER_CLEARED_STATUS = 0x43
    TIMER_STATUS = 0x35
    CEC_VERSION = 0x9e
    SET_MENU_LANGUAGE = 0x32
    REPORT_FEATURES = 0xa6
    GET_CEC_VERSION = 0x9f
    GIVE_PHYSICAL_ADDR = 0x83
    GET_MENU_LANGUAGE = 0x91
    REPORT_PHYSICAL_ADDR = 0x84
    GIVE_FEATURES = 0xa5
    DECK_CONTROL = 0x42
    DECK_STATUS = 0x1b
    GIVE_DECK_STATUS = 0x1a
    GIVE_TUNER_DEVICE_STATUS = 0x08
    SELECT_ANALOGUE_SERVICE = 0x92
    SELECT_DIGITAL_SERVICE = 0x93
    TUNER_DEVICE_STATUS = 0x07
    PLAY = 0x41
    TUNER_STEP_DECREMENT = 0x06
    TUNER_STEP_INCREMENT = 0x05
    DEVICE_VENDOR_ID = 0x87
    GIVE_DEVICE_VENDOR_ID = 0x8c
    VENDOR_COMMAND = 0x89
    VENDOR_COMMAND_WITH_ID = 0xa0
    VENDOR_REMOTE_BUTTON_DOWN = 0x8a
    VENDOR_REMOTE_BUTTON_UP = 0x8b
    SET_OSD_STRING = 0x64
    GIVE_OSD_NAME = 0x46
    SET_OSD_NAME = 0x47
    MENU_REQUEST = 0x8d
    MENU_STATUS = 0x8e
    USER_CONTROL_PRESSED = 0x44
    USER_CONTROL_RELEASED = 0x45
    GIVE_DEVICE_POWER_STATUS = 0x8f
    REPORT_POWER_STATUS = 0x90
    ABORT = 0xff
    GIVE_AUDIO_STATUS = 0x71
    GIVE_SYSTEM_AUDIO_MODE_STATUS = 0x7d
    REPORT_AUDIO_STATUS = 0x7a
    REPORT_SHORT_AUDIO_DESCRIPTOR = 0xa3
    REQUEST_SHORT_AUDIO_DESCRIPTOR = 0xa4
    SET_SYSTEM_AUDIO_MODE = 0x72
    SYSTEM_AUDIO_MODE_REQUEST = 0x70
    SYSTEM_AUDIO_MODE_STATUS = 0x7e
    SET_AUDIO_RATE = 0x9a
    FEATURE_ABORT = 0x00
    INITIATE_ARC = 0xc0
    REPORT_ARC_INITIATED = 0xc1
    REPORT_ARC_TERMINATED = 0xc2
    REQUEST_ARC_INITIATION = 0xc3
    REQUEST_ARC_TERMINATION = 0xc4
    TERMINATE_ARC = 0xc5
    REQUEST_CURRENT_LATENCY = 0xa7
    REPORT_CURRENT_LATENCY = 0xa8
    CDC_MESSAGE = 0xf8
    CDC_HEC_INQUIRE_STATE = 0x00
    CDC_HEC_REPORT_STATE = 0x01
    CDC_HEC_SET_STATE_ADJACENT = 0x02
    CDC_HEC_SET_STATE = 0x03
    CDC_HEC_REQUEST_DEACTIVATION = 0x04
    CDC_HEC_NOTIFY_ALIVE = 0x05
    CDC_HEC_DISCOVER = 0x06
    CDC_HPD_SET_STATE = 0x10
    CDC_HPD_REPORT_STATE = 0x11


class Cec_Op_Record_Src(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OWN, DIGITAL, ANALOG, EXT_PLUG, EXT_PHYS_ADDR) = range(1, 6)


class Cec_Op_Service_ID_Method(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (BY_DIG_ID, BY_CHANNEL) = range(2)


class Cec_Op_Dig_Service_Bcast_System(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ARIB_GEN, ATSC_GEN, DVB_GEN) = range(3)

    (ARIB_BS, ARIB_CS, ARIB_T) = range(8, 11)

    (ATSC_CABLE, ATSC_SAT, ATSC_T) = range(16, 19)

    (DVB_C, DVB_S, DVB_S2, DVB_T) = range(24, 28)


class Cec_Op_Ana_Bcast_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (CABLE, SATELLITE, TERRESTRIAL) = range(3)


class Cec_Op_Bcast_System(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PAL_BG, SECAM_LQ, PAL_M, NTSC_M, PAL_I, SECAM_DK, SECAM_BG, SECAM_L,
     PAL_DK) = range(0x9)

    OTHER = 0x1f


class Cec_Op_Channel_Number(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (FMT_1_PART, FMT_2_PART) = range(1, 3)


class Cec_Op_Record_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (CUR_SRC, DIG_SERVICE, ANA_SERVICE, EXT_INPUT, NO_DIG_SERVICE,
     NO_ANA_SERVICE, NO_SERVICE) = range(1, 8)

    (INVALID_EXT_PLUG, INVALID_EXT_PHYS_ADDR, UNSUP_CA, NO_CA_ENTITLEMENTS,
     CANT_COPY_SRC, NO_MORE_COPIES) = range(9, 15)

    (NO_MEDIA, PLAYING, ALREADY_RECORDING, MEDIA_PROT, NO_SIGNAL,
     MEDIA_PROBLEM, NO_SPACE, PARENTAL_LOCK) = range(16, 24)

    (TERMINATED_OK, ALREADY_TERM) = range(26, 28)
    OTHER = 0x1f


class Cec_Op_Rec_Seq(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,
     SATERDAY) = [1 << x for x in range(7)]

    ONCE_ONLY = 0x00


class Cec_Op_Ext_Src(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PLUG, PHYS_ADDR) = range(4, 6)


class Cec_Op_Timer_Clr_Stat(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (RECORDING, NO_MATCHING, NO_INFO) = range(3)

    CLEARED = 0x80


class Cec_Op_Timer_Overlap_Warning(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NO_OVERLAP, OVERLAP) = range(2)


class Cec_Op_Media_Info(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (UNPROT_MEDIA, PROT_MEDIA, NO_MEDIA) = range(3)


class Cec_Op_Prog_Ind(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NOT_PROGRAMMED, PROGRAMMED) = range(2)


class Cec_Op_Prog_Info(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ENOUGH_SPACE, NOT_ENOUGH_SPACE, NONE_AVAILABLE,
     MIGHT_NOT_BE_ENOUGH_SPACE) = range(8, 12)


class Cec_Op_Prog_Error(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NO_FREE_TIMER, DATE_OUT_OF_RANGE, REC_SEQ_ERROR, INV_EXT_PLUG,
     INV_EXT_PHYS_ADDR, CA_UNSUPP, INSUF_CA_ENTITLEMENTS, RESOLUTION_UNSUPP,
     PARENTAL_LOCK, CLOCK_FAILURE) = range(1, 11)

    DUPLICATE = 0x0e


class Cec_Op_Cec(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (VERSION_1_3A, VERSION_1_4, VERSION_2_0) = range(4, 7)


class Cec_Op_Prim_Devtype(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (TV, RECORD) = range(2)

    (TUNER, PLAYBACK, AUDIOSYSTEM, SWITCH, PROCESSOR) = range(3, 8)


class Cec_Op_All_Devtype(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SWITCH, AUDIOSYSTEM, PLAYBACK, TUNER, RECORD,
     TV) = [1 << x for x in range(2, 8)]


class Cec_Op_Feat(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    EXT = 0x80


class Cec_Op_Feat_Rc_Tv(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    PROFILE_NONE = 0x00

    (PROFILE_1, PROFILE_2, PROFILE_3, PROFILE_4) = range(2, 15, 4)


class Cec_Op_Feat_Rc_Src(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    HAS_DEV_ROOT_MENU = 0x50
    HAS_DEV_SETUP_MENU = 0x48
    HAS_CONTENTS_MENU = 0x44
    HAS_MEDIA_TOP_MENU = 0x42
    HAS_MEDIA_CONTEXT_MENU = 0x41


class Cec_Op_Feat_Dev(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SOURCE_HAS_ARC_RX, SINK_HAS_ARC_TX, HAS_SET_AUDIO_RATE, HAS_DECK_CONTROL,
     HAS_SET_OSD_STRING, HAS_RECORD_TV_SCREEN) = [1 << x for x in range(2, 8)]


class Cec_Op_Deck_Ctl_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SKIP_FWD, SKIP_REV, STOP, EJECT) = range(1, 5)


class Cec_Op_Deck_Info(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PLAY, RECORD, PLAY_REV, STILL, SLOW, SLOW_REV, FAST_FWD, FAST_REV,
     NO_MEDIA, STOP, SKIP_FWD, SKIP_REV, INDEX_SEARCH_FWD, INDEX_SEARCH_REV,
     OTHER) = range(17, 32)


class Cec_Op_Status_Req(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ON, OFF, ONCE) = range(1, 4)


class Cec_Op_Play_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PLAY_FAST_FWD_MIN, PLAY_FAST_FWD_MED, PLAY_FAST_FWD_MAX) = range(5, 8)

    (PLAY_FAST_REV_MIN, PLAY_FAST_REV_MED, PLAY_FAST_REV_MAX) = range(9, 12)

    (PLAY_SLOW_FWD_MIN, PLAY_SLOW_FWD_MED, PLAY_SLOW_FWD_MAX) = range(21, 24)

    (PLAY_SLOW_REV_MIN, PLAY_SLOW_REV_MED, PLAY_SLOW_REV_MAX) = range(25, 28)

    PLAY_REV = 0x20

    (PLAY_FWD, PLAY_STILL) = range(36, 38)


class Cec_Op_Rec_Flag(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NOT_USED, USED) = range(2)


class Cec_Op_Tuner_Display_Info(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DIGITAL, NONE, ANALOGUE) = range(3)


class Cec_Op_Disp_Ctl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    DEFAULT = 0x00
    (UNTIL_CLEARED, CLEAR) = [1 << x for x in range(6, 8)]


class Cec_Op_Menu_Request(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ACTIVATE, DEACTIVATE, QUERY) = range(3)


class Cec_Op_Menu_State(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ACTIVATED, DEACTIVATED) = range(2)


class Cec_Op_Ui_Bcast_Type_Toggle(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ALL, DIG_ANA) = range(2)


class Cec_Op_Ui_Bcast_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ANALOGUE, ANALOGUE_T, ANALOGUE_CABLE, ANALOGUE_SAT, DIGITAL, DIGITAL_T,
     DIGITAL_CABLE, DIGITAL_SAT, DIGITAL_COM_SAT, IP) = range(16, 161, 16)

    DIGITAL_COM_SAT2 = 0x91


class Cec_Op_Ui_Snd_Pres_Ctl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DUAL_MONO, KARAOKE) = range(16, 33, 16)

    (DOWNMIX, REVERB, EQUALIZER) = range(128, 161, 16)


class Cec_Op_Ui_Snd_Pres_Ctl_Bass(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (UP, NEUTRAL, DOWN) = range(177, 180)


class Cec_Op_Ui_Snd_Pres_Ctl_Treble(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (UP, NEUTRAL, DOWN) = range(193, 196)


class Cec_Op_Power_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ON, STANDBY, TO_ON, TO_STANDBY) = range(4)


class Cec_Op_Abort(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (UNRECOGNIZED_OP, INCORRECT_MODE, NO_SOURCE, INVALID_OP, REFUSED,
     UNDETERMINED) = range(6)


class Cec_Op_Aud_Mute_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OFF, ON) = range(2)


class Cec_Op_Sys_Aud_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OFF, ON) = range(2)


class Cec_Op_Aud_Fmt_Id(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (CEA861, CEA861_CXT) = range(2)


class Cec_Op_Aud_Rate(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OFF, WIDE_STD, WIDE_FAST, WIDE_SLOW, NARROW_STD, NARROW_FAST,
     NARROW_SLOW) = range(7)


class Cec_Op_Low_Latency_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OFF, ON) = range(2)


class Cec_Op_Aud_Out_Compensated(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NA, DELAY, NO_DELAY, PARTIAL_DELAY) = range(4)


class Cec_Op_Hec_Func_State(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NOT_SUPPORTED, INACTIVE, ACTIVE, ACTIVATION_FIELD) = range(4)


class Cec_Op_Host_Func_State(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NOT_SUPPORTED, INACTIVE, ACTIVE) = range(3)


class Cec_Op_Enc_Func_State_Ext_Con(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NOT_SUPPORTED, INACTIVE, ACTIVE) = range(3)


class Cec_Op_Cdc_Error_Code(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NONE, CAP_UNSUPPORTED, WRONG_STATE, OTHER) = range(4)


class Cec_Op_Hec_Support(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NO, YES) = range(2)


class Cec_Op_Hec_Activation(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ON, OFF) = range(2)


class Cec_Op_Hec_Set_State(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (DEACTIVATE, ACTIVATE) = range(2)


class Cec_Op_Hpd_State(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (CP_EDID_DISABLE, CP_EDID_ENABLE, CP_EDID_DISABLE_ENABLE, EDID_DISABLE,
     EDID_ENABLE, EDID_DISABLE_ENABLE) = range(6)


class Cec_Op_Hpd_Error(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NONE, INITIATOR_NOT_CAPABLE, INITIATOR_WRONG_STATE, OTHER,
     NONE_NO_VIDEO) = range(5)


def cec_is_2nd_tv(las: POINTER(Cec_Log_Addrs)) -> c_int:
    return las.contents.num_log_addrs and \
        las.contents.log_addr[0] >= Cec_Log_Addr.SPECIFIC and \
        las.contents.primary_device_type[0] == Cec_Op_Prim_Devtype.TV


def cec_is_processor(las: POINTER(Cec_Log_Addrs)) -> c_int:
    return las.contents.num_log_addrs and \
           las.contents.log_addr[0] >= Cec_Log_Addr.BACKUP_1 and \
           las.contents.primary_device_type[0] == Cec_Op_Prim_Devtype.PROCESSOR


def cec_is_switch(las: POINTER(Cec_Log_Addrs)) -> c_int:
    return las.contents.num_log_addrs == 1 and \
           las.contents.log_addr[0] == Cec_Log_Addr.UNREGISTERED and \
           las.contents.primary_device_type[0] == Cec_Op_Prim_Devtype.SWITCH and \
           not(las.contents.flags & Cec_Log_Addrs_Fl.CDC_ONLY)


def cec_is_cdc_only(las: POINTER(Cec_Log_Addrs)) -> c_int:
    return las.contents.num_log_addrs == 1 and \
           las.contents.log_addr[0] == Cec_Log_Addr.UNREGISTERED and \
           las.contents.primary_device_type[0] == Cec_Op_Prim_Devtype.SWITCH and \
           (las.contents.flags & Cec_Log_Addrs_Fl.CDC_ONLY)
