#!/usr/bin/python
# encoding: utf-8
"""
Storage.py

Created by Alexander Rössler on 2015-01-03.
"""

import time
import sys
import argparse

import ConfigParser

import hal


class Pin:
    def __init__(self):
        self.halPin = 0
        self.halName = ''
        self.section = ''
        self.name = ''
        self.lastValue = 0.0
        
        
def savePins(cfg, filename, pins):
    for pin in pins:
        cfg.set(pin.section, pin.name, str(pin.halPin.value))
    with open(filename, 'w') as f:
        cfg.write(f)
        f.close()
        
parser = argparse.ArgumentParser(description='HAL component to store and load values')
parser.add_argument('-n', '--name', help='HAL component name', required=True)
parser.add_argument('-f', '--file', help='Filename to store values', required=True)
parser.add_argument('-x', '--on_exit', help='Save on exit', action='store_true')
parser.add_argument('-a', '--autosave', help='Automatically save on value change', action='store_true')
parser.add_argument('-i', '--interval', help='Update interval', default=1.00)

args = parser.parse_args()

updateInterval = float(args.interval)
autosave = args.autosave
saveOnExit = args.on_exit
filename = args.file

# Create pins
pins = []

cfg = ConfigParser.ConfigParser()
cfg.read(filename)
h = hal.component(args.name)
for section in cfg.sections():
    for item in cfg.items(section):
        pin = Pin()
        pin.section = section
        pin.name = item[0]
        pin.halName = section.lower() + '.' + item[0].lower()
        pin.lastValue = float(item[1])
        pin.halPin = h.newpin(pin.halName, hal.HAL_FLOAT, hal.HAL_IO)
        pin.halPin.value = pin.lastValue
        pins.append(pin)
h.ready()

try:
    while (True):
        if autosave:
            for pin in pins:
                if pin.halPin.value != pin.lastValue:
                    pin.lastValue = pin.halPin.value
                    savePins(cfg, filename, pins)
        time.sleep(updateInterval)
except KeyboardInterrupt:
    if saveOnExit:
        savePins(cfg, filename, pins)
    print(("exiting HAL component " + args.name))
    h.exit()
