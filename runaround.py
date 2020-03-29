#!/usr/bin/env python3

import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

left = kit.continuous_servo[0]
right = kit.continuous_servo[1]


left.throttle = 1
right.throttle = -1

time.sleep(1)

left.throttle = 0
right.throttle = 0

time.sleep(1)

left.throttle = 1
right.throttle = 1

time.sleep(2)

left.throttle = 1
right.throttle = -1

time.sleep(2)

left.throttle = 0
right.throttle = 0
