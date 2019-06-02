import RPi.GPIO as GPIO
from time import sleep
import subprocess
from DBProc import DEFINE_NUMS

OnOffstate = 1
def ledproc():
	global OnOffstate
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO, GPIO.OUT)
	OnOffstate = OnOffstate + 1
	OnOffstate = OnOffstate % 2
	GPIO.output(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO, OnOffstate)

def ButtonProc2(channel):
    if channel == 23:
        print("push!")
        ledproc()

def ButtonProc1():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.RISING, callback=ButtonProc2, bouncetime=5)

    try:
        while True:
            sleep(0.01)

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()