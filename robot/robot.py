#!/usr/bin/env python3

from vision import motiondetection
from vision.motiondetection import MotionDetector
from movement.movement import Movement
from depth import depthdetection

import time

OBSTRUCTION_DISTANCE = 20

class Robot:
        
    def __init__(self):
        self.log = print
        self.motion_listener = lambda m : print(f"Motion: {m}")
        self.left_depth_listener = lambda d : print(f"Depth 1: {d}")
        self.right_depth_listener = lambda d : print(f"Depth 2: {d}")
        self.quit_monitor = lambda: False


    def start(self):
        self.motion_detector = MotionDetector(self.log)
        self.log(f"Motion detection started")
        self.movement = Movement()
        self.movement.stop()        
        self.left_depth_detector = depthdetection.build_left()
        self.right_depth_detector = depthdetection.build_right()        
        self.running = True


    def chase_motion(self):
        current_motion = self.motion_detector.detect_motion()
        self.motion_listener(current_motion)

        if current_motion.has_motion() and not current_motion.motion_everywhere():            
            if current_motion.motion_in_middle():
                self.movement.go_forward(1, 1)
            elif current_motion.motion_on_left():
                self.movement.turn_left(1, 0.3)
            elif current_motion.motion_on_right():
                self.movement.turn_right(1, 0.3)


    def check_depth(self):
        left_depth = self.left_depth_detector.get_dist_cm()
        self.left_depth_listener(left_depth)

        right_depth = self.right_depth_detector.get_dist_cm()
        self.right_depth_listener(right_depth)

        if left_depth < OBSTRUCTION_DISTANCE or right_depth < OBSTRUCTION_DISTANCE:
            self.movement.stop()


    def run(self):
        while self.running:
            self.movement.update()

            if self.movement.is_moving:
                self.check_depth()
            else:
                self.chase_motion()       

            if self.quit_monitor():
                self.stop()


    def stop(self):
        self.running = False
        self.movement.stop()


if __name__ == '__main__':
    robot = Robot()
    robot.start()
    robot.run()
    
