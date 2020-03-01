import time
import signal

from gfxhat import touch, lcd, backlight, fonts
from PIL import Image, ImageFont, ImageDraw

from pyo import *

def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def midi_2s_complement(value):
    if value <= 64:
        return value
    else:
        return value - 128

class Midiencoder(PyoObject):
    def __init__(self, ctlnumber, minscale=0, maxscale=1, init=0, encoder_step=8, step=0.01):
        PyoObject.__init__(self)
        self._value = init
        self._ctlnumber = ctlnumber
        self._minscale = minscale
        self._maxscale = maxscale
        self._encoder_step = encoder_step
        self._step = step
        self._raw = RawMidi(self.handle_midi)
        self._midi = Midictl(-1, minscale, maxscale, init)
        self._base_objs = self._midi.getBaseObjects()
        self._init_play()


    def handle_midi(self, status, data1, data2):
        if data1 == self._ctlnumber:
            self._midi.setValue(
                clamp(
                    self._midi.get() + self._step * midi_2s_complement(data2) / self._encoder_step,
                    self._minscale,
                    self._maxscale
                )
            )

# led_states = [False for _ in range(6)]

# width, height = lcd.dimensions()

# font = ImageFont.truetype(fonts.Bitbuntu, 10)

# backlight.set_all(255, 255, 255)
# backlight.show()

# param1 = 0
# param2 = 0
# param3 = 0
# param4 = 0

# def draw_text((x, y), text):
#     w, h = font.getsize(text)

#     image = Image.new('P', (w, h))
#     draw = ImageDraw.Draw(image)

#     draw.text((0, 0), text, 1, font)

#     for ix in range(w):
#         for iy in range(h):
#             pixel = image.getpixel((ix, iy))
#             lcd.set_pixel(ix + x, iy + y, pixel)

# def draw():
#     draw_text((0, 0), str(param1).rjust(3))
#     draw_text((20, 0), str(param2).rjust(3))
#     draw_text((40, 0), str(param3).rjust(3))
#     draw_text((60, 0), str(param4).rjust(3))

#     lcd.show()

# draw()
 
# midiin = rtmidi.RtMidiIn()




# def handle_midi(message):
#     if message.isController():
#         controller = message.getControllerNumber()
#         value = message.getControllerValue()

#         if controller == 22:
#             global param1
#             param1 = clamp(param1 + midi_2s_complement(value) / 8, 0, 100)
#         elif controller == 23:
#             global param2
#             param2 = clamp(param2 + midi_2s_complement(value) / 8, 0, )
#         elif controller == 24:
#             global param3
#             param3 = clamp(param3 + midi_2s_complement(value) / 8, 0, 100)
#         elif controller == 25:
#             global param4
#             param4 = clamp(param4 + midi_2s_complement(value) / 8, 0, 100)
    
#     draw()

# ports = range(midiin.getPortCount())
# if ports:
#     midiin.openPort(1)
#     midiin.setCallback(handle_midi)
# else:
#     print('NO MIDI INPUT PORTS!')

# pyo.pa_list_devices()
# print(pyo.pa_get_default_output())
s = Server(audio='jack', duplex=0)
s.setMidiInputDevice(99)
s.boot()
s.start()

from os import path

m = Midiencoder(22, minscale = 110, maxscale = 440, init = 220, step=10)
si = Sine(freq = m).out()

# while 1:
#     pass

try:
    signal.pause()
except KeyboardInterrupt:
    s.stop()
    # for x in range(6):
    #     backlight.set_pixel(x, 0, 0, 0)
    #     touch.set_led(x, 0)
    # backlight.show()
    # lcd.clear()
    # lcd.show()
