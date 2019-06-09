#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
import subprocess
from DBProc import DEFINE_NUMS
from DBProc import global_Flag
from DBProc import itemThreadState
# ボタンスレッドの定義
ButttonThState = itemThreadState()

OnOffstate = True
def ledproc():
	global OnOffstate
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO, GPIO.OUT)
	OnOffstate = not OnOffstate
	GPIO.output(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO, OnOffstate)
	GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.GREEN_LED_GPIO, GPIO.OUT)
	GPIO.output(DEFINE_NUMS.GPIO_NUM_DEF.GREEN_LED_GPIO, not OnOffstate)

def ButtonProc2(channel):
    if channel == DEFINE_NUMS.GPIO_NUM_DEF.BUTTON_GPIO:
        ledproc()

def ButtonProc1():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(DEFINE_NUMS.GPIO_NUM_DEF.BUTTON_GPIO, GPIO.RISING, callback=ButtonProc2, bouncetime=5)

    try:
        while True:
            sleep(0.01)
            if (global_Flag.getFlag() == True):
                # setメソッドが呼び出されるまでスレッドを待機させる
                ButttonThState.wait_flag = True
                ButttonThState.event.wait()
                ButttonThState.wait_flag = False

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()