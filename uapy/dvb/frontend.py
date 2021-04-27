from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.common import *


class Fe_Caps(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    FE_IS_STUPID = 0

    (FE_CAN_INVERSION_AUTO, FE_CAN_FEC_1_2, FE_CAN_FEC_2_3, FE_CAN_FEC_3_4,
     FE_CAN_FEC_4_5, FE_CAN_FEC_5_6, FE_CAN_FEC_6_7, FE_CAN_FEC_7_8,
     FE_CAN_FEC_8_9, FE_CAN_FEC_AUTO, FE_CAN_QPSK, FE_CAN_QAM_16,
     FE_CAN_QAM_32, FE_CAN_QAM_64, FE_CAN_QAM_128, FE_CAN_QAM_256,
     FE_CAN_QAM_AUTO, FE_CAN_TRANSMISSION_MODE_AUTO, FE_CAN_BAUTO,
     FE_CAN_GUARD_INTERVAL_AUTO, FE_CAN_HIERARCHY_AUTO, FE_CAN_8VSB,
     FE_CAN_16VSB, FE_HAS_EXTENDED_CAPS) = [1 << x for x in range(24)]

    (FE_CAN_MULTISTREAM, FE_CAN_TURBO_FEC, FE_CAN_2G_MODULAT, FE_NEEDS_BENDING,
     FE_CAN_RECOVER, FE_CAN_MUTE_TS) = [1 << x for x in range(26, 32)]


class Fe_Type(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (FE_QPSK, FE_QAM, FE_OFDM, FE_ATSC) = range(4)


class Dvb_Frontend_Info(Structure):
    _fields_ = [('name', c_char * 128), ('type', c_int),
                ('frequency_min', c_uint32), ('frequency_max', c_uint32),
                ('frequency_stepsize', c_uint32),
                ('frequency_tolerance', c_uint32),
                ('symbol_rate_min', c_uint32), ('symbol_rate_max', c_uint32),
                ('symbol_rate_tolerance', c_uint32),
                ('notifier_delay', c_uint32), ('caps', c_int)]


class Dvb_Diseqc_Master_Cmd(Structure):
    _fields_ = [('msg', c_uint8 * 6), ('msg_len', c_uint8)]


class Dvb_Diseqc_Slave_Reply(Structure):
    _fields_ = [('msg', c_uint8 * 4), ('msg_len', c_uint8),
                ('timeout', c_uint)]


class Fe_Sec_Voltage(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (S13, S18, SOFF) = range(3)


class Fe_Sec_Tone_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ON, OFF) = range(2)


class Fe_Sec_Mini_Cmd(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (A, B) = range(2)


class Fe_Status(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)
        FE_NONE = 0x00,

        (FE_HAS_SIGNAL, FE_HAS_CARRIER, FE_HAS_VITERBI, FE_HAS_SYNC,
         FE_HAS_LOCK, FE_TIMEDOUT, FE_REINIT) = [1 << x for x in range(7)]


class Fe_Spectral_Inversion(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (OFF, ON, AUTO) = range(3)


class Fe_Code_Rate(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    NONE = 0
    (C1_2, C2_3, C3_4, C4_5, C5_6, C6_7, C7_8, C8_9, CAUTO, C3_5, C9_10,
     C2_5) = range(12)


class Fe_Modulation(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)
        (QPSK, QAM_16, QAM_32, QAM_64, QAM_128, QAM_256, QAM_AUTO, VSB_8,
         VSB_16, PSK_8, APSK_16, APSK_32, DQPSK, QAM_4_NR) = range(14)


class Fe_Transmit_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (T2K, T8K, AUTO, T4K, T1K, T16K, T32K, C1, C3780) = range(9)


class Fe_Guard_Interval(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (G1_32, G1_16, G1_8, G1_4, AUTO, G1_128, G19_128, G19_256, PN420, PN595,
     PN945) = range(11)


class Fe_Hierarchy(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NONE, H1, H2, H4, AUTO) = range(5)


class Fe_Interleaving(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (NONE, AUTO, I240, I720) = range(4)


class Dtv_(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (UNDEFINED, TUNE, CLEAR, FREQUENCY, MODULATION, BHZ, INVERSION,
     DISEQC_MASTER, SYMBOL_RATE, INNER_FEC, VOLTAGE, TONE, PILOT, ROLLOFF,
     DISEQC_SLAVE_REPLY, FE_CAPABILITY_COUNT, FE_CAPABILITY, DELIVERY_SYSTEM,
     ISDBT_PARTIAL_RECEPTION, ISDBT_SOUND_BROADCASTING, ISDBT_SB_SUBCHANNEL_ID,
     ISDBT_SB_SEGMENT_IDX, ISDBT_SB_SEGMENT_COUNT, ISDBT_LAYERA_FEC,
     ISDBT_LAYERA_MODULATION, ISDBT_LAYERA_SEGMENT_COUNT,
     ISDBT_LAYERA_TIME_INTERLEAVING, ISDBT_LAYERB_FEC, ISDBT_LAYERB_MODULATION,
     ISDBT_LAYERB_SEGMENT_COUNT, ISDBT_LAYERB_TIME_INTERLEAVING,
     ISDBT_LAYERC_FEC, ISDBT_LAYERC_MODULATION, ISDBT_LAYERC_SEGMENT_COUNT,
     ISDBT_LAYERC_TIME_INTERLEAVING, API_VERSION, CODE_RATE_HP, CODE_RATE_LP,
     GUARD_INTERVAL, TRANSMISSION_MODE, HIERARCHY, ISDBT_LAYER_ENABLED,
     STREAM_ID, DVBT2_PLP_ID_LEGACY, ENUM_DELSYS, ATSCMH_FIC_VER,
     ATSCMH_PARADE_ID, ATSCMH_NOG, ATSCMH_TNOG, ATSCMH_SGN, ATSCMH_PRC,
     ATSCMH_RS_FRAME_MODE, ATSCMH_RS_FRAME_ENSEMBLE, ATSCMH_RS_CODE_MODE_PRI,
     ATSCMH_RS_CODE_MODE_SEC, ATSCMH_SCCC_BLOCK_MODE, ATSCMH_SCCC_CODE_MODE_A,
     ATSCMH_SCCC_CODE_MODE_B, ATSCMH_SCCC_CODE_MODE_C, ATSCMH_SCCC_CODE_MODE_D,
     INTERLEAVING, LNA, STAT_SIGNAL_STRENGTH, STAT_CNR,
     STAT_PRE_ERROR_BIT_COUNT, STAT_PRE_TOTAL_BIT_COUNT,
     STAT_POST_ERROR_BIT_COUNT, STAT_POST_TOTAL_BIT_COUNT,
     STAT_ERROR_BLOCK_COUNT, STAT_TOTAL_BLOCK_COUNT,
     SCRAMBLING_SEQUENCE_INDEX) = range(71)

    ISDBS_TS_ID_LEGACY = STREAM_ID
    MAX_COMMAND = SCRAMBLING_SEQUENCE_INDEX


class Fe_Pilot(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (ON, OFF, AUTO) = range(3)


class Fe_Rolloff(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (R35, R20, R25, AUTO) = range(4)


class Fe_Delivery_System(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SYS_UNDEFINED, SYS_DVBC_ANNEX_A, SYS_DVBC_ANNEX_B, SYS_DVBT, SYS_DSS,
     SYS_DVBS, SYS_DVBS2, SYS_DVBH, SYS_ISDBT, SYS_ISDBS, SYS_ISDBC, SYS_ATSC,
     SYS_ATSCMH, SYS_DTMB, SYS_CMMB, SYS_DAB, SYS_DVBT2, SYS_TURBO,
     SYS_DVBC_ANNEX_C) = range(19)
    SYS_DVBC_ANNEX_AC = SYS_DVBC_ANNEX_A
    SYS_DMBTH = SYS_DTMB


class Atscmh_Sccc_Block_mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (SEP, COMB, RES) = range(3)


class Atscmh_Sccc_Code_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (HLF, QTR, RES) = range(3)


class Atscmh_Rs_Frame_Ensemble(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PRI, SEC) = range(2)


class Atscmh_Rs_Frame_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (PRI_ONLY, PRI_SEC, RES) = range(3)


class Atscmh_Rs_Code_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (R211_187, R223_187, R235_187, RES) = range(4)


class Dvb_Sys(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    NO_STREAM_ID_FILTER = ~c_uint32(0).value
    LNA_AUTO = ~c_uint32(0).value


def v4l2_ctrl_id2which(id):
    c = 0x0fff0000
    return id & c_ulong(c).value


class Fecap_Scale_Params(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    NOT_AVAILABLE = 0,
    (DECIBEL, RELATIVE, COUNTER) = range(3)


class Dtv_Stats(Structure):
    class _u(Union):
        _fields_ = [('uvalue', c_uint64), ('svalue', c_int64)]

    _fields_ = [('scale', c_uint8), ('_u', _u)]
    _pack_ = True


class Dtv_Statistics(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MAX = 4


class Dtv_Fe_Stats(Structure):
    _fields_ = [('len', c_uint8), ('stat', Dtv_Stats * Dtv_Statistics.MAX)]
    _pack_ = True


class Dtv_Property(Structure):
    class _u(Union):
        class _s(Structure):
            _fields_ = [('data', c_uint8 * 32), ('len', c_uint32),
                        ('reserved1', c_uint32 * 3), ('reserved2', c_void_p)]

        _fields_ = [('data', c_uint32), ('st', Dtv_Fe_Stats), ('buffer', _s)]

    _fields_ = [('cmd', c_uint32), ('reserved', c_uint32 * 3), ('u', _u),
                ('result', c_int)]
    _pack_ = True


class Dtv_Msgs(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    MAX = 64


class Dtv_Properties(Structure):
    _fields_ = [('num', c_uint32), ('props', POINTER(Dtv_Property))]


class Tune_Mode(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ONESHOT = 0x01


class Fe_Bandwidth(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    (B8_MHZ, B7_MHZ, B6_MHZ, AUTO, B5_MHZ, B10_MHZ, B1_712_MHZ) = range(7)


Fe_Sec_Voltage_T = Fe_Sec_Voltage
Fe_Caps_T = Fe_Caps
Fe_Type_T = Fe_Type
Fe_Sec_Tone_Mode_T = Fe_Sec_Tone_Mode
Fe_Sec_Mini_Cmd_T = Fe_Sec_Mini_Cmd
Fe_Status_T = Fe_Status
Fe_Spectral_Inversion_T = Fe_Spectral_Inversion
Fe_Code_Rate_T = Fe_Code_Rate
Fe_Modulation_T = Fe_Modulation
Fe_Transmit_Mode_T = Fe_Transmit_Mode
Fe_Bandwidth_T = Fe_Bandwidth
Fe_Guard_Interval_T = Fe_Guard_Interval
Fe_Hierarchy_T = Fe_Hierarchy
Fe_Pilot_T = Fe_Pilot
Fe_Rolloff_T = Fe_Rolloff
Fe_Delivery_System_T = Fe_Delivery_System


class Dvb_Qpsk_Parameters(Structure):
    _fields_ = [
        ('symbol_rate', c_uint32),
        ('fec_inner', c_uint32),
    ]


class Dvb_Qam_Parameters(Structure):
    _fields_ = [('symbol_rate', c_uint32), ('fec_inner', c_uint32),
                ('modulation', c_uint32)]


class Dvb_Vsb_Parameters(Structure):
    _fields_ = [
        ('modulation', c_uint32),
    ]


class Dvb_Ofdm_Parameters(Structure):
    _fields_ = [('bandwidth', c_uint32), ('code_rate_HP', c_uint32),
                ('code_rate_LP', c_uint32), ('constellation', c_uint32),
                ('transmission_mode', c_uint32), ('guard_interval', c_uint32),
                ('hierarchy_information', c_uint32)]


class Dvb_Frontend_Parameters(Structure):
    class _u(Union):
        _fields_ = [('qpsk', Dvb_Qpsk_Parameters), ('qam', Dvb_Qam_Parameters),
                    ('ofdm', Dvb_Ofdm_Parameters), ('vsb', Dvb_Vsb_Parameters)]

    _fields_ = [('frequency', c_uint32), ('inversion', c_uint32), ('u', _u)]


class Dvb_Frontend_Event(Structure):
    _fields_ = [('status', c_uint32), ('parameters', Dvb_Frontend_Parameters)]


class Fe(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    GET_INFO = ior('o', 61, Dvb_Frontend_Info)
    DISEQC_RESET_OVERLOAD = io('o', 62)
    DISEQC_SEND_MASTER_CMD = iow('o', 63, Dvb_Diseqc_Master_Cmd)
    DISEQC_RECV_SLAVE_REPLY = ior('o', 64, Dvb_Diseqc_Slave_Reply)
    DISEQC_SEND_BURST = io('o', 65)
    SET_TONE = io('o', 66)
    SET_VOLTAGE = io('o', 67)
    ENABLE_HIGH_LNB_VOLTAGE = io('o', 68)
    READ_STATUS = ior('o', 69, c_uint32)
    READ_BER = ior('o', 70, c_uint32)
    READ_SIGNAL_STRENGTH = ior('o', 71, c_uint16)
    READ_SNR = ior('o', 72, c_uint16)
    READ_UNCORRECTED_BLOCKS = ior('o', 73, c_uint32)
    SET_FRONTEND_TUNE_MODE = io('o', 81)
    GET_EVENT = ior('o', 78, Dvb_Frontend_Event)
    DISHNETWORK_SEND_LEGACY_CMD = io('o', 80)
    SET_PROPERTY = iow('o', 82, Dtv_Properties)
    GET_PROPERTY = ior('o', 83, Dtv_Properties)
    SET_FRONTEND = iow('o', 76, Dvb_Frontend_Parameters)
    GET_FRONTEND = ior('o', 77, Dvb_Frontend_Parameters)
