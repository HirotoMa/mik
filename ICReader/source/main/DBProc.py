#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import Queue
import time

class itemThreadState():
    def __init__(self):
        self.wait_flag = False
        # Eventオブジェクトを生成する
        self.event = threading.Event()

# DBスレッドの定義
DBThState = itemThreadState()

DbQueue = Queue.Queue()
class DBOrder:
   def __init__(self, direct, IDm):
    self.direct = direct
    self.IDm = IDm

class DEFINE_NUMS():
    class RECORD_DIRECTION():
        ENTER_RECORD = 0
        LEAVE_RECORD = 1

    class GPIO_NUM_DEF():
        RED_LED_GPIO = 18
        BUTTON_GPIO = 23
        SHUDOWN_SWITCH_GPIO = 17
        YELLOW_LED_GPIO = 26
        GREEN_LED_GPIO = 19

class GLOBAL_FLAG():
    def __init__(self):
        self.KILL_TASK_FLAG = True
    def getFlag(self):
        return self.KILL_TASK_FLAG
    def setFlagChange(self):
        self.KILL_TASK_FLAG = not self.KILL_TASK_FLAG
    def setFlagON(self):
        self.KILL_TASK_FLAG = True
    def setFlagOFF(self):
        self.KILL_TASK_FLAG = False

global_Flag = GLOBAL_FLAG()


def DBProc1():
    while True:
        if not DbQueue.empty():
            item = DbQueue.get()
            print("receive")
            #import pdb; pdb.set_trace()
            if item.direct == DEFINE_NUMS.RECORD_DIRECTION.ENTER_RECORD:
                WriteEnterRecord(item.IDm)
            elif item.direct == DEFINE_NUMS.RECORD_DIRECTION.LEAVE_RECORD:
                WriteLeaveRecord(item.IDm)
        else:
            if global_Flag.getFlag() == True:
                # setメソッドが呼び出されるまでスレッドを待機させる
                DBThState.wait_flag = True
                DBThState.event.wait()
                DBThState.wait_flag = False

# MySQLdbのインポート
import MySQLdb
# モジュールのインポート
import xml.etree.ElementTree as ET

from LCDProc import LCDQueue
def ConnectDB():
    # xmlファイルの読み込み
    tree = ET.parse('MIKConfig.xml')

    # hostの読み込み
    dbhost = tree.find('DBHost').text
    # ユーザーの読み込み
    dbuser = tree.find('DBUser').text
    # パスワードの読み込み
    dbpass = tree.find('DBPassWd').text
    # 使用DBの読み込み
    dbuseDB = tree.find('UseDB').text

    # データベースへの接続とカーソルの生成
    return MySQLdb.connect(
        host=dbhost,
        user=dbuser,
        passwd=dbpass,
        db=dbuseDB)

def WriteEnterRecord(IDm):
    connection = ConnectDB()
    cursor = connection.cursor()
    # ここに実行したいコードを入力します
    stmt1 = "select user_id from m_user where user_IDm = %s"
    cursor.execute(stmt1, (IDm, ))
    # fetchone()で1件ずつ取り出し
    rows = cursor.fetchone()
    stmt2 = "insert into t_enter (user_id)values(%s)"
    cursor.execute(stmt2, (rows, ))

    # ユーザー名をLCDキューに入れる
    LCDQueue.put(rows[0])

    # 保存を実行
    connection.commit()

    # 接続を閉じる
    connection.close()

def WriteLeaveRecord(IDm):
    connection = ConnectDB()
    cursor = connection.cursor()

    # ここに実行したいコードを入力します
    stmt1 = "select user_id from m_user where user_IDm = %s"
    cursor.execute(stmt1, (IDm, ))
    # fetchone()で1件ずつ取り出し
    rows = cursor.fetchone()
    stmt2 = "insert into t_leave (user_id)values(%s)"
    cursor.execute(stmt2, (rows, ))

    # ユーザー名をLCDキューに入れる
    LCDQueue.put(rows[0])

    # 保存を実行
    connection.commit()

    # 接続を閉じる
    connection.close()

