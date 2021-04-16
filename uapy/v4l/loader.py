import usb.core
import usb.util
import videodev2
import errno
import fcntl

dev = usb.core.find(idVendor=0x09cb, idProduct=0x1996)
print(videodev2.hb())
if dev is None:
    raise ValueError('Device not found')

cfg = usb.util.find_descriptor(dev, bConfigurationValue=3)
config = dev.set_configuration(cfg)

if cfg is None:
    raise ValueError('Config not set')

claims = [usb.util.claim_interface(dev, i) for i in range(3)]
vd1 = open("/dev/video2", "r")

if vd1 is None:
    raise ValueError('Video Device /dev/video2 not set')


# cap = v4l2.v4l2_capability()
# fcntl.ioctl(vd1, v4l2.VIDIOC_QUERYCAP, cap)

# format = v4l2.v4l2_format()

# fcntl.ioctl(vd1, v4l2.VIDIOC_G_FMT, format)

# fcntl.ioctl(vd1, v4l2.VIDIOC_S_FMT, format)



# def config_format():
#     linewidth1 = FRAME_WIDTH1
#     framesize1 = FRAME_WIDTH1 * FRAME_HEIGHT1

#     format1.type = V4L2_BUF_TYPE_VIDEO_OUTPUT
#     format1.fmt.pix.width = FRAME_WIDTH1
#     format1.fmt.pix.height = FRAME_HEIGHT1
#     format1.fmt.pix.pixelformat = FRAME_FORMAT1
#     format1.fmt.pix.sizeimage = framesize1
#     format1.fmt.pix.field = V4L2_FIELD_NONE
#     format1.fmt.pix.bytesperline = linewidth1
#     format1.fmt.pix.colorspace = V4L2_COLORSPACE_SRGB