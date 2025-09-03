from machine import Pin, ADC
from time import sleep
from neopixel import NeoPixel

ADCPins = [26,27,28]
NeoPixelPin = 18

class touchPad:
    SENSITIVITY = 5000 # Maximum deviation to ADC count from touching the pad
    THRESHOLD = 0.05

    def __init__(self,pin):
        self.ch = ADC(Pin(pin))
        sleep(0.1)
        self.base = self.ch.read_u16()

    # Read the touchpad and return a value between 0 and 1.0
    def read(self):
        touch = min(max((self.base - self.ch.read_u16())/touchPad.SENSITIVITY,touchPad.THRESHOLD),1.0+touchPad.THRESHOLD)-touchPad.THRESHOLD
        return touch
    
class NeoPixelf:
    OFF = (0,0,0)

    def __init__(self,pin,n):
        self.np = NeoPixel(machine.Pin(pin), n)
        self.np[0] = NeoPixelf.OFF
        self.np[1] = NeoPixelf.OFF
        self.np.write()

    def setHue(self,hues):
        hsvs = [(h,1.0,1.0) for h in hues]
        self.setHSV(hsvs)

    def setHSV(self,hsvs):
        rgbs = [(0,0,0) for n in hsvs]
        for i,hsv in enumerate(hsvs):

            hue = hsv[0]
            s_ = 1.0-hsv[1]
            v = hsv[2]

            if hue < 0:
                rgbs[i] = (1.0*v,s_*v,s_*v)
            elif hue < 0.3333:
                h = hue*3.0
                h_ = 1.0-h
                rgbs[i] = ((h_+h*s_)*v, (h+h_*s_)*v, s_*v)
            elif hue < 0.6666:
                h = (hue-0.3333)*3.0
                h_ = 1.0-h
                rgbs[i] = (s_*v, (h_+h*s_)*v, (h+h_*s_)*v)
            elif hue <= 1.0:
                h = (hue-0.6666)*3.0
                h_ = 1.0-h
                rgbs[i] = ((h+h_*s_)*v, s_*v, (h_+h*s_)*v)
            else:
                rgbs[i] = (1.0*v,s_*v,s_*v)

        self.setRGB(rgbs)
    
    def setRGB(self,rgbs):
        for n in range(self.np.n):
            rgb = rgbs[n] if n < len(rgbs) else rgbs[-1]

            rgbc = [0,0,0]
            for i,c in enumerate(rgb):
                if c < 0.0:
                    rgbc[i] = 0
                elif c <= 1.0:
                    rgbc[i] = int(c*255)
                else:
                    rgbc[i] = 255

            self.np[n] = rgbc
        self.np.write()

            
            


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
np = NeoPixelf(NeoPixelPin, 2)

# Initialise the list of touchpads
tp = [touchPad(p) for p in ADCPins]

hue = 0.0

while True:
    # Read the touchpads
    touch = [p.read() for p in tp]

    np.setHSV([(touch[0],1.0-touch[1],1.0-touch[2])])
    
    # Pause before repeating
    sleep(0.1)
    