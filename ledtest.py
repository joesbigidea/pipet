#!/usr/bin/env python3

import board
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

#pwm frequency
hat.frequency = 60

led_channel = hat.channels[1]

# Increase brightness:
for i in range(0, 0xffff, 10):
    led_channel.duty_cycle = i
 
# Decrease brightness:
for i in range(0xffff, 0, -10):
    led_channel.duty_cycle = i