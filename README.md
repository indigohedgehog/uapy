# uapy

Python wrapper for Linux UAPI ioctl

## Overview

This project provides a Python wrapper for Linux Media Infrastructure userspace API ioctl requests.

## Support

Current milestone is Linux 5.8.0

## API

* v4l - Video for Linux version 2
* dvb - Digital TV
* rc - Remote Controller
* mediactl - Media Controller
* cec - Consumer Electronics Control

## Example

```python
from uapy.v4l2.videodev import *

cap = V4l2_Capability()
res = fcntl.ioctl(vd1, Vidioc.QUERYCAP, cap)
format = V4l2_Format()
format.type = V4l2_Buf_Type.VIDEO_OUTPUT
```

## Install
```console
user@machine:~$ pip3 install uapy
```
