#!/usr/bin/env python3

from picamera import PiCamera
import numpy as np
import cv2
import time

print("Starting camera")
camera = PiCamera()
camera.resolution = [320, 240]
camera.framerate = 16

time.sleep(5)
print("Camera started")

image = np.empty((240 * 320 * 3,), dtype=np.uint8)
camera.capture(image, 'bgr')
cv2.imwrite('testimage.png', image)
