import re
import RPi.GPIO as GPIO
import Keypad
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
from settings import getSettings, updateFeedingTime, toggleEnabled

ROWS = 4
COLS = 4
keys =  [
    '1','2','3','A',    #key code
    '4','5','6','B',
    '7','8','9','C',
    '*','0','#','D'
]

rowsPins = [12,16,18,22]
colsPins = [19,15,13,11]

isEditing = False
isInvalid = False
currentMessage = ''
timeSetting = ''

def display(message):
    lcd.clear()
    lcd.setCursor(0,0) # set cursor position
    if len(message) <= 16:
        lcd.message(message)
    else:
        lcd.message(message[0:14]+'\n')
        lcd.message(message[15:])
    print(f'displaying message: {message}')

def is_valid_military_time(input_string):
    pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, input_string))

def parse_hour(military_time):
    # If the string length is 3, pad with a leading zero
    if len(military_time) == 3:
        military_time = '0' + military_time

    # Extract the hour part from the string
    hour = int(military_time[:2])
    return hour

def parse_minute(military_time):
    # If the string length is 3, pad with a leading zero
    if len(military_time) == 3:
        military_time = '0' + military_time

    # Extract the minute part from the string
    minute = int(military_time[-2:])
    return minute

def displayedEditTime(timeStr):
    if len(timeStr) == 0:
        return '00:00'
    elif len(timeStr) == 1:
        return f'{timeStr[:1]}0:00'
    elif len(timeStr) == 2:
        return f'{timeStr[:2]}:00'
    elif len(timeStr) == 3:
        return f'{timeStr[:2]}:{timeStr[-1:]}0'
    else:
        return f'{timeStr[:2]}:{timeStr[-2:]}'

def loop(isInvalid, isEditing, timeSetting, currentMessage):
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS) #creat Keypad object
    keypad.setDebounceTime(50)
    mcp.output(3,1) # turn on LCD backlight 
    lcd.begin(16,2) # set number of LCD lines and columns

    while(True):
        settings = getSettings()
        # print(settings)
        if isEditing:
            newMessage = 'Feed at: '+displayedEditTime(timeSetting)
            if not isInvalid and newMessage != currentMessage:
                display(newMessage)
                currentMessage = newMessage
        else:
            if not settings['enabled']:
                newMessage = "Disabled"
                if newMessage != currentMessage:
                    display(newMessage)
                    currentMessage = newMessage
            elif settings['feed_at_hour'] == None or settings['feed_at_minute'] == None:
                newMessage = "Press A to      select time"
                if newMessage != currentMessage:
                    display(newMessage)
                    currentMessage = newMessage
            else:
                minutes = settings['feed_at_minute']
                if minutes == 0:
                    minutes = '00'
                newMessage = f"Feeds at {settings['feed_at_hour']}:{minutes}"
                if newMessage != currentMessage:
                    display(newMessage)
                    currentMessage = newMessage

        key = keypad.getKey()
        if key == 'A':
            if isInvalid:
                isInvalid = False
                timeSetting = ''
            elif not isEditing:
                isEditing = True
                isInvalid = False
            elif not is_valid_military_time(displayedEditTime(timeSetting)):
                newMessage = 'Invalid time   Try again'
                isInvalid = True
                if newMessage != currentMessage:
                    display(newMessage)
                    currentMessage = newMessage
            else:
                # save time, end editing
                actualTime = displayedEditTime(timeSetting).replace(":", "")
                minute = parse_minute(actualTime)
                hour = parse_hour(actualTime)
                updateFeedingTime(hour, minute)
                timeSetting = ''
                isEditing = False
                isInvalid = False
            
        elif key == 'B':
            # cancel select time
            isEditing = False
            isInvalid = False
            timeSetting = ''

        elif key == 'C':
            # clear select time
            timeSetting = ''
            isInvalid = False

        elif key == 'D':
            # enable/disable
            toggleEnabled()

        elif(key != keypad.NULL):
            if len(timeSetting) >= 4:
                print (f"You Pressed Ignored Key: {key}")
                continue
            timeSetting = f"{timeSetting}{key}"
            print (f"You Pressed Key: {key}, time setting: {timeSetting}")

        # print(f'current: {currentMessage}')


def destroy():
    lcd.clear()
    GPIO.cleanup()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)


if __name__ == '__main__':
    print ("Program is starting ...")

    try: 
        loop(isInvalid, isEditing, timeSetting, currentMessage)
    except KeyboardInterrupt:
        destroy()