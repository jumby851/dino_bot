
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

DEFAULT_INCREMENTS=25

def move(servoAngleTuples):
    for servo,angle in servoAngleTuples:
        kit.servo[servo].angle=angle

def slowMove(servoAngleTuples, timeDelay=0.005, increments=DEFAULT_INCREMENTS):
    if(increments <= 1):
        move(servoAngleTuples)
        return

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

def shiftLeft(increments=DEFAULT_INCREMENTS):
    slowMove([(0,50),(1,20)],increments=increments)

def shiftRight(increments=DEFAULT_INCREMENTS):
    slowMove([(0,20),(1,50)], increments=increments)

def stepLeft(increments=DEFAULT_INCREMENTS):
    slowMove([(2,60),(3,50)], increments=increments)

def stepRight(increments=DEFAULT_INCREMENTS):
    slowMove([(2,110),(3,100)], increments=increments)

def balance(increments=DEFAULT_INCREMENTS):
    slowMove([(0,35),(1,35)], increments=increments)

def stand(increments=DEFAULT_INCREMENTS):
    balance(increments)
    slowMove([(2,85),(3,85)], increments=increments)

def robotStand(increments=DEFAULT_INCREMENTS):
    balance(increments)
    slowMove([(2,85),(3,85)], increments=increments)

def dinoStand(increments=DEFAULT_INCREMENTS):
    balance(increments)
    slowMove([(2,65),(3,110)], increments=increments)

def walkLeft(increments=DEFAULT_INCREMENTS):
    shiftRight(increments)
    stepLeft(increments)
    balance(increments)
    stand(increments)

def walkRight(increments=DEFAULT_INCREMENTS):
    shiftLeft(increments)
    stepRight(increments)
    balance(increments)
    stand(increments)

def walk(increments=DEFAULT_INCREMENTS):
    walkLeft(increments)
    walkRight(increments)

def robotHead(increments=DEFAULT_INCREMENTS):
    slowMove([(4,75)], increments=increments)

def dinoHead(increments=DEFAULT_INCREMENTS):
    slowMove([(4,5)], increments=increments)

def dinoMouthClose(increments=DEFAULT_INCREMENTS):
    slowMove([(5,30)], timeDelay=0.01, increments=increments)

def dinoMouthOpen(increments=DEFAULT_INCREMENTS):
    slowMove([(5,70)], timeDelay=0.01, increments=increments)

def dinoChomp(increments=DEFAULT_INCREMENTS):
    dinoMouthOpen(increments)
    dinoMouthClose(increments)

def robotShoulders(increments=DEFAULT_INCREMENTS):
    slowMove([(6,95),(7,95)], increments=increments)

def dinoShoulders(increments=DEFAULT_INCREMENTS):
    slowMove([(6,10),(7,10)], increments=increments)

def robotTransform(increments=DEFAULT_INCREMENTS):
    robotStand(increments)
    robotHead(increments*2)
    robotShoulders(increments)
    dinoMouthClose(increments)

def dinoTransform(increments=DEFAULT_INCREMENTS):
    dinoStand(increments)
    dinoHead(increments*2)
    dinoShoulders(increments)
    for i in range(0,2):
        dinoChomp(increments)

def dance(increments=DEFAULT_INCREMENTS):
    stand(increments)
    for i in range(0,4):
        shiftLeft(increments)
        shiftRight(increments)
        slowMove([(6,60),(7,60)], increments=increments)
        slowMove([(6,30),(7,30)], increments=increments)
    stand(increments)
