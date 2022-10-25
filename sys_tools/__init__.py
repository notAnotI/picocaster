from sys import platform

if platform == "win32":
    from sys_tools.win32_tools import *
    from sys_tools.wall_classes import *
    from sys_tools.sprite_classes import *
    import json
    import math as m
    import time

if platform == "rp2":
    from sys_tools.rp2_tools import *
    from sys_tools.wall_classes import *
    from sys_tools.sprite_classes import *
    from machine import freq
    freq(270000000)
    import ujson as json
    import math as m
    import utime as utime
