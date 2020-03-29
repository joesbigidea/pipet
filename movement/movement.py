
import time
from adafruit_servokit import ServoKit


class Movement:

    def __init__(self):
        self._kit = ServoKit(channels=16)
        self._left = self._kit.continuous_servo[1]
        self._right = self._kit.continuous_servo[0]    
    

    def _go(self, lspeed, rspeed):
        self._left.throttle = lspeed
        self._right.throttle = rspeed

    
    def go_forward(self, speed):
        self._go(speed, -speed)


    def go_backward(self, speed):
        self.go_forward(-speed)


    def turn_left(self, speed):
        self._go(-speed, -speed)


    def turn_right(self, speed):
        self._go(speed, speed)


    def stop(self):
        self._go(0, 0)


    def left_wheel(self):
        self._go(1, 0)


    def is_stopped(self):
        return self._left.throttle == self._left.throttle == 0
