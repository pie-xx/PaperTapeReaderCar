#!/usr/bin/env pybricks-micropython
#
# PCとシリアル接続し、PCから送られた文字列を行単位で音声出力する
#
from pybricks.hubs import EV3Brick
from pybricks.iodevices import UARTDevice
from pybricks.parameters import Port
from pybricks.media.ev3dev import SoundFile

# Initialize the EV3
ev3 = EV3Brick()
# Initialize sensor port 1 as a uart device
ser = UARTDevice(Port.S1, baudrate=115200)

msg = b'\r\nHello, I am Mindstroms EV3!\r\n'
prompt = b'= '

ser.write(msg)
ev3.speaker.say(msg.decode('utf-8'))
ser.write(prompt)

linebuff = ""
while True:
    data = ser.read(1)
    if data == b'\r':
        ser.write(b'\r\n')
        ev3.speaker.say(linebuff)
        print(linebuff)
        linebuff = ""
        ser.write(prompt)
    elif data == b'\b':
        ser.write(b'\b \b')
        linebuff = linebuff[:-1]
    else:
        ser.write(data)
        try:
            linebuff = linebuff + data.decode('utf-8')
        except:
            linebuff = linebuff + '*'
