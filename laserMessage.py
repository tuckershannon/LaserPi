#!/usr/bin/env python
"""
laserPi by Tucker Shannon 2018
thingiverse 3d print files:
https://www.thingiverse.com/thing:2965798
youTube tutorial:
https://www.youtube.com/watch?v=Ll1u_rkKWxM&t=2s
"""


from Adafruit_IO import Client
import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import math
import sys
from datetime import datetime


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

with open('LaserPi/font.cxf', 'r') as myFile:
    data = myFile.readlines()

cordDict = {}
for x in range(0,len(data)):
    stuff = data[x].split()
    if stuff != []:
        if '[' in stuff[0]:
            str2 = list(stuff[0])
            key = str2[1]
            points = []
            y = 0
        if 'L' == stuff[0]:
            str2 = stuff[1].split(',')
            points.append(str2)
            y = y + 1
            cordDict[key] = points
        if 'A' == stuff[0]:
            str2 = stuff[1].split(',')
            centerX = float(str2[0])
            centerY = float(str2[1])
            radius = float(str2[2])
            startAngle = float(str2[3])
            endAngle = float(str2[4])
            while int(startAngle) != int(endAngle):
                x1 = math.cos(math.radians(startAngle)) * radius + centerX
                y1 = math.sin(math.radians(startAngle)) * radius + centerY
                startAngle += 1
                if startAngle > 360:
                    startAngle = 0
                x2 = math.cos(math.radians(startAngle)) * radius + centerX
                y2 = math.sin(math.radians(startAngle)) * radius + centerY
                points.append([x1,y1,x2,y2])
            cordDict[key] = points


        if 'AR' == stuff[0]:
            str2 = stuff[1].split(',')
            centerX = float(str2[0])
            centerY = float(str2[1])
            radius = float(str2[2])
            startAngle = float(str2[3])
            endAngle = float(str2[4])
            while int(startAngle) != int(endAngle):
                x1 = math.cos(math.radians(startAngle)) * radius + centerX
                y1 = math.sin(math.radians(startAngle)) * radius + centerY
                startAngle -= 1
                if startAngle < 0:
                    startAngle = 360
                x2 = math.cos(math.radians(startAngle)) * radius + centerX
                y2 = math.sin(math.radians(startAngle)) * radius + centerY
                points.append([x1,y1,x2,y2])
            cordDict[key] = points



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





def main(message):
    seqStepY = 0
    seqStepX = 0
    radPerStep = (2.0 * math.pi)/4076.0;
    currentTheta = 0.0001;
    currentPhi = 0.0001;
    currentX = 0.0;
    currentY = 0.0;

    currentDX = math.sin(radPerStep) / math.cos(currentTheta)
    currentDY = math.sin(radPerStep) / math.cos(currentPhi)
    startX = 0
    letterStart = 0.0
    startPosition = -(((0.4 / 3.0) *  ((float(len(list(message)))/2.0))))
    for letter in list(message):
        currentXLetter = 0.0
        farXLetter = 0.0
        if letter == " ":
            farXLetter = 0.05
        else:
            letter = cordDict[letter]
            for lineDraw in letter:
                for x in range(0,2):
                    laser(x)
                    nextX = float(lineDraw[x*2])  * (0.4 / 18) +  letterStart + startPosition
                    nextY = float(lineDraw[x*2+1])  * (0.4 / 18) #+ (0.30)# * (len(messages)/2.0)
                    if (float(lineDraw[x*2])  * (0.4 / 18)) > farXLetter:
                        farXLetter = (float(lineDraw[x*2])  * (0.4 / 18))
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
        letterStart = letterStart + farXLetter + 0.05



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


if __name__=='__main__':
    sys.exit(main(sys.argv[1]))
