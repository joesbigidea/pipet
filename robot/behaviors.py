import time
from status import status_reporting
from abc import ABC, abstractmethod

BEHAVIOR_MAX_NORMAL_PRIORITY = 50
BEHAVIOR_MAX_EMERGENCY_PRIORITY = 100


class Behavior(ABC):

    def __init__(self, description, robot):
        self.description = description
        self.robot = robot
        super(Behavior, self).__init__()


    @abstractmethod
    def start(self):
        pass


    @abstractmethod
    def stop(self):
        pass


    @abstractmethod
    def run(self):
        pass


    @abstractmethod
    def priority(self):
        pass


class TimedBehavior(Behavior):

    def __init__(self, description, robot, run_time, rest_time):
        self.run_time = run_time
        self.rest_time = rest_time
        self.recovery_scalar = rest_time / run_time
        self.time_remaining = run_time
        self.last_priority_call = time.time()
        self.running = False
        self.mode_stop = time.time()
        super().__init__(description, robot)


    def start(self):
        self.mode_start = time.time()
        self.mode_stop = None
        self.running = True
        if self.time_remaining == 0:
            self.time_remaining = self.run_time


    def stop(self):
        self.mode_stop = time.time()       
        self.running = False
        

    def priority(self):
        if self.running:
            current_time = time.time()
            duration = current_time - self.last_priority_call
            self.time_remaining = max(0, self.time_remaining - duration)
            self.last_priority_call = current_time

        if self.time_remaining > 0:
            return BEHAVIOR_MAX_NORMAL_PRIORITY

        if self.running:
            return 0

        target_start_time = self.mode_stop + self.rest_time
        time_to_wait = target_start_time - time.time()
        priority_scaler = BEHAVIOR_MAX_NORMAL_PRIORITY / self.rest_time
        result = BEHAVIOR_MAX_NORMAL_PRIORITY - (time_to_wait * priority_scaler)
        return max(0, min(BEHAVIOR_MAX_NORMAL_PRIORITY, result)) 


class ChaseMotion(TimedBehavior):
    
    
    def __init__(self, robot):
        self.movement = robot.movement
        super().__init__("Chase Motion", robot, 30, 60)


    def run(self):
        current_motion = self.robot.motion_detector.detect_motion()
    
        if current_motion.has_motion() and not current_motion.motion_everywhere():            
            if current_motion.motion_in_middle():
                self.movement.go_forward(1, 1)
            elif current_motion.motion_on_left():
                self.movement.turn_left(1, 0.3)
            elif current_motion.motion_on_right():
                self.movement.turn_right(1, 0.3)


class Wander(TimedBehavior):


    def __init__(self, robot):
        super().__init__("Wander", robot, 60, 30)


    def run(self):
        self.robot.movement.go_forward(1, 0.1)    


class AvoidObstacles(Behavior):

    _OBSTRUCTION_DISTANCE = 30
    _PRIORITY_SCALAR = (BEHAVIOR_MAX_EMERGENCY_PRIORITY - BEHAVIOR_MAX_NORMAL_PRIORITY) / _OBSTRUCTION_DISTANCE

    def __init__(self, robot):
        super().__init__("Avoid Obstacles", robot)


    def start(self):
        left, right = self._get_dist()
        if left < right:
            self.move = self.robot.movement.turn_right
        else:
            self.move = self.robot.movement.turn_left


    def stop(self):
        pass


    def run(self):
        self.move(1, 0.1)


    def priority(self):
        left, right = self._get_dist()
        if left > self._OBSTRUCTION_DISTANCE and right > self._OBSTRUCTION_DISTANCE:
            return 0

        dist = min(left, right)

        dist_priority = (self._OBSTRUCTION_DISTANCE - (dist)) * self._PRIORITY_SCALAR
        return BEHAVIOR_MAX_NORMAL_PRIORITY + dist_priority

    
    def _get_dist(self):
        return (self.robot.left_depth_detector.get_dist_cm(),
            self.robot.right_depth_detector.get_dist_cm())
