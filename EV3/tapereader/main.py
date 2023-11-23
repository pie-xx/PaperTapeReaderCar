#!/usr/bin/env pybricks-micropython
#
# 紙テープリーダーとシリアル接続し、送られた文字列をデバッガに表示
#
from pybricks.hubs import EV3Brick
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port
from pybricks.media.ev3dev import SoundFile

# Initialize the EV3
ev3 = EV3Brick()
# Initialize sensor port 1 as a uart device
ser = UARTDevice(Port.S1, baudrate=9600)

msg = b'\r\nHello, I am Mindstroms EV3!\r\n'
ev3.speaker.say(msg.decode('utf-8'))

linebuff = ""
while True:
    data = ser.read(1)
    if data == b'\r':
        print(linebuff)
        linebuff = ""
    elif data == b'\b':
        linebuff = linebuff[:-1]
    else:
        try:
            linebuff = linebuff + data.decode('utf-8')
        except:
            linebuff = linebuff + '*'
