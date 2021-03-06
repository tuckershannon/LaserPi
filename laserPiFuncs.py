import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import math
import sys
from datetime import datetime



class laserPi:
    # GPIO Pin numbbers (BCM)
    StepPins = [4, 17, 27, 22]
    StepPins2 = [5, 6, 13, 19]
    laserPin = 14

    StepCount1 = 8
    Seq = []
    Seq = range(0, StepCount1)

    # Stepper motor sequence
    Seq[0] = [1, 0, 0, 0]
    Seq[1] = [1, 1, 0, 0]
    Seq[2] = [0, 1, 0, 0]
    Seq[3] = [0, 1, 1, 0]
    Seq[4] = [0, 0, 1, 0]
    Seq[5] = [0, 0, 1, 1]
    Seq[6] = [0, 0, 0, 1]
    Seq[7] = [1, 0, 0, 1]

    stepsPerRev = 4096



    def setUpPins():
        GPIO.setwarnings(False)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(laserPin, GPIO.OUT)
        for pin in StepPins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        for pin in StepPins2:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def laser(onOff):
        if onOff:
            GPIO.output(14, True)
        else:
            GPIO.output(14, False)

    def takeStep(motor, direction, seqStep):
        if (motor == 1):
            for pin in range(0, 4):
                xpin = StepPins2[pin]
                if Seq[seqStep][pin] != 0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
        elif (motor == 2):
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq[seqStep][pin] != 0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

        sleep(0.001)

        if (direction == 1):
            if (motor == 2):
                nSteps[0] = nSteps[0] + 1
            if (motor == 1):
                nSteps[1] = nSteps[1] + 1
            if (seqStep == 7):
                return 0
            else:
                return seqStep + 1
        else:
            if (motor == 2):
                nSteps[0] = nSteps[0] - 1
            if (motor == 1):
                nSteps[1] = nSteps[1] - 1

            if (seqStep == 0):
                return 7
            else:
                return seqStep - 1
