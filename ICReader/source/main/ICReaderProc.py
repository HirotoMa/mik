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
import RPi.GPIO as GPIO

num_blocks = 20
service_code = 0x090f

def connected(tag):
  #import pdb; pdb.set_trace()
  global LED_GPIO
  strtag = str(tag)
  result = strtag.find('ID=')
  strtag = strtag[result+3:result+19]
  print(strtag)
  # 赤LED点灯中なら退場
  import pdb; pdb.set_trace()
  channel_is_on = GPIO.input(DEFINE_NUMS.GPIO_NUM_DEF.RED_LED_GPIO) 
  if channel_is_on:
      DbQueue.put(DBOrder(DEFINE_NUMS.RECORD_DIRECTION.LEAVE_RECORD,strtag))
  else:
      DbQueue.put(DBOrder(DEFINE_NUMS.RECORD_DIRECTION.ENTER_RECORD,strtag))
  

def ICReaderProc1():
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(rdwr={'on-connect': connected})
        time.sleep(5)

