from picamera.array import PiRGBArray
from picamera import PiCamera
from vision.motiongrid import MotionCheckResult, MotionDetectionGrid
from vision.boundingbox import BoundingBox
from types import SimpleNamespace

import threading
import time
import cv2

NO_MOTION = MotionCheckResult([ [ False for col in range(3)] for row in range(3) ])

class MotionDetector:

    def __init__(self, log):
        self._conf = SimpleNamespace()
        self._conf.camera_warmup_time = 10
        self._conf.delta_thresh = 5
        self._conf.blur_size = [11, 11]
        self._conf.resolution = [320, 240]
        self._conf.fps = 30
        self._conf.min_area = 1000
        self._camera = PiCamera()
        self._camera.exposure_mode = "fixedfps"
        self._camera.resolution = self._conf.resolution
        self._camera.framerate = self._conf.fps
        self._camera.rotation = 180
    
        self._raw_capture = PiRGBArray(self._camera, size=tuple(self._conf.resolution))
        self._motion_detection_grid = MotionDetectionGrid(self._conf.resolution)
        time.sleep(self._conf.camera_warmup_time)
        log("Camera started")
        

    def _capture_frame(self):
        self._raw_capture.truncate(0)
        self._camera.capture(self._raw_capture, format="bgr", use_video_port=True)
        frame = self._raw_capture.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, tuple(self._conf.blur_size), 0)
        return gray


    def detect_motion(self):
        start = time.time()

        frame1 = self._capture_frame()

        frame2 = self._capture_frame()

        frameDelta = cv2.absdiff(frame2, cv2.convertScaleAbs(frame1))
                
        # threshold the delta image, dilate the thresholded image to fill
        # in holes, then find contours on thresholded image
        thresh = cv2.threshold(frameDelta, self._conf.delta_thresh, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_contours = list(filter(lambda c : cv2.contourArea(c) > self._conf.min_area, cnts))

        if len(motion_contours) > 0:
            motion_rects = [ cv2.boundingRect(c) for c in motion_contours ]
            motion_bounds = [ BoundingBox(r[0], r[1], r[0] + r[2], r[1] + r[3]) for r in motion_rects ]

            result = self._motion_detection_grid.check_motion(motion_bounds)
        else:
            result = NO_MOTION

        end = time.time()
        return result
