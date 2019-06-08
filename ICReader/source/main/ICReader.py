#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import threading

import ICReaderProc
import DBProc
import ButtonProc
from DBProc import DEFINE_NUMS
from DBProc import global_Flag
from DBProc import itemThreadState
from DBProc import DBThState
from ICReaderProc import IcReaderThState
from ButtonProc import ButttonThState
import RPi.GPIO as GPIO


icReaderTh = threading.Thread(target=ICReaderProc.ICReaderProc1)
dbTh = threading.Thread(target=DBProc.DBProc1)
butttonTh = threading.Thread(target=ButtonProc.ButtonProc1)
global ThArray
ThArray = [icReaderTh,dbTh,butttonTh]
ThStateArray = [IcReaderThState,DBThState,ButttonThState]

def threadStart(tharray):
    for th in ThStateArray:
        th.event.set()  # 待機を解除する
        th.event.clear()  # setしたままだとwaitで待機しなくなる

def threadStart1(tharray):
    for th in tharray:
        th.start()

def powerButtonProc(channel):
    global ThArray
    if channel != DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO:
        return
    global_Flag.setFlagChange()
    if global_Flag.getFlag() == False:
        threadStart(ThArray)
        print("FlagOFF")
    else:
        # 二回目のボタン押しならスレッド停止
        print("FlagON")

def defSwitchLCD(channel):
    if channel == DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO:
        threadProc()

def threadProc():
    print("signal detect")
    if GPIO.input(DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO):     # if port 17 == 1
        print("ONdetect!")
        global_Flag.setFlagOFF()
        threadStart(ThArray)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.YELLOW_LED_GPIO, GPIO.OUT)
        GPIO.output(DEFINE_NUMS.GPIO_NUM_DEF.YELLOW_LED_GPIO, 1)
        print("ON!")
    else:
        print("OFFdetect!")
        global_Flag.setFlagON()
        # 全スレッドのリストを取得
        #thread_list = threading.enumerate()
        #import pdb; pdb.set_trace()
        # メインスレッドは対象外
        #thread_list.remove(threading.current_thread())
        # メインスレッド以外の全スレッドを待ち合わせ
        while True:
            alive_cnt = 0
            if icReaderTh.isAlive() and IcReaderThState.wait_flag == False:
                alive_cnt = alive_cnt + 1
            if dbTh.isAlive() and DBThState.wait_flag == False:
                alive_cnt = alive_cnt + 1
            if butttonTh.isAlive() and ButttonThState.wait_flag == False:
                alive_cnt = alive_cnt + 1
            if alive_cnt == 0:
                break

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.YELLOW_LED_GPIO, GPIO.OUT)
        GPIO.output(DEFINE_NUMS.GPIO_NUM_DEF.YELLOW_LED_GPIO, 0)
        print("OFF!")

if __name__ == "__main__":
    #from db.DBProc import DBProc
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO, GPIO.OUT)
    GPIO.output(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO, 0)
    GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    threadStart1(ThArray)
    threadProc()
    last_state = GPIO.input(DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO)
    while True:
        # メインスレッドはスライドスイッチのポーリング処理を行う
        time.sleep(0.5)
        if last_state != GPIO.input(DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO):
            threadProc()
            GPIO.setup(DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            last_state = GPIO.input(DEFINE_NUMS.GPIO_NUM_DEF.SHUDOWN_SWITCH_GPIO)
            
