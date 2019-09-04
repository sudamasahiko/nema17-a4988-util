import sys
from time import sleep
import RPi.GPIO as GPIO

PIN_DIR = 20
PIN_STEP = 21
CW = 1
CCW = 0
STEP_RESOLUTION = 1
DEG_PER_STEP = 1.8 / STEP_RESOLUTION
SPR = 360 / DEG_PER_STEP

# parameter check
raw_angle = float(sys.argv[1])
if raw_angle == None:
    raw_angle = 0.0
angle = abs(raw_angle) % 360
steps = abs(int(SPR * angle / 360))
direction = CCW if raw_angle < 0 else CW

# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR, GPIO.OUT)
GPIO.setup(PIN_STEP, GPIO.OUT)
GPIO.output(PIN_DIR, GPIO.LOW)
GPIO.output(PIN_STEP, GPIO.LOW)

# 100RPM
delay = .003

GPIO.output(PIN_DIR, direction)
for x in range(steps):
    GPIO.output(PIN_STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(PIN_STEP, GPIO.LOW)
    sleep(delay)

GPIO.cleanup()

