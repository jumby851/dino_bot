
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
    kit.servo[0].angle=50
    kit.servo[1].angle=20

def shiftRight():
    kit.servo[0].angle=20
    kit.servo[1].angle=50

def stepLeft():
    kit.servo[2].angle=30
    kit.servo[3].angle=60

def stepRight():
    kit.servo[2].angle=70
    kit.servo[3].angle=100

def balance():
    kit.servo[0].angle=35
    kit.servo[1].angle=35
    
def stand():
    balance()
    kit.servo[2].angle=50
    kit.servo[3].angle=80

def robotStand():
    balance()
    kit.servo[2].angle=50
    kit.servo[3].angle=80

def dinoStand():
    balance()
    kit.servo[2].angle=25
    kit.servo[3].angle=110

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

def bow():
    kit.servo[2].angle=25
    kit.servo[3].angle=110

def robotHead():
    kit.servo[4].angle=75

def dinoHead():
    kit.servo[4].angle=5

def dinoMouthClose():
    kit.servo[5].angle=30
    
def dinoMouthOpen():
    kit.servo[5].angle=70

def dinoChomp(sleepSecs):
    dinoMouthClose()
    time.sleep(sleepSecs)
    dinoMouthOpen()
    time.sleep(sleepSecs)
    dinoMouthClose()

def robotShoulders():
    kit.servo[6].angle=95
    kit.servo[7].angle=95

def dinoShoulders():
    kit.servo[6].angle=10
    kit.servo[7].angle=10

def robotTransform():
    robotStand()
    robotHead()
    robotShoulders()
    dinoMouthClose()

def dinoTransform():
    dinoStand()
    dinoHead()
    dinoShoulders()
    for i in range(0,2):
        dinoChomp(0.25)
