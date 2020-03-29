#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)


kit.continuous_servo[2].throttle = 1
time.sleep(5)
kit.continuous_servo[2].throttle = 0