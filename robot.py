#!/usr/bin/env python3

from vision import motiondetection
from vision.motiondetection2 import MotionDetector
from movement.movement import Movement

import time
#import keyboard

print(f"Starting robot")

#motiondetection.start_motion_detection()
motion_detector = MotionDetector()

print(f"Motion detection started")

movement = Movement()

while True:
#    current_motion = motiondetection.get_current_motion()
    current_motion = motion_detector.detect_motion()

    print(current_motion)

    if current_motion.motion_in_middle():
        print("forward")
        movement.go_forward(1)
        time.sleep(0.5)
        movement.stop()
    elif current_motion.motion_on_left():
        print("left")
        movement.turn_left(1)
        time.sleep(0.2)
        movement.stop()
    elif current_motion.motion_on_right():
        print("right")
        movement.turn_right(1)
        time.sleep(0.2)
        movement.stop()
    else:
        print("no motion")
        #time.sleep(0.2)

    #time.sleep(0.1)

movement.stop()
motiondetection.stop_motion_detection()
