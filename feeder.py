#!/usr/bin/env python3
########################################################################
# Filename    : Sweep.py
# Description : Servo sweep
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
from datetime import datetime
import time
from settings import getSettings, wasFedToday, updateLastFedDate

OFFSET_DUTY = 0.5        # define pulse offset of servo
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY     # define pulse duty cycle for minimum angle of servo
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY    # define pulse duty cycle for maximum angle of servo
SERVO_DELAY_SEC = 0.001
DEGREES_TO_OPEN_LID = 150
SECONDS_LID_STAYS_OPEN = 3

servoPin = 12
fsrPin = 18

def setup():
    global p
    GPIO.setmode(GPIO.BOARD)         # use PHYSICAL GPIO Numbering
    GPIO.setup(fsrPin, GPIO.IN)      # Set fsrPin to INPUT mode
    GPIO.setup(servoPin, GPIO.OUT)   # Set servoPin to OUTPUT mode
    GPIO.output(servoPin, GPIO.LOW)  # Make servoPin output LOW level

    p = GPIO.PWM(servoPin, 50)     # set Frequence to 50Hz
    p.start(0)                     # Set initial Duty Cycle to 0
    
def servoWrite(angle):      # make the servo rotate to specific angle, 0-180 
    if(angle < 0):
        angle = 0
    elif(angle > 180):
        angle = 180
    dc = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * angle / 180.0 # map the angle to duty cycle
    p.ChangeDutyCycle(dc)


def openLid():
    print('open lid')
    for angle in range(0, DEGREES_TO_OPEN_LID + 1, 1):   # make servo rotate from 0 to 180 deg
        servoWrite(angle)
        time.sleep(SERVO_DELAY_SEC)

def closeLid():
    print('close lid')
    for angle in range(DEGREES_TO_OPEN_LID, -1, -1): # make servo rotate from 180 to 0 deg
        servoWrite(angle)
        time.sleep(SERVO_DELAY_SEC)
    
def loop():
    while True:
        print(f'Current time: {datetime.now()}')

        settings = getSettings()
        if settings['feed_at_hour'] != None:
            minutes = settings['feed_at_minute']
            if minutes == 0:
                minutes = '00'
            # print(f"Setting: {settings['feed_at_hour']}:{minutes}")
        else:
            # print(f'Setting: Not set')


        if not settings['enabled']:
            # print('Feeder disabled')
            continue

        isTimeToFeed = datetime.now().hour == settings['feed_at_hour'] and datetime.now().minute == settings['feed_at_minute']
        if not isTimeToFeed:
            print('Not time to feed')
            continue

        # if wasFedToday():
        #     print('Already fed today')
        #     continue

        # https://pimylifeup.com/raspberry-pi-pressure-pad/
        # bowlHasFood = GPIO.input(fsrPin) > 0
        # if bowlHasFood:
        #     print('Bowl already has food')
        #     updateLastFedDate()
        #     continue

        openLid()

        time.sleep(SECONDS_LID_STAYS_OPEN)
        
        closeLid()
        p.stop()

        updateLastFedDate()


def destroy():
    p.stop()
    GPIO.cleanup()

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
