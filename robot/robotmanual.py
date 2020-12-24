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
        #self.motion_detector = MotionDetector()
        self.movement = Movement()
        self.movement.stop()        
        self.left_depth_detector = depthdetection.build_left()
        self.right_depth_detector = depthdetection.build_right()        
        self.running = True
        #self.behaviors = [ behaviors.ChaseMotion(self), behaviors.Wander(self), behaviors.AvoidObstacles(self) ]
        self._current_behavior = None

    #########################################################################
    # Simplified robot commands
    # speed is (I think, 0-1)
    # duration is seconds
    #########################################################################

    def go_forward(self, duration, speed = 1):
        self.movement.go_forward(speed, duration)
        time.sleep(duration)
        self.movement.stop()

    def go_backard(self, duration, speed = 1):
        self.go_forward(duration, -speed)

    def turn_right(self, duration, speed = 1):
        self.movement.turn_right(speed, duration)
        time.sleep(duration)
        self.movement.stop()

    def turn_left(self, duration, speed = 1):
        self.turn_right(duration, -speed)

    #get the distance to the nearest obstacle in cm
    def left_depth(self):
        return self.left_depth_detector.get_dist_cm()

    #get the distance to the nearest obstacle in cm
    def right_depth(self):
        return self.right_depth_detector.get_dist_cm()

    def distance(self):
        l = self.left_depth()
        r = self.right_depth()
        if l < r:
            return l
        
        return r

    # PUT YOUR COMMANDS HERE!
    def run(self):
        status_reporting.log('hi there!')
        self.go_forward(5)
        self.go_backard(1)
        self.turn_left(2)
        self.turn_right(1)
        distance = self.distance()
        if distance < 10:
            status_reporting.log('Oh no!')

        time.sleep(1)

        
        status_reporting.log('bye!')        
        time.sleep(5)

        #always end with stop
        self.stop()


    def stop(self):
        self.running = False
        self.movement.stop()


if __name__ == '__main__':
    robot = Robot()
    robot.start()
    robot.run()
    
