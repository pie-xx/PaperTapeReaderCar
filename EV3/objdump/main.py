#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import UARTDevice
from pybricks.nxtdevices import VernierAdapter
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

import pybricks
import machine

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

def recursive_dir(obj, pname="", depth=0, max_depth=6):
    # 再帰の深さがmax_depthを超えたら終了
    if depth > max_depth:
        return

    # オブジェクト名とタイプを表示
    print('  ' * depth + pname + " " + str(obj) )

    # オブジェクトの属性一覧を取得
    attributes = dir(obj)

    if( len(attributes) < 2 ):
        return

    if( not str(obj).startswith("<") ):
        return

    # 属性値がオブジェクトなら再帰的に属性を調べる

    for attribute in attributes:
        if( attribute == '__class__'):
              continue
        if( attribute == '__name__'):
              continue
        if( attribute == '__path__'):
              continue

        # 属性値を取得
        if hasattr(obj, attribute):
            attr_value = getattr(obj, attribute)
            recursive_dir(attr_value, attribute, depth + 1, max_depth)



# Create your objects here.
ev3 = EV3Brick()

ev3.speaker.say("Hello, I am LEGO Mindstorms EV3.")

ev3.speaker.say("Dump pybricks.")
recursive_dir(pybricks)

ev3.speaker.say("Dump machine.")
recursive_dir(machine)

ev3.speaker.say("Dump EV3Brick()")
recursive_dir(EV3Brick())

ev3.speaker.say("Job finished.")
