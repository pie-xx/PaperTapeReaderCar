import time
import machine
from machine import Pin, I2C, UART
import utime
import math


class PCA9685:
    # Registers/etc.
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALLLED_ON_L        = 0xFA
    __ALLLED_ON_H        = 0xFB
    __ALLLED_OFF_L       = 0xFC
    __ALLLED_OFF_H       = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=100000)
        self.address = address
        self.debug = debug
        if (self.debug):
            print("Reseting PCA9685") 
        self.write(self.__MODE1, 0x00)
	
    def write(self, cmd, value):
        "Writes an 8-bit value to the specified register/address"
        self.i2c.writeto_mem(int(self.address), int(cmd), bytes([int(value)]))
        if (self.debug):
            print("I2C: Write 0x%02X to register 0x%02X" % (value, cmd))
	  
    def read(self, reg):
        "Read an unsigned byte from the I2C device"
        rdate = self.i2c.readfrom_mem(int(self.address), int(reg), 1)
        if (self.debug):
            print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" % (self.address, int(reg), rdate[0]))
        return rdate[0]
	
    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        if (self.debug):
            print("Setting PWM frequency to %d Hz" % freq)
            print("Estimated pre-scale: %d" % prescaleval)
        prescale = math.floor(prescaleval + 0.5)
        if (self.debug):
            print("Final pre-scale: %d" % prescale)

        oldmode = self.read(self.__MODE1)
        #print("oldmode = 0x%02X" %oldmode)
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.write(self.__MODE1, newmode)        # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.write(self.__LED0_ON_L+4*channel, on & 0xFF)
        self.write(self.__LED0_ON_H+4*channel, on >> 8)
        self.write(self.__LED0_OFF_L+4*channel, off & 0xFF)
        self.write(self.__LED0_OFF_H+4*channel, off >> 8)
        if (self.debug):
            print("channel: %d  LED_ON: %d LED_OFF: %d" % (channel,on,off))
	  
    def setServoPulse(self, channel, pulse):
        pulse = pulse * (4095 / 100)
        self.setPWM(channel, 0, int(pulse))
    
    def setLevel(self, channel, value):
        if (value == 1):
              self.setPWM(channel, 0, 4095)
        else:
              self.setPWM(channel, 0, 0)

class MotorDriver():
    def __init__(self, debug=False):
        self.debug = debug
        self.pwm = PCA9685()
        self.pwm.setPWMFreq(50)       
        self.MotorPin = ['MA', 0,1,2, 'MB',3,4,5, 'MC',6,7,8, 'MD',9,10,11]
        self.MotorDir = ['forward', 0,1, 'backward',1,0]

    def MotorRun(self, motor, mdir, speed, runtime):
        if speed > 100:
            return
        
        mPin = self.MotorPin.index(motor)
        mDir = self.MotorDir.index(mdir)
        
        if (self.debug):
            print("set PWM PIN %d, speed %d" %(self.MotorPin[mPin+1], speed))
            print("set pin A %d , dir %d" %(self.MotorPin[mPin+2], self.MotorDir[mDir+1]))
            print("set pin b %d , dir %d" %(self.MotorPin[mPin+3], self.MotorDir[mDir+2]))

        self.pwm.setServoPulse(self.MotorPin[mPin+1], speed)        
        self.pwm.setLevel(self.MotorPin[mPin+2], self.MotorDir[mDir+1])
        self.pwm.setLevel(self.MotorPin[mPin+3], self.MotorDir[mDir+2])

        if runtime > 0:
            time.sleep(runtime)
            self.pwm.setServoPulse(self.MotorPin[mPin+1], 0)
            self.pwm.setLevel(self.MotorPin[mPin+2], 0)
            self.pwm.setLevel(self.MotorPin[mPin+3], 0)

    def MotorStop(self, motor):
        mPin = self.MotorPin.index(motor)
        self.pwm.setServoPulse(self.MotorPin[mPin+1], 0)


time.sleep(1)
uart = UART(0, 9600)
led = machine.Pin(25, machine.Pin.OUT)
startbtn = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_DOWN)
m = MotorDriver()
m.MotorStop('MA')
m.MotorStop('MB')
m.MotorStop('MC')


def btntest():
    global uart, startbtn
    while True:
        c = uart.read(1)
        if c!= None:
            try:
                c.decode('utf-8')
            except:
                print("error")
                print(c)
                errordisp()
                uart = UART(0, 9600)
                time.sleep(0.5)
        led.value(0)
        if startbtn.value()==1:
            print("start")
            time.sleep(0.5)
            break
        time.sleep(0.1)
        led.value(1)
        time.sleep(0.1)
        
def errordisp():
    for i in range(3):
        led.value(1)
        time.sleep(0.5)
        led.value(0)
        time.sleep(0.2)

if __name__ == '__main__':
    #time.sleep(1)
    btntest()
    print("ttest code")
    try:
     
        #Parameter 1: motor select:'MA', 'MB', 'MC', 'MD'
        #Parameter 2: turn dir:'forward', 'backward'
        #Parameter 3: motor speed: 0-100
        #Parameter 4: Running time: >0

        print("motor A backward, speed 10%")
        m.MotorRun('MA', 'backward', 50, 0)

        s=[0,0,0,0,0,0,0,0,-1]
        ss=""
        sinx=0
        while True:
            c = uart.read(1)
            if c!= None:
                try:
                    ss=ss+c.decode('utf-8')
                except:
                    print("error!")
                    print(c)
                    m.MotorStop('MA')
                    m.MotorStop('MB')
                    m.MotorStop('MC')
                    errordisp()
                    uart = UART(0, 9600)
                    time.sleep(0.5)
                    ss=""
                    break
            if c==b'\n':
                sinx = 0
                ss = ""
                print(s)
                if s[1] > 50 or s[2] > 50 or s[3] > 50:
                    m.MotorRun('MB', 'forward', 100, 0)
                else:
                    m.MotorStop('MB')
                if s[5] > 50 or s[6] > 50 or s[7] > 50:
                    m.MotorRun('MC', 'forward', 100, 0)
                else:
                    m.MotorStop('MC')
            if c==b'\t':
                try:
                    s[sinx] = int(ss)
                except:
                    print("error",ss)
                ss=""
                sinx = sinx + 1
            if startbtn.value()==1:
                m.MotorStop('MA')
                m.MotorStop('MB')
                m.MotorStop('MC')
                time.sleep(2)
                btntest()
                print("restart")
                m.MotorRun('MA', 'backward', 10, 0)
                s=[0,0,0,0,0,0,0,0,-1]
                ss=""
                sinx=0

    except KeyboardInterrupt:
        m.MotorStop('MA')

