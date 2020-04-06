#!/usr/bin/env python3

from vision import motiondetection
from vision.motiondetection import MotionDetector
from movement.movement import Movement
from depth import depthdetection

import time

class Robot:
    
    def __init__(self):
        self.log = print
        self.motion_listener = lambda m : print(f"Motion: {m}")
        self.left_depth_listener = lambda d : print(f"Depth 1: {d}")
        self.right_depth_listener = lambda d : print(f"Depth 2: {d}")
        self.quit_monitor = lambda: False


    def start(self):
        self.motion_detector = MotionDetector(self.log)
        self.movement = Movement()
        self.log(f"Motion detection started")
        self.left_depth_detector = depthdetection.build_left()
        self.right_depth_detector = depthdetection.build_right()
        self.running = True


    def run(self):
        while self.running:
            current_motion = self.motion_detector.detect_motion()
            self.motion_listener(current_motion)

            left_depth = self.left_depth_detector.get_dist_cm()
            self.left_depth_listener(left_depth)

            right_depth = self.right_depth_detector.get_dist_cm()
            self.right_depth_listener(right_depth)

            not_moving = False

            if current_motion.motion_everywhere() or not current_motion.has_motion():
                self.log("not moving")
                not_moving = True
            elif current_motion.motion_in_middle():
                self.log("forward")
                self.movement.go_forward(1)
                time.sleep(1)
                self.movement.stop()
            elif current_motion.motion_on_left():
                self.log("left")
                self.movement.turn_left(1)
                time.sleep(0.3)
                self.movement.stop()
            elif current_motion.motion_on_right():
                self.log("right")
                self.movement.turn_right(1)
                time.sleep(0.3)
                self.movement.stop()

            if not not_moving:
                time.sleep(0.2)

            if self.quit_monitor():
                self.stop()


    def stop(self):
        self.running = False
        self.movement.stop()


if __name__ == '__main__':
    robot = Robot()
    robot.start()
    robot.run()
    
