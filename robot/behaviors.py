import time
from status import status_reporting
from abc import ABC, abstractmethod

BEHAVIOR_MAX_NORMAL_PRIORITY = 50
BEHAVIOR_MAX_EMERGENCY_PRIORITY = 100

def getPriorityForTime(start_time, stop_time, active_window_seconds, inactive_window_seconds, current_time = time.time()):
    if start_time:
        target_stop_time = start_time + active_window_seconds
        time_remaining = target_stop_time - current_time
        priority_scaler = BEHAVIOR_MAX_NORMAL_PRIORITY / active_window_seconds
        return max(0, time_remaining * priority_scaler)
    else:
        target_start_time = stop_time + inactive_window_seconds
        time_to_wait = target_start_time - current_time
        priority_scaler = BEHAVIOR_MAX_NORMAL_PRIORITY / inactive_window_seconds
        return min(BEHAVIOR_MAX_NORMAL_PRIORITY, BEHAVIOR_MAX_NORMAL_PRIORITY - (time_to_wait * priority_scaler))


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


class ChaseMotion(Behavior):
    _OBSTRUCTION_DISTANCE = 20
    _REST_TIME = 30

    def __init__(self, robot):
        self.movement = robot.movement
        self.mode_stop = time.time() - self._REST_TIME
        super().__init__("Chase Motion", robot)


    def behavior_finished(self, robot):
        return robot.movement.state_elapsed_seconds() > 10


    def start(self):
        self.mode_start = time.time()
        self.movement.stop()


    def stop(self):
        self.mode_stop = time.time()


    def run(self):
        if not self.movement.is_moving:
            self.chase_motion()


    def priority(self):
        if time.time() - self.mode_stop < self._REST_TIME:
            return 0

        return 10


    def chase_motion(self):
        current_motion = self.robot.motion_detector.detect_motion()
    
        if current_motion.has_motion() and not current_motion.motion_everywhere():            
            if current_motion.motion_in_middle():
                self.movement.go_forward(1, 1)
            elif current_motion.motion_on_left():
                self.movement.turn_left(1, 0.3)
            elif current_motion.motion_on_right():
                self.movement.turn_right(1, 0.3)



class Wander(Behavior):

    _WANDER_OBSTRUCTION_DISTANCE = 30
    _WANDER_TIME = 90
    _PRIORITY_SCALAR = _WANDER_TIME / BEHAVIOR_MAX_NORMAL_PRIORITY 

    def __init__(self, robot):
        self.mode_stop = time.time()
        self.mode_start = None
        super().__init__("Wander", robot)


    def start(self):
        self.mode_start = time.time()
        self.mode_stop = None


    def stop(self):
        self.mode_stop = time.time()
        self.mode_start = None


    def run(self):
        self.robot.movement.go_forward(1, 0.1)    


    def priority(self):
        current_time = time.time()
        if self.mode_start:
            result = (self._WANDER_TIME - (current_time - self.mode_start)) * self._PRIORITY_SCALAR
        else:
            result = (current_time - self.mode_stop) * self._PRIORITY_SCALAR

        return max(min(BEHAVIOR_MAX_NORMAL_PRIORITY, result), 0)


class AvoidObstacles(Behavior):

    _OBSTRUCTION_DISTANCE = 30
    _PRIORITY_SCALAR = (BEHAVIOR_MAX_EMERGENCY_PRIORITY - BEHAVIOR_MAX_NORMAL_PRIORITY) / _OBSTRUCTION_DISTANCE

    def __init__(self, robot):
        super().__init__("Avoid Obstacles", robot)


    def start(self):
        pass


    def stop(self):
        pass


    def run(self):
        left, right = self._get_dist()
        left_obstructed = left < self._OBSTRUCTION_DISTANCE
        right_obstructed = right < self._OBSTRUCTION_DISTANCE

        if left_obstructed:
            self.robot.movement.turn_right(1, 0.1)
        else: 
            self.robot.movement.turn_left(1, 0.1)


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
