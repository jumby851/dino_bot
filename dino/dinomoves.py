
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
kit.servo[0].actuation_range=120 # left ankle
kit.servo[1].actuation_range=120 # right ankle
kit.servo[2].actuation_range=120 # left hip
kit.servo[3].actuation_range=120 # right hip
kit.servo[4].actuation_range=120 # neck
kit.servo[5].actuation_range=120 # dino mouth
kit.servo[6].actuation_range=120 # left shoulder
kit.servo[7].actuation_range=120 # right shoulder

def slowMove(servoAngleTuples, timeDelay=0.005, increments=25):
    servoAngleIncrementTuples = []
    for servoAngleTuple in servoAngleTuples:
        servo,angle = servoAngleTuple
        totalDiff = angle - kit.servo[servo].angle
        angleIncrement = totalDiff / increments
        servoAngleIncrementTuples.append((servo,angle,angleIncrement))
        print("slow move: servo %s, newAngle %s, oldAngle %s, angleInc %s"%(servo,angle,kit.servo[servo].angle,angleIncrement))

    for i in range(0,increments):
        for servo,angle,angleIncrement in servoAngleIncrementTuples:
            currentAngle=kit.servo[servo].angle
            updatedAngle=currentAngle+angleIncrement
            kit.servo[servo].angle=updatedAngle
        time.sleep(timeDelay)

def move(servoAngleTuples):
    slowMove(servoAngleTuples, timeDelay=0, increments=1)

def shiftLeft():
    kit.servo[0].angle=50
    kit.servo[1].angle=20

def shiftRight():
    kit.servo[0].angle=20
    kit.servo[1].angle=50

def stepLeft():
    kit.servo[2].angle=70
    kit.servo[3].angle=60

def stepRight():
    kit.servo[2].angle=110
    kit.servo[3].angle=100

def balance():
    kit.servo[0].angle=35
    kit.servo[1].angle=35

def stand():
    balance()
    kit.servo[2].angle=85
    kit.servo[3].angle=85

def robotStand():
    balance()
    slowMove([(2,85),(3,85)])

def dinoStand():
    balance()
    slowMove([(2,65),(3,110)])

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
    slowMove([(4,75)])

def dinoHead():
    slowMove([(4,5)])

def dinoMouthClose():
    slowMove([(5,30)], timeDelay=0.01, increments=20)

def dinoMouthOpen():
    slowMove([(5,70)], timeDelay=0.01, increments=20)

def dinoChomp(sleepSecs):
    dinoMouthOpen()
    time.sleep(sleepSecs)
    dinoMouthClose()

def robotShoulders():
    slowMove([(6,95),(7,95)])

def dinoShoulders():
    slowMove([(6,10),(7,10)])

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
        dinoChomp(0)
