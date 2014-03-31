#!/usr/bin/python
# encoding: utf-8
"""
mperature.py

Created by Alexander Rössler on 2014-03-24.
"""

from ADS7828 import ADS7828
from R2Temp import R2Temp

import argparse
import time

import hal


class Pin:
    pin = 0
    r2temp = 0
    halValuePin = 0
    halRawPin = 0
    filterSamples = []
    filterSize = 10
    rawValue = 0.0

    def __init__(self):
        self.filterSamples = []
        self.rawValue = 0.0

    def addSample(self, value):
        self.filterSamples.append(value)
        if (len(self.filterSamples) > self.filterSize):
            self.filterSamples.pop(0)
        sampleSum = 0.0
        for sample in self.filterSamples:
            sampleSum += sample
        self.rawValue = sampleSum / len(self.filterSamples)


def getHalName(pin):
    return "ch-" + '{0:02d}'.format(pin.pin)


def adc2Temp(pin):
    R1 = 4700.0
    R2 = R1 / max(4095.0 / pin.rawValue - 1.0, 0.000001)
    return round(pin.r2temp.r2t(R2) * 10.0) / 10.0


parser = argparse.ArgumentParser(description='HAL component to read Temperature values over I2C')
parser.add_argument('-n', '--name', help='HAL component name', required=True)
parser.add_argument('-b', '--bus_id', help='I2C bus id', default=2)
parser.add_argument('-a', '--address', help='I2C device address', default=0x20)
parser.add_argument('-i', '--interval', help='I2C update interval', default=0.05)
parser.add_argument('-c', '--channels', help='Komma separated list of channels and thermistors to use e.g. 01:semitec_103GT_2,02:epcos_B57560G1104', required=True)
parser.add_argument('-f', '--filter_size', help='Size of the low pass filter to use', default=10)

args = parser.parse_args()

updateInterval = float(args.interval)
filterSize = int(args.filter_size)

adc = ADS7828(busId=int(args.bus_id),
                address=int(args.address))

# Create pins
pins = []

if (args.channels != ""):
    channelsRaw = args.channels.split(',')
    for channel in channelsRaw:
        pinRaw = channel.split(':')
        if (len(pinRaw) != 2):
            print(("wrong input"))
            exit()
        pin = Pin()
        pin.pin = int(pinRaw[0])
        if ((pin.pin > 7) or (pin.pin < 0)):
            print(("Pin not available"))
            exit()
        pin.r2temp = R2Temp(pinRaw[1])
        pin.filterSize = filterSize
        pins.append(pin)

# Initialize HAL
h = hal.component(args.name)
for pin in pins:
    pin.halRawPin = h.newpin(getHalName(pin) + ".raw", hal.HAL_FLOAT, hal.HAL_OUT)
    pin.halValuePin = h.newpin(getHalName(pin) + ".value", hal.HAL_FLOAT, hal.HAL_OUT)
h.ready()

while (True):
    time.sleep(updateInterval)
    for pin in pins:
        value = float(adc.readChannel(pin.pin))
        pin.addSample(value)
        pin.halRawPin.value = pin.rawValue
        pin.halValuePin.value = adc2Temp(pin)