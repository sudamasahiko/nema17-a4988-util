# manual.py
#
# this script will be used for manipulating motor angles manually
# usage syntax: python manual.py [deg_motor1] [deg_motor2] [deg_motor3]
# usage example: python manual.py 60 30 -30
# LICENSE: MIT License
# (C) Seltec Lab 2019

import sys, threading
from time import sleep
import RPi.GPIO as GPIO

# pins
PIN_DIR_MOT1 = 20
PIN_STEP_MOT1 = 21
PIN_DIR_MOT2 = 5
PIN_STEP_MOT2 = 6
PIN_DIR_MOT3 = 13
PIN_STEP_MOT3 = 19

# NEMA17
STEP_RESOLUTION = 1
DEG_PER_STEP = 1.8 / STEP_RESOLUTION
DELAY_PER_STEP = 0.006 # 100RPM

# other constants
SPR = 360 / DEG_PER_STEP
CW = 1
CCW = 0

# parameter check
def arg_to_steps(arg)
    raw_angle = float(arg)
    if raw_angle == None:
        raw_angle = 0.0
    angle = abs(raw_angle) % 360
    steps = abs(int(SPR * angle / 360))
    direction = CCW if raw_angle < 0 else CW
    return (steps, direction)

(s_m1, d_m1) = arg_to_steps(sys.argv[1])
(s_m2, d_m2) = arg_to_steps(sys.argv[2])
(s_m3, d_m3) = arg_to_steps(sys.argv[3])

# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR_MOT1, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT1, GPIO.OUT)
GPIO.setup(PIN_DIR_MOT2, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT2, GPIO.OUT)
GPIO.setup(PIN_DIR_MOT3, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT3, GPIO.OUT)

# init GPIO pins
GPIO.output(PIN_DIR_MOT1, GPIO.LOW)
GPIO.output(PIN_STEP_MOT1, GPIO.LOW)
GPIO.output(PIN_DIR_MOT2, GPIO.LOW)
GPIO.output(PIN_STEP_MOT2, GPIO.LOW)
GPIO.output(PIN_DIR_MOT3, GPIO.LOW)
GPIO.output(PIN_STEP_MOT3, GPIO.LOW)

# rotate function
def rotate(steps, direction, PIN_DIR, PIN_STEP):
    GPIO.output(PIN_DIR, direction)
    for x in range(steps):
        GPIO.output(PIN_STEP, GPIO.HIGH)
        sleep(DELAY_PER_STEP / 2)
        GPIO.output(PIN_STEP, GPIO.LOW)
        sleep(DELAY_PER_STEP / 2)

# execute rotation using threading
pin_direc = PIN_DIR_MOT1
pin_step = PIN_STEP_MOT1
t1 = threading.Thread(target=rotate, args=(s_m1, d_m1, pin_direc, pin_step))
pin_direc = PIN_DIR_MOT2
pin_step = PIN_STEP_MOT2
t2 = threading.Thread(target=rotate, args=(s_m2, d_m2, pin_direc, pin_step))
pin_direc = PIN_DIR_MOT3
pin_step = PIN_STEP_MOT3
t3 = threading.Thread(target=rotate, args=(s_m3, d_m3, pin_direc, pin_step))

# start execution
t1.start()
t2.start()
t3.start()

# wait until all motors finish rotation
t1.join()
t2.join()
t3.join()

GPIO.cleanup()

