
import random
import digitalio
import audioio
import audiocore
import board
import neopixel
import adafruit_lis3dh
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8, address=0x60)
kit.servo[0].actuation_range=120
kit.servo[1].actuation_range=120
kit.servo[2].actuation_range=120
kit.servo[3].actuation_range=120
kit.servo[4].actuation_range=120
kit.servo[5].actuation_range=120
kit.servo[6].actuation_range=120
kit.servo[7].actuation_range=120

def shiftLeft():
    kit.servo[0].angle=55
    kit.servo[1].angle=15

def shiftRight():
    kit.servo[0].angle=15
    kit.servo[1].angle=55

def stepLeft():
    kit.servo[2].angle=40
    kit.servo[3].angle=60

def stepRight():
    kit.servo[2].angle=70
    kit.servo[3].angle=95

def stand():
    kit.servo[0].angle=35
    kit.servo[1].angle=35
    kit.servo[2].angle=60
    kit.servo[3].angle=70

def balance():
    kit.servo[0].angle=35
    kit.servo[1].angle=35

def walkLeft(sleepSecs):
    shiftRight()
    time.sleep(sleepSecs)
    stepLeft()
    time.sleep(sleepSecs)
    balance()
    time.sleep(sleepSecs)
    stand()
    time.sleep(sleepSecs)

def walkRight(sleepSecs):
    shiftLeft()
    time.sleep(sleepSecs)
    stepRight()
    time.sleep(sleepSecs)
    balance()
    time.sleep(sleepSecs)
    stand()
    time.sleep(sleepSecs)

def walk(sleepSecs):
    walkLeft(sleepSecs)
    walkRight(sleepSecs)

