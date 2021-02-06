import RPi.GPIO as GPIO
from mothership.action import Action

class Led(Action):
    pin:int
    on:bool

    def execute(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.HIGH if self.on else GPIO.LOW)