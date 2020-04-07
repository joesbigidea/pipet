
import time
from adafruit_servokit import ServoKit
from status import status_reporting


class Movement:

    def __init__(self):
        self._kit = ServoKit(channels=16)
        self._left = self._kit.continuous_servo[1]
        self._right = self._kit.continuous_servo[0]    
        self._stop_time = time.time()
        self.stop()
    

    def _go(self, lspeed, rspeed, duration_seconds = 0):
        self._left.throttle = lspeed
        self._right.throttle = rspeed
        self._stop_time = time.time() + duration_seconds
        self.is_moving = True

    
    def go_forward(self, speed, duration_seconds):
        self._go(speed, -speed, duration_seconds)
        status_reporting.log(f"Move: forward {duration_seconds}")


    def go_backward(self, speed, duration_seconds):
        self.go_forward(-speed, duration_seconds)
        status_reporting.log(f"Move: backward {duration_seconds}")


    def turn_left(self, speed, duration_seconds):
        self._go(-speed, -speed, duration_seconds)
        status_reporting.log(f"Turn: left {duration_seconds}")


    def turn_right(self, speed, duration_seconds):
        self._go(speed, speed, duration_seconds)
        status_reporting.log(f"Turn: right {duration_seconds}")


    def stop(self):
        self._go(0, 0)
        self.is_moving = False
        status_reporting.log(f"Stop Moving")


    def left_wheel(self, duration_seconds):
        self._go(1, 0, duration_seconds)

    def is_stopped(self):
        return self.is_moving


    def update(self):
        if self.is_moving and time.time() > self._stop_time:
            self.stop()
