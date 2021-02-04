import board
import busio
import time
import simpleio
import digitalio
import adafruit_rfm69
from gamepadshift import GamePadShift

print ('mic check')

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D10)
reset = digitalio.DigitalInOut(board.D11)
rfm69 = adafruit_rfm69.RFM69(spi, cs, reset, 915.0)

#  setup for PyBadge buttons
BUTTON_LEFT = const(128)
BUTTON_UP = const(64)
BUTTON_DOWN = const(32)
BUTTON_RIGHT = const(16)
BUTTON_SEL = const(8)
BUTTON_START = const(4)
BUTTON_A = const(2)
BUTTON_B = const(1)

pad = GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
                   digitalio.DigitalInOut(board.BUTTON_LATCH))

current_buttons = pad.get_pressed()
last_read = 0

while True:
    #  checks if button has been pressed
    if (last_read + 0.01) < time.monotonic():
        buttons = pad.get_pressed()
        last_read = time.monotonic()
    if current_buttons != buttons:
        if buttons & BUTTON_START:
            print('pressed START @ %s'%last_read)
            rfm69.send('start')
        elif buttons & BUTTON_SEL:
            print('pressed SELECT @ %s'%last_read)
            rfm69.send('select')
        elif buttons & BUTTON_UP:
            print('pressed UP @ %s'%last_read)
            rfm69.send('forward')
        elif buttons & BUTTON_DOWN:
            print('pressed DOWN @ %s'%last_read)
            rfm69.send('backward')
        elif buttons & BUTTON_LEFT:
            print('pressed LEFT @ %s'%last_read)
            rfm69.send('left')
        elif buttons & BUTTON_RIGHT:
            print('pressed RIGHT @ %s'%last_read)
            rfm69.send('right')
        elif buttons & BUTTON_A and buttons & BUTTON_B:
            print('pressed A & B @ %s'%last_read)
            rfm69.send('special')
        elif buttons & BUTTON_A:
            print('pressed A @ %s'%last_read)
            rfm69.send('A')
        elif buttons & BUTTON_B:
            print('pressed B @ %s'%last_read)
            rfm69.send('B')
    time.sleep(0.01)
