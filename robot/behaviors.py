import time
from status import status_reporting

OBSTRUCTION_DISTANCE = 20

class ChaseMotion:

    def __init__(self):
        self.description = "Chase Motion"


    def behavior_finished(self, robot):
        return robot.movement.state_elapsed_seconds() > 10


    def start_behavior(self, robot):
        self.mode_start = time.time()
        robot.movement.stop()


    def check_for_obstacles(self, robot):
        left_depth = robot.left_depth_detector.get_dist_cm()
        right_depth = robot.right_depth_detector.get_dist_cm()

        if left_depth < OBSTRUCTION_DISTANCE or right_depth < OBSTRUCTION_DISTANCE:
            robot.movement.stop()


    def chase_motion(self, robot):
        current_motion = robot.motion_detector.detect_motion()
    
        if current_motion.has_motion() and not current_motion.motion_everywhere():            
            if current_motion.motion_in_middle():
                robot.movement.go_forward(1, 1)
            elif current_motion.motion_on_left():
                robot.movement.turn_left(1, 0.3)
            elif current_motion.motion_on_right():
                robot.movement.turn_right(1, 0.3)
    

    def run_behavior(self, robot):
        if robot.movement.is_moving:
            self.check_for_obstacles(robot)
        else:
            self.chase_motion(robot)


WANDER_OBSTRUCTION_DISTANCE = 30

class Wander:
    def __init__(self):
        self.description = "Wander"


    def start_behavior(self, robot):
        self.mode_start = time.time()
        

    def behavior_finished(self, robot):
        return time.time() - self.mode_start > 30


    def run_behavior(self, robot):
        if robot.left_depth_detector.get_dist_cm() < WANDER_OBSTRUCTION_DISTANCE:
            robot.movement.turn_right(1, 0.1)
        elif robot.right_depth_detector.get_dist_cm() < WANDER_OBSTRUCTION_DISTANCE:
            robot.movement.turn_left(1, 0.1)
        else:
            robot.movement.go_forward(1, 0.1)