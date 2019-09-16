# manual.py
#
# this script will be used for manipulating motor angles manually
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
# STEP_RESOLUTION = 1
STEP_RESOLUTION = 16
DEG_PER_STEP = 1.8 / STEP_RESOLUTION
DELAY_PER_STEP = 0.006 # 100RPM
# DELAY_PER_STEP = 0.048 # 12.5RPM

# other constants
SPR = 360 / DEG_PER_STEP
CW = 1
CCW = 0

# parameter check
def arg_to_steps(arg):
    raw_angle = float(arg)
    if raw_angle == None:
        raw_angle = 0.0
    angle = abs(raw_angle) % 360
    steps = abs(int(SPR * angle / 360))
    direction = CCW if raw_angle < 0 else CW
    return (steps, direction)

def biggest(a, y, z):
    Max = a
    if y > Max:
        Max = y
    if z > Max:
        Max = z
        if y > z:
            Max = y
    return Max

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
def rotate(steps, direction, pin_dir, pin_step, span_delay):
    if not span_delay or not steps:
        return

    GPIO.output(pin_dir, direction)
    for x in range(steps):
        GPIO.output(pin_step, GPIO.HIGH)
        sleep(span_delay)
        GPIO.output(pin_step, GPIO.LOW)
        sleep(span_delay)

def get_span_params(s_m1, s_m2, s_m3):
    max_step = biggest(s_m1, s_m2, s_m3)
    try:
        span_m1 = 0.5 * DELAY_PER_STEP * max_step / s_m1
    except:
        span_m1 = None
    try:
        span_m2 = 0.5 * DELAY_PER_STEP * max_step / s_m2
    except:
        span_m2 = None
    try:
        span_m3 = 0.5 * DELAY_PER_STEP * max_step / s_m3
    except:
        span_m3 = None
    return (span_m1, span_m2, span_m3)

try:
    while True:
        deg1 = input('motor1 angle:')
        deg2 = input('motor2 angle:')
        deg3 = input('motor3 angle:')
        (s_m1, d_m1) = arg_to_steps(deg1)
        (s_m2, d_m2) = arg_to_steps(deg2)
        (s_m3, d_m3) = arg_to_steps(deg3)
        (span_m1, span_m2, span_m3) = get_span_params(s_m1, s_m2, s_m3)

        # execute rotation using threading
        pin_direc = PIN_DIR_MOT1
        pin_step = PIN_STEP_MOT1
        t1 = threading.Thread(target=rotate, args=(s_m1, d_m1, pin_direc, pin_step, span_m1))
        pin_direc = PIN_DIR_MOT2
        pin_step = PIN_STEP_MOT2
        t2 = threading.Thread(target=rotate, args=(s_m2, d_m2, pin_direc, pin_step, span_m2))
        pin_direc = PIN_DIR_MOT3
        pin_step = PIN_STEP_MOT3
        t3 = threading.Thread(target=rotate, args=(s_m3, d_m3, pin_direc, pin_step, span_m3))

        # start execution
        t1.start()
        t2.start()
        t3.start()

        # wait until all motors finish rotation
        t1.join()
        t2.join()
        t3.join()
except KeyboardInterrupt:
    print('\nterminating...')
    GPIO.cleanup()
    sys.exit()

