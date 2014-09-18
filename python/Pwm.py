#!/usr/bin/python
# encoding: utf-8
"""
Pwm.py

Created by Alexander Rössler on 2014-03-24.
"""

from PCA9685 import PCA9685

import argparse
import time

import hal


class Pin:
    def __init__(self):
        self.enable = False
        self.value = 0.0
        self.pin = 0
        self.halValuePin = 0
        self.halEnablePin = 0

    def reset(self):
        self.enable = False
        self.value = 0.0


def getHalName(pin):
    return "out-" + '{0:02d}'.format(pin.pin)


parser = argparse.ArgumentParser(description='HAL component to read LSM303 Accelerometer values')
parser.add_argument('-n', '--name', help='HAL component name', required=True)
parser.add_argument('-b', '--bus_id', help='I2C bus id', default=2)
parser.add_argument('-a', '--address', help='I2C device address', default=0x20)
parser.add_argument('-i', '--interval', help='I2C update interval', default=0.05)
args = parser.parse_args()

updateInterval = float(args.interval)
error = False

try:
    pwm = PCA9685(busId=int(args.bus_id),
                    address=int(args.address))
except IOError as e:
    error = True    # if init fails it will be on default values after powerup

# Create pins
pins = []

for i in range(0, 16):
    pin = Pin()
    pin.pin = i
    pins.append(pin)

# Initialize HAL
h = hal.component(args.name)
frequencyValue = 1000
frequencyPin = h.newpin("frequency", hal.HAL_FLOAT, hal.HAL_IN)
for pin in pins:
    pin.halValuePin = h.newpin(getHalName(pin) + ".value", hal.HAL_FLOAT, hal.HAL_IN)
    pin.halEnablePin = h.newpin(getHalName(pin) + ".enable", hal.HAL_BIT, hal.HAL_IN)
halErrorPin = h.newpin("error", hal.HAL_BIT, hal.HAL_OUT)
halNoErrorPin = h.newpin("no-error", hal.HAL_BIT, hal.HAL_OUT)
h.ready()

while (True):
    try:
        if (error):
            pwm.init()
            for pin in pins:
                pin.reset()
            error = False

        if (frequencyPin.value != frequencyValue):
            pwm.setPwmClock(frequencyValue)
            frequencyValue = frequencyPin.value

        for pin in pins:
            if (pin.halEnablePin.value != pin.enable):
                if (pin.halEnablePin.value):
                    pwm.setPwmDuty(pin.pin, pin.value)
                    pin.value = pin.halValuePin.value
                else:
                    pwm.setPwmDuty(pin.pin, 0.0)
                pin.enable = pin.halEnablePin.value

            elif (pin.halValuePin.value != pin.value):
                pwm.setPwmDuty(pin.pin, pin.value)
                pin.value = pin.halValuePin.value
    except IOError as e:
        error = True
    halErrorPin.value = error
    halNoErrorPin.value = not error
    time.sleep(updateInterval)