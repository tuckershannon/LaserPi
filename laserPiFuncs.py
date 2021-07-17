import RPi.GPIO as GPIO
# import numpy as np
from time import sleep
import math


# import sys
# from datetime import datetime


class StepperMotor:
    def __init__(self, stepPins):
        print("setup ")
        print(stepPins)
        self.stepPins = stepPins

        self.stepsPerRev = 4076
        self.nSteps = 0
        self.theta = 0
        self.seq = [[1, 0, 0, 0],
                    [1, 1, 0, 0],
                    [0, 1, 0, 0],
                    [0, 1, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 1],
                    [0, 0, 0, 1],
                    [1, 0, 0, 1]]
        self.seqStep = 0



    def takeStep(self, dir):
        for pin in range(4):
            xpin = self.stepPins[pin]
            if self.seq[self.seqStep][pin] != 0:
                i = 1
                GPIO.output(xpin, True)
            else:
                i = 1
                GPIO.output(xpin, False)
        sleep(0.001)
        if dir == 1:
            self.nSteps += 1
            if self.seqStep == 7:
                self.seqStep = 0
            else:
                self.seqStep += 1
        else:
            self.nSteps -= 1

            if self.seqStep == 0:
                self.seqStep = 7
            else:
                self.seqStep -= 1

        self.theta = float(self.nSteps) / float(self.stepsPerRev) * 2.0 * math.pi


class laserPi:
    # GPIO Pin numbbers (BCM)

    def __init__(self):
        self.motor1 = StepperMotor([5, 6, 13, 19])
        self.motor2 = StepperMotor([4, 17, 27, 22])


    laserPin = 14

    xLimits = [0, 0]
    yLimits = [0, 0]

    def loadSettings(self):
        f = open("ScreenConfig.txt", "r")
        canvasMap = f.read().splitlines()
        self.xLimits = [canvasMap[0], canvasMap[1]]
        self.yLimits = [canvasMap[2], canvasMap[3]]
        print(self.xLimits)
        print(self.yLimits)

    def setUpPins(self):
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.laserPin, GPIO.OUT)
        for pin in [self.motor1.stepPins]:
            GPIO.setup(pin, GPIO.OUT)
        for pin in [self.motor2.stepPins]:
            GPIO.setup(pin, GPIO.OUT)

    def laser(self, onOff):
        if onOff:
            i = 1
            GPIO.output(self.laserPin, True)
        else:
            i = 1
            GPIO.output(self.laserPin, False)
