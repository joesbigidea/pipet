
import board
from adafruit_hcsr04 import HCSR04

LEFT_DEPTH_SENSOR_TRIGGER = board.D5
LEFT_DEPTH_SENSOR_ECHO = board.D6

RIGHT_DEPTH_SENSOR_TRIGGER = board.D17
RIGHT_DEPTH_SENSOR_ECHO = board.D18

class DepthSensor:

    def __init__(self, trigger, echo):
        self._sensor = HCSR04(trigger, echo)


    def get_dist_cm(self):
        try:
            return self._sensor.distance
        except RuntimeError:
            return -1


def build_left():
    return DepthSensor(LEFT_DEPTH_SENSOR_TRIGGER, LEFT_DEPTH_SENSOR_ECHO)
    

def build_right():
    return DepthSensor(RIGHT_DEPTH_SENSOR_TRIGGER, RIGHT_DEPTH_SENSOR_ECHO)
