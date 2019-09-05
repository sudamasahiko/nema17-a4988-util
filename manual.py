import sys, threading
from time import sleep
import RPi.GPIO as GPIO

CW = 1
CCW = 0
PIN_DIR_MOT1 = 20
PIN_STEP_MOT1 = 21
STEP_RESOLUTION = 1
DEG_PER_STEP = 1.8 / STEP_RESOLUTION
SPR = 360 / DEG_PER_STEP
DELAY_PER_STEP = 0.006 # 100RPM

# parameter check
raw_angle = float(sys.argv[1])
if raw_angle == None:
    raw_angle = 0.0
angle = abs(raw_angle) % 360
steps = abs(int(SPR * angle / 360))
direction = CCW if raw_angle < 0 else CW

# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR_MOT1, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT1, GPIO.OUT)
GPIO.output(PIN_DIR_MOT1, GPIO.LOW)
GPIO.output(PIN_STEP_MOT1, GPIO.LOW)

def rotate(direction, steps, PIN_DIR, PIN_STEP):
    GPIO.output(PIN_DIR, direction)
    for x in range(steps):
        GPIO.output(PIN_STEP, GPIO.HIGH)
        sleep(DELAY_PER_STEP / 2)
        GPIO.output(PIN_STEP, GPIO.LOW)
        sleep(DELAY_PER_STEP / 2)

# rotate(direction, steps, PIN_DIR_MOT1, PIN_STEP_MOT1)
t1 = threading.Thread(target=rotate, args=(direction, steps, PIN_DIR_MOT1, PIN_STEP_MOT1))
t1.start()
t1.join()

GPIO.cleanup()

