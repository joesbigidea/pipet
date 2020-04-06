#!/usr/bin/env python3

import time
import board
from adafruit_hcsr04 import HCSR04

def getDist(sonar):
    try:
        return sonar.distance
    except RuntimeError:
        return -1

left = HCSR04(board.D5, board.D6)
right = HCSR04(board.D17, board.D18)

while True:
    print(f"Left {getDist(left)}, Right {getDist(right)}")
    time.sleep(0.1)


# with HCSR04(board.D23, board.D24) as sonar:
#     while True:
#         try:
#             print((sonar.distance,))
#         except RuntimeError:
#             print("Retrying!")
#         time.sleep(0.1)