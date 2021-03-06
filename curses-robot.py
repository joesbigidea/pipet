#!/usr/bin/env python3

import curses
from vision.motiongrid import MotionCheckResult
from robot.robot import Robot
from status import status_reporting

class MotionWindow:
    
    def __init__(self, screen):
        self._MOTION_WINDOW_HEIGHT = 6
        self.window = screen.subwin(self._MOTION_WINDOW_HEIGHT, 10, screen_height - (self._MOTION_WINDOW_HEIGHT + 1), 0)
        self.window.border('|', '|', '-', '-')
        self.window.addstr(1, 1, " MOTION ")

    def update(self, motion_check_result):
        START_POS_Y = 2
        START_POS_X = 2
        for y in range(3):
            for x in range(3):
                if motion_check_result.motion_at(x, y):
                    display_char = "X"
                else:
                    display_char = "O"
                
                self.window.addstr(START_POS_Y + y, START_POS_X + (x * 2), display_char)

        self.refresh()

        
    def refresh(self):
        self.window.refresh()

class DepthWindow:
    
    def __init__(self, screen, label, y, x):
        self.WINDOW_HEIGHT = 4
        self.WINDOW_WIDTH = 25
        self.window = screen.subwin(self.WINDOW_HEIGHT, self.WINDOW_WIDTH, y, x)
        self.label = label
        self.update(0.00)        

    def update(self, depth_cm):
        self.window.erase()
        self.window.border('|', '|', '-', '-')
        self.window.addstr(1, 1, f" {self.label} DEPTH ")
        self.window.addstr(2, 2, f"{depth_cm:.2f}")
        self.refresh()

    def refresh(self):
        self.window.refresh()


class LogWindow:

    def __init__(self, screen, y, x):
        self.window = screen.subwin(5, screen_width - 10, y, x)


    def update(self, message):
        self.window.erase()
        self.window.border('|', '|', '-', '-')
        self.window.addstr(1, 1, "LOG")
        self.window.addstr(2, 1, f"{message}")
        self.refresh()

    
    def refresh(self):
        self.window.refresh()


class BehaviorWindow:

    def __init__(self, screen):
        WINDOW_HEIGHT = 4
        WINDOW_WIDTH = 20
        self.window = screen.subwin(WINDOW_HEIGHT, WINDOW_WIDTH, screen_height - (WINDOW_HEIGHT + 1), screen_width - (WINDOW_WIDTH + 1))
        self.update("LOADING...")


    def update(self, behavior):
        self.window.erase()
        self.window.border('|', '|', '-', '-')
        self.window.addstr(1, 1, "BEHAVIOR")
        self.window.addstr(2, 1, f"{behavior}")
        self.refresh()

    
    def refresh(self):
        self.window.refresh()


def should_quit(screen):
    try:
        return 'q' == screen.getkey()
    except:
        return False
       
MOTION_WINDOW_HEIGHT = 6

# The `screen` is a window that acts as the master window
# that takes up the whole screen. Other windows created
# later will get painted on to the `screen` window.
screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.curs_set(0)
screen.nodelay(True)
screen_height, screen_width = screen.getmaxyx()


motion_window = MotionWindow(screen)
left_depth_window = DepthWindow(screen, "Left", 1, 1)
right_depth_window = DepthWindow(screen, "Right", 1, 50)
log_window = LogWindow(screen, 10, 1)
behavior_window = BehaviorWindow(screen)

status_reporting.log = log_window.update
status_reporting.motion_listener = motion_window.update
status_reporting.left_depth_listener = left_depth_window.update
status_reporting.right_depth_listener = right_depth_window.update
status_reporting.behavior_listener = behavior_window.update

screen.refresh()

status_reporting.log("Starting...")

try:
    robot = Robot()
    robot.quit_monitor = lambda : should_quit(screen)
    robot.start()
    robot.run()
finally:
    curses.nocbreak()
    screen.keypad(0)
    curses.curs_set(1)
    curses.echo()
    curses.endwin()    

