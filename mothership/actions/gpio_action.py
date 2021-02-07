"""
If running on a pi, then the first import will work. Otherwise it'll
use the fake gpio so that compilation works.

usage:

import mothership.actions.gpio_action as gpio_x
mothership.add_action('foogle', gpio_x.TogglePin(25))
"""

import importlib.util
try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO
from mothership.action import Action

class SetPin(Action):
    pin:int
    on:bool

    def execute(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH if self.on else GPIO.LOW)

class TogglePin(Action):
    pin:int

    def execute(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, not GPIO.input(self.pin))

class Cleanup(Action):

    def execute(self):
        GPIO.cleanup()