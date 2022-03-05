PiPet
=====
This is software for a Raspberry Pi based robopet written in Python

Software Requirements
=====================
- OpenCV
- Python 3
- Probably other stuff I've forgotten


Running
=======
There are two entrypoints that present a Curses UI for some feedback on what the Robot is experiencing. They provide two different modes of operation.

1. curses-robot.py: This starts the robot in behavior driven mode, where it cycles through various behaviors like wandering, movement following (not great), and obstacle avoidance based on sensor input and time
2. curses-manual-robot.py: This starts the robot in a mode that follows simple commands you can write in robot/robotmanual.py. This is a much more straightforward way to control the bot if you just want to give it specific instructions. This is great for letting beginners use programming to make something happen.

Hardware
========
My implementation uses two sonar depth sensors, a Raspberry Pi camera, two hobby servos modified to rotate continuously, and a good old cell phone backup batter for power. If you want more specifics let me know and I'll put together a design and a parts list.
