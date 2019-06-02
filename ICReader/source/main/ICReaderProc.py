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

num_blocks = 20
service_code = 0x090f

count = 0
def connected(tag):
  #import pdb; pdb.set_trace()
  global count
  strtag = str(tag)
  import re
  result = strtag.find('ID=')
  strtag = strtag[result+3:result+19]
  print(strtag)
  count = count + 1
  DbQueue.put(DBOrder(count%2,strtag))

def ICReaderProc1():
    clf = nfc.ContactlessFrontend('usb')
    while True:
        clf.connect(rdwr={'on-connect': connected})
        time.sleep(5)

