
import board
from adafruit_hcsr04 import HCSR04
from status import status_reporting
import time

LEFT_DEPTH_SENSOR_TRIGGER = board.D5
LEFT_DEPTH_SENSOR_ECHO = board.D6

RIGHT_DEPTH_SENSOR_TRIGGER = board.D17
RIGHT_DEPTH_SENSOR_ECHO = board.D18

class DepthSensor:

    _MEASURE_INTERVAL_SECONDS = 0.01

    def __init__(self, trigger, echo, listener):
        self._sensor = HCSR04(trigger, echo)
        self._listener = listener
        self._previous_result = 0
        self._previous_time = time.time() - self._MEASURE_INTERVAL_SECONDS


    def get_dist_cm(self):
        current_time = time.time()
        if current_time - self._previous_time < self._MEASURE_INTERVAL_SECONDS:
            return self._previous_result

        for i in range(0, 5):
            try:
                self._previous_result = self._sensor.distance
                self._previous_time = current_time
                self._listener(self._previous_result)
                return self._previous_result
            except RuntimeError:
                pass

        return self._previous_result


def build_left():
    return DepthSensor(LEFT_DEPTH_SENSOR_TRIGGER, LEFT_DEPTH_SENSOR_ECHO, status_reporting.left_depth_listener)
    

def build_right():
    return DepthSensor(RIGHT_DEPTH_SENSOR_TRIGGER, RIGHT_DEPTH_SENSOR_ECHO, status_reporting.right_depth_listener)
