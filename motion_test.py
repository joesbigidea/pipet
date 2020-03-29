#!/usr/bin/env python3

from vision import motiondetection
from movement.movement import Movement

import time

print(f"Starting robot")

movement = Movement()

print("left wheel only")
movement.left_wheel()
time.sleep(0.2)
movement.stop()
time.sleep(5)


print("turning left")
movement.turn_left(1)
time.sleep(0.2)
movement.stop()
time.sleep(5)

print("turning right")
movement.turn_right(1)
time.sleep(0.2)
movement.stop()
time.sleep(5)

print("forward")
movement.go_forward(0.75)
time.sleep(0.2)
movement.stop()
time.sleep(5)

print("backward")
movement.go_backward(0.75)
time.sleep(0.2)
movement.stop()
