
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

    motorStepSequence1 = 0
    motorStepSequence2 = 0




    def setUpCanvas(self):
        self.laserPi.setUpPins()
        self.useKeys()




    def __useKeys(self):
        self.setupCurses()
        while True:
            char = self.screen.getch()
            response = self.inputHandler(char)
            if response == "finished":
                break


        self.endCurses()

    def __setupCurses(self):

        # turn off input echoing
        curses.noecho()

        # respond to keys immediately (don't wait for enter)
        curses.cbreak()

        # map arrow keys to special values
        self.screen.keypad(True)

    def __endCurses(self):
        # shut down cleanly
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()


    def __inputHandler(self, char):
        if char == ord('q'):
            # if q is pressed quit
            return "finished"
        if char == ord('w'):
            # if q is pressed quit
            self.laserPi.laser(True)
        if char == ord('e'):
            self.laserPi.laser(False)
        elif char == curses.KEY_RIGHT:
            self.screen.addstr(0, 0, 'right ')
            self.motorStepSequence1 = self.laserPi.takeStep(1 ,0 ,self.motorStepSequence1)
        elif char == curses.KEY_LEFT:
            self.screen.addstr(0, 0, 'left ')
            self.motorStepSequence1 = self.laserPi.takeStep(1 ,1 ,self.motorStepSequence1)
        elif char == curses.KEY_UP:
            self.screen.addstr(0, 0, 'up ')
            self.motorStepSequence2 = self.laserPi.takeStep(0 ,0 ,self.motorStepSequence2)
        elif char == curses.KEY_DOWN:
            self.screen.addstr(0, 0, 'down ')
            self.motorStepSequence2 = self.laserPi.takeStep(0 ,1 ,self.motorStepSequence2)



startSetup = setUpLaser()
startSetup.setUpCanvas()
