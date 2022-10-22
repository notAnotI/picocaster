from sys import platform

if platform == "win32":
    from sys_tools.win32_tools import *
    import json
    import math as m
    import time

if platform == "rp2":
    from sys_tools.rp2_tools import *
    from machine import freq
    freq(270000000)
    import ujson as json
    import math as m
    import utime as utime
