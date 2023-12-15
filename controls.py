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

def display(message, currentMessage):
    if message != currentMessage:
        lcd.clear()
        lcd.setCursor(0,0) # set cursor position
        lcd.message(message)
        currentMessage = message
        print("displaying message: {message}")
    else:

def is_valid_military_time(input_string):
    pattern = r'^([01]?[0-9]|2[0-3])[0-5][0-9]$'
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
        return '{military_time[:1]}0:00'
    elif len(timeStr) == 2:
        return '{military_time[:2]}:00'
    elif len(timeStr) == 3:
        return '{military_time[:2]}:{military_time[:-1]}0'
    else:
        return '{military_time[:2]}:{military_time[:-2]}'

def loop(isEditing):
    keypad = Keypad.Keypad(keys,rowsPins,colsPins,ROWS,COLS) #creat Keypad object
    keypad.setDebounceTime(50)
    mcp.output(3,1) # turn on LCD backlight 
    lcd.begin(16,2) # set number of LCD lines and columns
    currentMessage = ''

    while(True):
        settings = getSettings()
        if isEditing:
            display(displayedEditTime(timeSetting), currentMessage)
        else:
            if not settings['enabled']:
                display("Disabled", currentMessage)
            elif not settings['feed_at_hour'] or not settings['feed_at_minute']:
                display("Select time", currentMessage)
            else:
                display("{settings['feed_at_hour']}:{settings['feed_at_minute']}", currentMessage)

        timeSetting = ''
        key = keypad.getKey()
        if(key == keypad.NULL):
            continue
        elif key == 'A':
            if not isEditing:
                isEditing = True
            elif not is_valid_military_time(timeSetting):
                display('Invalid time, please clear & try again', currentMessage)
            else:
                # save time, end editing
                minute = parse_minute(timeSetting)
                hour = parse_hour(timeSetting)
                updateFeedingTime(hour, minute)
                isEditing = False
            
        elif key == 'B':
            # cancel select time
            isEditing = False
            timeSetting = ''

        elif key == 'C':
            # clear select time
            timeSetting = ''

        elif key == 'D':
            # enable/disable
            toggleEnabled()

        else:
            if len(timeSetting) >= 4:
                print ("You Pressed Ignored Key: {key}")
                continue
            timeSetting = "{timeSetting}{key}"
            print ("You Pressed Key: {key}")


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
        loop(isEditing)
    except KeyboardInterrupt:
        destroy()