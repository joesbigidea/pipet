from picamera.array import PiRGBArray
from picamera import PiCamera
from vision.motiongrid import MotionCheckResult, MotionDetectionGrid
from vision.boundingbox import BoundingBox
from types import SimpleNamespace

import threading
import time
import cv2

NO_MOTION = MotionCheckResult([ [ False for col in range(3)] for row in range(3) ])

_current_motion = NO_MOTION
_running = True
_motion_lock = threading.RLock()
_detection_thread = None


def start_motion_detection():
    global _running, _detection_thread
    conf = SimpleNamespace()
    conf.camera_warmup_time = 10
    conf.delta_thresh = 5
    conf.blur_size = [21, 21]
    conf.resolution = [640, 480]
    conf.fps = 30
    conf.min_area = 5000
    camera = PiCamera()
    camera.resolution = conf.resolution
    camera.framerate = conf.fps
    camera.rotation = 180
    _running = True

    time.sleep(conf.camera_warmup_time)
    print("Camera started")

    _detection_thread = threading.Thread(target=_detect_motion, args=(conf,camera), name="motion-detection-thread")
    _detection_thread.start()


def stop_motion_detection():
    global _running, _detection_thread
    _running = False
    if _detection_thread:
        _detection_thread.join()


def get_current_motion():
    global _motion_lock, _current_motion
    _motion_lock.acquire()
    result = _current_motion
    _motion_lock.release()
    return result


def _set_current_motion(motion):
    global _motion_lock, _current_motion
    _motion_lock.acquire()
    _current_motion = motion
    _motion_lock.release()


def _detect_motion(conf, camera):
    global NO_MOTION, _running

    rawCapture = PiRGBArray(camera, size=tuple(conf.resolution))
    previous_gray = None

    motion_detection_grid = MotionDetectionGrid(conf.resolution)

    for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        start = time.time()
        
        if not _running:
            break

        # grab the raw NumPy array representing the image and initialize
        # the timestamp and occupied/unoccupied text
        frame = f.array

        ######################################################################
        # COMPUTER VISION
        ######################################################################
        # resize the frame, convert it to grayscale, and blur it
        # TODO: resize image here into cmaller sizes 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, tuple(conf.blur_size), 0)

        if not previous_gray is None:
            frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(previous_gray))
            
            # threshold the delta image, dilate the thresholded image to fill
            # in holes, then find contours on thresholded image
            thresh = cv2.threshold(frameDelta, conf.delta_thresh, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            motion_contours = list(filter(lambda c : cv2.contourArea(c) > conf.min_area, cnts))

            if len(motion_contours) > 0:
                motion_rects = [ cv2.boundingRect(c) for c in motion_contours ]
                motion_bounds = [ BoundingBox(r[0], r[1], r[0] + r[2], r[1] + r[3]) for r in motion_rects ]

                _set_current_motion(motion_detection_grid.check_motion(motion_bounds))
            else:
                _set_current_motion(NO_MOTION)

        previous_gray = gray    
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        end = time.time()
        print(f"took: {end - start}")
