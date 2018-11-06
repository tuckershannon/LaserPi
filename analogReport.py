#!/usr/bin/env python
"""
laserPi by Tucker Shannon 2018
thingiverse 3d print files:
https://www.thingiverse.com/thing:2965798
youTube tutorial:
https://www.youtube.com/watch?v=Ll1u_rkKWxM&t=2s
"""

import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import math
import sys
from datetime import datetime

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

StepPins = [4,17,27,22]
StepPins2 = [5,6,13,19]


for pin in StepPins:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

for pin in StepPins2:
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

GPIO.setup(14,GPIO.OUT)
StepCount1 = 8
Seq = []
Seq = range(0, StepCount1)
Seq[0] = [1,0,0,0]
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]


nSteps = range(0,2)

def laser(onOff):
    if onOff:
        GPIO.output(14,True)
    else:
        GPIO.output(14,False)

def takeStep(motor,direction,seqStep):
        if (motor == 1):
            for pin in range(0, 4):
                xpin = StepPins2[pin]
                if Seq[seqStep][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)
        elif (motor == 2):
            for pin in range(0, 4):
                xpin = StepPins[pin]
                if Seq[seqStep][pin]!=0:
                    GPIO.output(xpin, True)
                else:
                    GPIO.output(xpin, False)

        sleep(0.001)

        if(direction == 1):
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







def main():

    drawCircle = []

    angle = 0
    while angle > -360:
        x1 = math.cos(math.radians(angle))
        y1 = math.sin(math.radians(angle))
        angle = angle - 10
        x2 = math.cos(math.radians(angle))
        y2 = math.sin(math.radians(angle))
        drawCircle.append([x1,y1,x2,y2])
    hour = float(datetime.now().strftime('%-I'))
    minutes = float(datetime.now().strftime('%M'))

    #drawHour
    hourTheta = 90.0 - hour * (360.0/12.0) - (minutes/60.0) * (360.0/12.0)
    print "time: ", datetime.now().strftime('%-I:%M')
    print "hourTheta: ", hourTheta
    x1 = math.cos(math.radians(hourTheta + 180.0)) * 0.2
    y1 = math.sin(math.radians(hourTheta + 180.0)) * 0.2
    x2 = math.cos(math.radians(hourTheta )) * 0.5
    y2 = math.sin(math.radians(hourTheta )) * 0.5
    drawHour = [[x1,y1,x2,y2]]

    minuteTheta = 90.0 - (minutes/60.0) * (360.0)
    print "minuteTheta: ", minuteTheta
    x1 = math.cos(math.radians(minuteTheta + 180.0)) * 0.2
    y1 = math.sin(math.radians(minuteTheta + 180.0)) * 0.2
    x2 = math.cos(math.radians(minuteTheta )) * 0.8
    y2 = math.sin(math.radians(minuteTheta )) * 0.8
    drawMinute = [[x1,y1,x2,y2]]

    drawClockSteps = [drawCircle, drawHour, drawMinute]

    seqStepY = 0
    seqStepX = 0
    radPerStep = (2.0 * math.pi)/4076.0;
    currentTheta = 0.0001;
    currentPhi = 0.0001;
    currentX = 0.0;
    currentY = 0.0;
    currentDX = math.sin(radPerStep) / math.cos(currentTheta)
    currentDY = math.sin(radPerStep) / math.cos(currentPhi)

    for lol in range(0,len(drawClockSteps)):
        startX = 0
        letterStart = 0.0
        startPosition = 0
        letter = drawClockSteps[lol]
        for lineDraw in letter:
            for x in range(0,2):
                laser(x)
                nextX = float(lineDraw[x*2])* 0.7
                nextY = float(lineDraw[x*2+1])* 0.7 + 0.3

                dx = currentX - nextX
                dy = currentY - nextY
                stepsX = abs(dx / currentDX) * 2
                stepsY = abs(dy / currentDY) * 2

                if stepsX > stepsY:
                    yStepArray = np.linspace(currentY, nextY, stepsX)
                    xStepArray = np.linspace(currentX, nextX, stepsX)
                else:
                    yStepArray = np.linspace(currentY, nextY, stepsY)
                    xStepArray = np.linspace(currentX, nextX, stepsY)
                for i in range(0,len(xStepArray)):
                    currentX = math.tan(currentTheta)
                    currentY = math.tan(currentPhi)/math.cos(currentTheta)
                    if abs(xStepArray[i]-currentX) > currentDX:
                        if xStepArray[i]-currentX > 0:
                            seqStepX = takeStep(2,1,seqStepX)
                            currentTheta = currentTheta + radPerStep
                        else:
                            seqStepX = takeStep(2,2,seqStepX)
                            currentTheta = currentTheta - radPerStep
                    if abs(yStepArray[i]-currentY) > currentDY:
                        if yStepArray[i]-currentY > 0:
                            seqStepY = takeStep(1,1,seqStepY)
                            currentPhi = currentPhi + radPerStep
                        else:
                            seqStepY = takeStep(1,2,seqStepY)
                            currentPhi = currentPhi - radPerStep
        laser(0)
    while (abs(nSteps[0]) > 0)  or (abs(nSteps[1]) > 0):
        if (nSteps[0] < 0):
            seqStepX = takeStep(2,1,seqStepX)
        elif (nSteps[0] > 0):
            seqStepX = takeStep(2,2,seqStepX)
        if (nSteps[1] < 0):
            seqStepY = takeStep(1,1,seqStepY)
        elif (nSteps[1] > 0):
            seqStepY = takeStep(1,2,seqStepY)

    currentX = 0;
    currentY = 0;
    currentTheta = 0.0001
    currentPhi = 0.0001


    for pin in range(0,4):
        GPIO.output(StepPins[pin],False)
        GPIO.output(StepPins2[pin],False)

if __name__ == "__main__":
    main()
