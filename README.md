# Installation

In raspberry pi terminal:
```
cd ~
git clone https://github.com/larkinwhitaker/rp-ez-feeder
```

### Follow quick steps in tutorial on 110-111 "Configure I2C and Install Smbus":
 - Enable I2C
 - Install I2C-Tools
 - Install Smbus Module

---

# Files

## controls.py
Test by running `$ python controls.py` in terminal
This code takes the input from the matrix keypad to control the feed time and display output to the LCD screen

Controlling settings via keypad:
- A: select/change time
- B: cancel select/change time
- C: clear changing time input
- D: disable/re-enable


## feeder.py
Test by running `$ python feeder.py` in terminal

This code opens/closes the "lid" using a servo motor at the time set by the controls.py


### Test the whole system by running both in 2 different terminal windows

---

## To auto-run this code when the raspberry pi turns on:

```
$ sudo nano /etc/xdg/autostart/ez-feeder-controls.desktop
[Desktop Entry]
Type=Application
Name=EZFeeder-Controls
Exec=/usr/bin/python /home/pi/rp-ez-feeder/controls.py &
```

```
$ sudo nano /etc/xdg/autostart/ez-feeder.desktop
[Desktop Entry]
Type=Application
Name=EZFeeder
Exec=/usr/bin/python /home/pi/rp-ez-feeder/feeder.py &
```

---

## settings.py
This is just a set of helper commands to access/update the user's settings: the feed time, whether its enabled/disabled

Note: These settings are stored in a file called settings.json


These python code files came straight from the Freenove kit:
 - Adafruit_LCD1602.py
 - PCF8574.py
 - Keypad.py

---

# Wiring

## Matrix keypad: (same wiring as tutorial ch 22, note resistors setup)
- 1 (far left): GPIO18
- 2: GPIO23
- 3: GPIO24
- 4: GPIO25
- 5: MOSI
- 6: GPIO22
- 7: GPIO27
- 8: GND

## LCD Screen: (tutorial ch 20 LCD1602)
- 1: GND
- 2: 5V
- 3: SDA1
- 4: SCL1

## Servo (can go backwards - (tutorial ch 15):
- 1: GPIO4
- 2: 5V
- 3: GND

## Force Sensitive Resistor:
https://core-electronics.com.au/guides/force-sensitive-pads-raspberry-pi/
- 1: 5V
- 2: GPIO5 => 10k Resistor => GND
