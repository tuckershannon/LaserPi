# import RPi.GPIO as GPIO
# import numpy as np
# from time import sleep
import math
# import sys
# from datetime import datetime

# import laserPiFuncs
from pygcode import Line, Machine


class gCodeLaser:

    def __init__(self, filePath):
        self.currentTheta = 0.0  # bottom motor
        self.currentPhi = 0.0  # top motor
        self.radPerStep = (2.0 * math.pi) / 4076.0
        # self.piLaser = laserPiFuncs.laserPi()
        # self.piLaser.loadSettings()
        self.traj = []
        self.laserIsOn = []
        self.pathTaken = []
        self.currentPos = []
        self.readGcode(filePath)
        self.yMotorStepCount = 0
        self.xMotorStepCount = 0
        self.motorStepSequence1 = 0
        self.motorStepSequence2 = 0
        self.xMax = 0
        self.yMax = 0
        self.multiplyer = 0
        self.offset = 0

    def readGcode(self, filePath):
        m = Machine()
        with open(filePath, 'r') as fh:
            for line_text in fh.readlines():
                line = Line(line_text)
                m.process_block(line.block)
                if line.gcodes != []:
                    self.traj.append((m.pos.values['X'], m.pos.values['Y']))
                    if str(m.mode.gcodes[0]) == "G00":
                        self.laserIsOn.append(False)
                    else:
                        self.laserIsOn.append(True)
        xPoints = [x[0] for x in self.traj]
        yPoints = [x[1] for x in self.traj]
        self.xMax = max(xPoints)
        self.yMax = max(yPoints)

        # theta1 = self.piLaser.xLimits[0]/4076.0
        # theta2 = self.piLaser.xLimits[1]/4076.0

        theta1 = -200.0 / 4076.0
        theta2 = 200 / 4076.0

        self.multiplyer = self.xMax / (math.tan(theta2) - math.tan(theta1))
        self.offset = -(self.multiplyer * math.tan(theta1))

        # self.print("ok")

    def getPosition(self):
        xPos = self.multiplyer * math.tan(self.currentTheta) + self.offset
        yPos = self.multiplyer * ()

    def returnHome(self):
        self.goToPosition(0, 0)

    def goToPosition(self, x, y):
        print("going")


#
# currentX = math.tan(currentTheta)  #
# currentY = math.tan(currentPhi) / math.cos(currentTheta)
new = gCodeLaser('test.gcode')
