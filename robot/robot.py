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
        self.behaviors = [ behaviors.ChaseMotion(self), behaviors.Wander(self), behaviors.AvoidObstacles(self) ]
        self._current_behavior = None


    def run_updates(self):
        self.movement.update()


    def update_behavior(self):
        max_priority = -1
        best_behavior = None
        priorities = ""
        for behavior in self.behaviors:
            priority = behavior.priority()
            priorities += f"Behavior {behavior.description} Priority: {priority} "
            if priority > max_priority:
                max_priority = priority
                best_behavior = behavior

        status_reporting.log(priorities)

        if best_behavior != self._current_behavior:
            if self._current_behavior:
                self._current_behavior.stop()
            best_behavior.start()
            self._current_behavior = best_behavior
            status_reporting.behavior_listener(best_behavior.description)


    def run(self):
        while self.running:
            self.movement.update()            

            self.update_behavior()
                
            self._current_behavior.run()

            if self.quit_monitor():
                self.stop()


    def stop(self):
        self.running = False
        self.movement.stop()


if __name__ == '__main__':
    robot = Robot()
    robot.start()
    robot.run()
    
