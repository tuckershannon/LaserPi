#!/usr/bin/env python
from Adafruit_IO import Client
import sys
sys.path.insert(0, '/home/pi/')
import weatherReport
import timeReport
import analogReport
import laserMessage
from time import sleep

aio = Client('e69763443f284a9cbcd7463ac7d93481')
#print "working"

while True:
    try:
        laserText = aio.receive('textBox')
        break
    except:
          print('connection error')


while True:
    try:
        timeButton = aio.receive('time')
        weatherButton = aio.receive('weather')
        analogButton = aio.receive('analog')
        messageReceived = aio.receive('textBox')
        if weatherButton.value != '0':
            weatherReport.main()
            aio.send('weather', 0)
            sleep(2)
        if analogButton.value != '0':
            analogReport.main()
            aio.send('analog', 0)
            sleep(2)
        if timeButton.value != '0':
            timeReport.main()
            aio.send('time', 0)
            sleep(2)
        if laserText != messageReceived:
            laserText = messageReceived
            laserMessage.main(laserText.value)

    except:
       print('connection error')
