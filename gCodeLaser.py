import RPi.GPIO as GPIO
import numpy as np
from time import sleep
import math
import sys
from datetime import datetime

import laserPiFuncs


piLaser = laserPiFuncs.laserPi()


piLaser.loadSettings()
