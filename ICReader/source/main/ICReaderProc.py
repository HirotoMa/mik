#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import binascii
import os
import struct
import sys
import time
import threading
import Queue
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/nfcpy')

import nfc
from DBProc import DbQueue
from DBProc import DBOrder
from DBProc import DEFINE_NUMS
from DBProc import itemThreadState
import RPi.GPIO as GPIO

num_blocks = 20
service_code = 0x090f

# ICリーダースレッドの定義
IcReaderThState = itemThreadState()

def connected(tag):
  import pdb; pdb.set_trace()
  global LED_GPIO
  strtag = str(tag)
  result = strtag.find('ID=')
  strtag = strtag[result+3:result+19]
  print(strtag)
  # 赤LED点灯中なら退場
  #import pdb; pdb.set_trace()
  channel_is_on = GPIO.input(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO)
  if channel_is_on:
      DbQueue.put(DBOrder(DEFINE_NUMS.RECORD_DIRECTION.LEAVE_RECORD,strtag))
  else:
      DbQueue.put(DBOrder(DEFINE_NUMS.RECORD_DIRECTION.ENTER_RECORD,strtag))

from DBProc import global_Flag

# 待ち受けの1サイクル秒
TIME_cycle = 0.1
# 待ち受けの反応インターバル秒
TIME_interval = 0.1
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIME_wait = 3
# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_felica = nfc.clf.RemoteTarget("212F")
def ICReaderProc1():
    clf = nfc.ContactlessFrontend('usb')
    try:
        while True:
            if (global_Flag.getFlag() == True):
                # setメソッドが呼び出されるまでスレッドを待機させる
                IcReaderThState.wait_flag = True
                clf.close()
                print("connect closed!")
                IcReaderThState.event.wait()
                IcReaderThState.wait_flag = False
                clf = nfc.ContactlessFrontend('usb')
            # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
            target_res = clf.sense(target_req_felica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)
            if not target_res is None:
                # 読み取りを行う（読み取り完了かタイムアップまでブロックされる）
                tag = nfc.tag.activate(clf, target_res)
                # 読み取り完了なら、タグ読み込みを行う
                connected(tag)
                # 次の読み込みまで、ブロッキングを行う
                time.sleep(5)

    except KeyboardInterrupt:
        clf.close()
        print("connect closed!!!!!")
    clf.close()
    print("connect closed!")

