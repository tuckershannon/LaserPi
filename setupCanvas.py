import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import math
import sys
from datetime import datetime

import laserPiFuncs

import curses


class setUpLaser:
    laserPi = laserPiFuncs.laserPi()
    # get the curses screen window
    screen = curses.initscr()

    yMotorStepCount = 0
    xMotorStepCount = 0
    motorStepSequence1 = 0
    motorStepSequence2 = 0
    didStartCounting = False

    topLeft = [0, 0]
    bottomRight = [0, 0]

    def setUpCanvas(self):
        self.laserPi.setUpPins()

        self.startInstructions()

    def startInstructions(self):
        self.printCenter(
            ["Aim laser straight ahead, level with the horizon", "Press 1 when finished", "Press Q to QUIT"])
        self.waitForKey('1')
        self.didStartCounting = True
        self.printCenter(["Aim laser to top left of canvas", "Press 1 when finished", "Press Q to QUIT"])
        self.waitForKey('1')
        self.topLeft = [self.xMotorStepCount, self.yMotorStepCount]
        self.printCenter(["Aim laser to bottom right canvas", "Press 1 when finished", "Press Q to QUIT"])
        self.waitForKey('1')
        self.bottomRight = [self.xMotorStepCount, self.yMotorStepCount]
        self.writeCustomScreenSettingsToFile()

    def writeCustomScreenSettingsToFile(self):
        print("Writing custom screen")
        f = open("ScreenConfig.txt", "w")

        f.write(str(self.topLeft[0]) + '\n' + str(self.bottomRight[0]) + '\n' + str(self.topLeft[1])+ '\n' + str(self.bottomRight[1]))
        print(self.topLeft)
        print(self.bottomRight)

    def waitForKey(self, key):
        self.setupCurses()
        while True:
            char = self.screen.getch()
            response = self.inputHandler(char, key)
            if response == "finished":
                break

    def setupCurses(self):

        # turn off input echoing
        curses.noecho()

        # respond to keys immediately (don't wait for enter)
        curses.cbreak()
        # map arrow keys to special values
        self.screen.keypad(True)

    def printCenter(self, message):
        dims = self.screen.getmaxyx()
        self.screen.clear()
        for x, _ in enumerate(message):
            self.screen.addstr(int(int(dims[0]) / 2 - 1 + x), int(int(dims[1]) / 2) - int(len(message[x]) / 2),
                               message[x])
        self.screen.refresh()

    def endCurses(self):
        # shut down cleanly
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def takeXSteps(self, motor, direction, x):
        for _ in range(0, x):
            if motor == 1:
                self.motorStepSequence1 = self.laserPi.takeStep(motor, direction, self.motorStepSequence1)
                if self.didStartCounting:
                    if direction == 0:
                        self.yMotorStepCount -= 1
                    else:
                        self.yMotorStepCount += 1
            if motor == 2:
                self.motorStepSequence2 = self.laserPi.takeStep(motor, direction, self.motorStepSequence2)
                if self.didStartCounting:
                    if direction == 0:
                        self.xMotorStepCount -= 1
                    else:
                        self.xMotorStepCount += 1

    def inputHandler(self, char, key):
        xSteps = 5
        if char == ord(key):
            self.endCurses()
            return "finished"
        if char == ord('q'):
            # if q is pressed quit
            self.endCurses()
            exit(0)
            return "quit"
        if char == ord('w'):
            # if q is pressed quit
            self.laserPi.laser(True)
        if char == ord('e'):
            self.laserPi.laser(False)
        elif char == curses.KEY_RIGHT:
            self.takeXSteps(2, 1, xSteps)
        elif char == curses.KEY_LEFT:
            self.takeXSteps(2, 0, xSteps)
        elif char == curses.KEY_UP:
            self.takeXSteps(1, 1, xSteps)
        elif char == curses.KEY_DOWN:
            self.takeXSteps(1, 0, xSteps)
        self.printCenter(["StepX: ", str(self.xMotorStepCount), " StepY: ", str(self.yMotorStepCount)])


startSetup = setUpLaser()
startSetup.setUpCanvas()
