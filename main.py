from machine import Pin, ADC
from time import sleep
from neopixel import NeoPixel

ADCPins = [26,27,28]

class touchPad:
    ch = None
    base = 0
    def __init__(self,pin):
        self.ch = ADC(Pin(pin))
        self.base = self.ch.read_u16()
        
    def calibrate(self):
        self.base = self.ch.read_u16()
        return
        
    def read(self):
        touch = int(max(self.base - self.ch.read_u16(), 0))
        return touch

np = NeoPixel(machine.Pin(18), 2)

tp = [touchPad(p) for p in ADCPins]
sleep(0.1)
[p.calibrate() for p in tp]

while True:
    touch = [min(int(p.read()/20),255) for p in tp]
    print(touch)
    
    np[0] = (touch[0], touch[1], touch[2])
    np[1] = (255-touch[0], 255-touch[1], 255-touch[2])
    np.write()
    
    sleep(0.1)
    