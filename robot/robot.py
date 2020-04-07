#!/usr/bin/env python3

from vision import motiondetection
from vision.motiondetection import MotionDetector
from movement.movement import Movement
from depth import depthdetection
from status import status_reporting
from robot import behaviors

import time

class Robot:
        
    def __init__(self):
        self.quit_monitor = lambda: False


    def start(self):
        self.motion_detector = MotionDetector()
        self.movement = Movement()
        self.movement.stop()        
        self.left_depth_detector = depthdetection.build_left()
        self.right_depth_detector = depthdetection.build_right()        
        self.running = True
        self.behaviors = [ behaviors.ChaseMotion(), behaviors.Wander() ]
        self._current_behavior = None
        self.behavior_index = -1


    def run_updates(self):
        self.movement.update()


    def start_next_behavior(self):
        self.behavior_index += 1
        if self.behavior_index >= len(self.behaviors):
            self.behavior_index = 0
            
        self._current_behavior = self.behaviors[self.behavior_index]
        self._current_behavior.start_behavior(self)


    def run(self):
        self.start_next_behavior()

        while self.running:
            self.movement.update()            
                
            if self._current_behavior.behavior_finished(self):
                self.start_next_behavior()

            self._current_behavior.run_behavior(self)

            if self.quit_monitor():
                self.stop()


    def stop(self):
        self.running = False
        self.movement.stop()


if __name__ == '__main__':
    robot = Robot()
    robot.start()
    robot.run()
    
