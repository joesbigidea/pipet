#!/usr/bin/env python3

from vision import motiondetection
from movement.movement import Movement

import time
#import keyboard

print(f"Starting robot")

motiondetection.start_motion_detection()
print(f"Motion detection started")

while True:
    current_motion = motiondetection.get_current_motion()
    print(current_motion)
    time.sleep(0.1)

motiondetection.stop_motion_detection()
