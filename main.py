from machine import Pin, ADC
from time import sleep
from neopixel import NeoPixel

ADCPins = [26,27,28]

class touchPad:
    ch = None
    base = 0
    maxCount = 5000.0 # Maximum deviation to ADC count from touching the pad

    def __init__(self,pin):
        self.ch = ADC(Pin(pin))
        self.base = self.ch.read_u16()
        
    # Read and store an offset to compare against later
    def calibrate(self):
        self.base = self.ch.read_u16()
        return
        
    # Read the touchpad and return a value between 0 and 255
    def readChar(self):
        touch = min(max(int((self.base - self.ch.read_u16())*255/self.maxCount),0),255)
        return touch

    # Read the touchpad and return a value between 0 and 1.0
    def readNorm(self):
        touch = min(max((self.base - self.ch.read_u16())/self.maxCount,0),1.0)
        return touch

# Convert a hue in the range 0-1.0 to RGB values in the range 0-255
def hue2RGB(hue):
    if hue < 0.3333:
        rgb = (255-int(hue*255*3),int(hue*255*3),0)
    elif hue < 0.6666:
        rgb = (0,255-int((hue-0.3333)*255*3),int((hue-0.3333)*255*3))
    else:
        rgb = (int((hue-0.6666)*255*3),0,255-int((hue-0.6666)*255*3))
    return rgb

# Initialise the NeoPixel chain
np = NeoPixel(machine.Pin(18), 2)

# Initialise the list of touchpads
tp = [touchPad(p) for p in ADCPins]
sleep(0.1)
[p.calibrate() for p in tp]

hue = 0.0

while True:
    touch = [p.readNorm() for p in tp]
    hue += touch[0]/10.0
    hue -= touch[1]/10.0
    if hue >= 1.0:
        hue -= 1.0
    if hue <= 0.0:
        hue += 1.0
    rgb = hue2RGB(hue)

    np[0] = rgb
    np[1] = rgb
    np.write()
    
    sleep(0.1)
    