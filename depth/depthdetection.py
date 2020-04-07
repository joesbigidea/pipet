
import board
from adafruit_hcsr04 import HCSR04
from status import status_reporting

LEFT_DEPTH_SENSOR_TRIGGER = board.D5
LEFT_DEPTH_SENSOR_ECHO = board.D6

RIGHT_DEPTH_SENSOR_TRIGGER = board.D17
RIGHT_DEPTH_SENSOR_ECHO = board.D18

class DepthSensor:

    def __init__(self, trigger, echo, listener):
        self._sensor = HCSR04(trigger, echo)
        self._listener = listener


    def get_dist_cm(self):
        try:
            dist = self._sensor.distance
            self._listener(dist)
            return dist
        except RuntimeError:
            return -1


def build_left():
    return DepthSensor(LEFT_DEPTH_SENSOR_TRIGGER, LEFT_DEPTH_SENSOR_ECHO, status_reporting.left_depth_listener)
    

def build_right():
    return DepthSensor(RIGHT_DEPTH_SENSOR_TRIGGER, RIGHT_DEPTH_SENSOR_ECHO, status_reporting.right_depth_listener)
