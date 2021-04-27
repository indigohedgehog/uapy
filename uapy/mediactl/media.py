from ctypes import *
from enum import Enum, IntEnum
from util.ioctl import *
from util.ctypes_tools import *
from v4l2.common import *


class Media_Device_Info(Structure):
    _fields_ = [('driver', c_char * 16), ('model', c_char * 32),
                ('serial', c_char * 40), ('bus_info', c_char * 32),
                ('media_version', c_uint32), ('hw_revision', c_uint32),
                ('driver_version', c_uint32), ('reserved', c_uint32 * 31)]


class Media_Ent_F(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    BASE = 0x00000000
    OLD_BASE = 0x00010000
    OLD_SUBDEV_BASE = 0x00020000
    UNKNOWN = BASE
    V4L2_SUBDEV_UNKNOWN = OLD_SUBDEV_BASE
    DTV_DEMOD = (BASE + 0x00001)
    TS_DEMUX = (BASE + 0x00002)
    DTV_CA = (BASE + 0x00003)
    DTV_NET_DECAP = (BASE + 0x00004)
    IO_V4L = (OLD_BASE + 1)
    IO_DTV = (BASE + 0x01001)
    IO_VBI = (BASE + 0x01002)
    IO_SWRADIO = (BASE + 0x01003)
    CAM_SENSOR = (OLD_SUBDEV_BASE + 1)
    FLASH = (OLD_SUBDEV_BASE + 2)
    LENS = (OLD_SUBDEV_BASE + 3)
    TUNER = (OLD_SUBDEV_BASE + 5)
    IF_VID_DECODER = (BASE + 0x02001)
    IF_AUD_DECODER = (BASE + 0x02002)
    AUDIO_CAPTURE = (BASE + 0x03001)
    AUDIO_PLAYBACK = (BASE + 0x03002)
    AUDIO_MIXER = (BASE + 0x03003)
    PROC_VIDEO_COMPOSER = (BASE + 0x4001)
    PROC_VIDEO_PIXEL_FORMATTER = (BASE + 0x4002)
    PROC_VIDEO_PIXEL_ENC_CONV = (BASE + 0x4003)
    PROC_VIDEO_LUT = (BASE + 0x4004)
    PROC_VIDEO_SCALER = (BASE + 0x4005)
    PROC_VIDEO_STATISTICS = (BASE + 0x4006)
    PROC_VIDEO_ENCODER = (BASE + 0x4007)
    PROC_VIDEO_DECODER = (BASE + 0x4008)
    VID_MUX = (BASE + 0x5001)
    VID_IF_BRIDGE = (BASE + 0x5002)
    ATV_DECODER = (OLD_SUBDEV_BASE + 4)
    DV_DECODER = (BASE + 0x6001)
    DV_ENCODER = (BASE + 0x6002)
    DTV_DECODER = DV_DECODER


class Media_Ent_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    DEFAULT = (1 << 0)
    CONNECTOR = (1 << 1)


class Media_Ent_Id(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    FLAG_NEXT = (1 << 31)


class Media_Entity_Desc(Structure):
    class _u(Union):
        class _dev(Structure):
            _fields_ = [('major', c_uint32), ('minor', c_uint32)]

        class _alsa(Structure):
            _fields_ = [('card', c_uint32), ('device', c_uint32),
                        ('subdevice', c_uint32)]

        class _v4l(Structure):
            _fields_ = [('major', c_uint32), ('minor', c_uint32)]

        class _fb(Structure):
            _fields_ = [('major', c_uint32), ('minor', c_uint32)]

        _fields_ = [('dev', _dev), ('alsa', _alsa), ('v4l', _v4l), ('fb', _fb),
                    ('dvb', c_int), ('raw', c_uint8 * 184)]

    _fields_ = [
        ('id', c_uint32),
        ('name', c_char * 32),
        ('type', c_uint32),
        ('revision', c_uint32),
        ('flags', c_uint32),
        ('group_id', c_uint32),
        ('pads', c_uint16),
        ('links', c_uint16),
        ('reserved', c_uint32 * 4),
    ]


class Media_Pad_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    SINK = (1 << 0)
    SOURCE = (1 << 1)
    MUST_CONNECT = (1 << 2)


class Media_Pad_Desc(Structure):
    _fields_ = [('entity', c_uint32), ('index', c_uint16), ('flags', c_uint32),
                ('reserved', c_uint32 * 2)]


class Media_Link_Fl(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    ENABLED = (1 << 0)
    IMMUTABLE = (1 << 1)
    DYNAMIC = (1 << 2)
    LINK_TYPE = (0xf << 28)
    DATA_LINK = (0 << 28)
    INTERFACE_LINK = (1 << 28)


class Media_Link_Desc(Structure):
    _fields_ = [('source', Media_Pad_Desc), ('sink', Media_Pad_Desc),
                ('flags', c_uint32), ('reserved', c_uint32 * 2)]


class Media_Links_Enum(Structure):
    _fields_ = [('entity', c_uint32), ('pads', POINTER(Media_Pad_Desc)),
                ('links', POINTER(Media_Link_Desc)), ('reserved', c_uint32)]


class Media_Intf_T(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    DVB_BASE = 0x00000100
    V4L_BASE = 0x00000200
    DVB_FE = (DVB_BASE)
    DVB_DEMUX = (DVB_BASE + 1)
    DVB_DVR = (DVB_BASE + 2)
    DVB_CA = (DVB_BASE + 3)
    DVB_NET = (DVB_BASE + 4)
    V4L_VIDEO = (V4L_BASE)
    V4L_VBI = (V4L_BASE + 1)
    V4L_RADIO = (V4L_BASE + 2)
    V4L_SUBDEV = (V4L_BASE + 3)
    V4L_SWRADIO = (V4L_BASE + 4)
    V4L_TOUCH = (V4L_BASE + 5)
    ALSA_BASE = 0x00000300
    ALSA_PCM_CAPTURE = (ALSA_BASE)
    ALSA_PCM_PLAYBACK = (ALSA_BASE + 1)
    ALSA_CONTROL = (ALSA_BASE + 2)
    ALSA_COMPRESS = (ALSA_BASE + 3)
    ALSA_RAWMIDI = (ALSA_BASE + 4)
    ALSA_HWDEP = (ALSA_BASE + 5)
    ALSA_SEQUENCER = (ALSA_BASE + 6)
    ALSA_TIMER = (ALSA_BASE + 7)


def media_v2_entity_has_flags(media_version):
    return ((media_version) >= ((4 << 16) | (19 << 8) | 0))


class Media_V2_Entity(Structure):
    _fields_ = [('id', c_uint32), ('name', c_char), ('function', c_uint32),
                ('flags', c_uint32), ('reserved', c_uint32 * 5)]
    _pack_ = True


class Media_V2_Intf_Devnode(Structure):
    _fields_ = [('major', c_uint32), ('minor', c_uint32)]
    _pack_ = True


class Media_V2_Interface(Structure):
    class _u(Union):
        _fields_ = [('devnode', Media_V2_Intf_Devnode), ('raw', c_uint32 * 16)]

    _fields_ = [('id', c_uint32), ('intf_type', c_uint32), ('flags', c_uint32),
                ('reserved', c_uint32)]
    _pack_ = True


def media_v2_pad_has_index(media_version):
    return ((media_version) >= ((4 << 16) | (19 << 8) | 0))


class Media_V2_Pad(Structure):
    _fields_ = [('id', c_uint32), ('entity_id', c_uint32), ('flags', c_uint32),
                ('index', c_uint32), ('reserved', c_uint32 * 4)]
    _pack_ = True


class Media_V2_Link(Structure):
    _fields_ = [
        ('id', c_uint32),
        ('source_id', c_uint32),
        ('sink_id', c_uint32),
        ('flags', c_uint32),
        ('reserved', c_uint32 * 6),
    ]
    _pack_ = True


class Media_V2_Topology(Structure):
    _fields_ = [('topology_version', c_uint64), ('num_entities', c_uint32),
                ('reserved1', c_uint32), ('ptr_entities', c_uint64),
                ('num_interfaces', c_uint32), ('reserved2', c_uint32),
                ('ptr_interfaces', c_uint64), ('num_pads', c_uint32),
                ('reserved3', c_uint32), ('ptr_pads', c_uint64),
                ('num_links', c_uint32), ('reserved4', c_uint32),
                ('ptr_links', c_uint64)]
    _pack_ = True


class Media_Ioc(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    DEVICE_INFO = iowr('|', 0x00, Media_Device_Info)
    ENUM_ENTITIES = iowr('|', 0x01, Media_Entity_Desc)
    ENUM_LINKS = iowr('|', 0x02, Media_Links_Enum)
    SETUP_LINK = iowr('|', 0x03, Media_Link_Desc)
    G_TOPOLOGY = iowr('|', 0x04, Media_V2_Topology)
    REQUEST_ALLOC = ior('|', 0x05, c_int)


class Media_Request_Ioc(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    QUEUE = io('|', 0x80)
    REINIT = io('|', 0x81)


class Media_Ent(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    TYPE_SHIFT = 16
    TYPE_MASK = 0x00ff0000
    SUBTYPE_MASK = 0x0000ffff


class Media_Ent_T(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    DEVNODE_UNKNOWN = (Media_Ent_F.OLD_BASE | Media_Ent.SUBTYPE_MASK)
    DEVNODE = Media_Ent_F.OLD_BASE
    DEVNODE_V4L = Media_Ent_F.IO_V4L
    DEVNODE_FB = (Media_Ent_F.OLD_BASE + 2)
    DEVNODE_ALSA = (Media_Ent_F.OLD_BASE + 3)
    DEVNODE_DVB = (Media_Ent_F.OLD_BASE + 4)
    UNKNOWN = Media_Ent_F.UNKNOWN
    V4L2_VIDEO = Media_Ent_F.IO_V4L
    V4L2_SUBDEV = Media_Ent_F.V4L2_SUBDEV_UNKNOWN
    V4L2_SUBDEV_SENSOR = Media_Ent_F.CAM_SENSOR
    V4L2_SUBDEV_FLASH = Media_Ent_F.FLASH
    V4L2_SUBDEV_LENS = Media_Ent_F.LENS
    V4L2_SUBDEV_DECODER = Media_Ent_F.ATV_DECODER
    V4L2_SUBDEV_TUNER = Media_Ent_F.TUNER


class Media_Api(IntEnum):
    def __str__(self):
        return '{0}'.format(self.value)

    VERSION = ((0 << 16) | (1 << 8) | 0)
