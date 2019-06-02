#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import Queue
import time

DbQueue = Queue.Queue()
class DBOrder:
   def __init__(self, direct, IDm):
    self.direct = direct
    self.IDm = IDm

class RECORD_DIRECTION():
    ENTER_RECORD = 0
    LEAVE_RECORD = 1

def DBProc1():
    while True:
        if not DbQueue.empty():
            item = DbQueue.get()
            print("receive")
            #import pdb; pdb.set_trace()
            if item.direct == RECORD_DIRECTION.ENTER_RECORD:
                WriteEnterRecord(item.IDm)
            elif item.direct == RECORD_DIRECTION.LEAVE_RECORD:
                WriteLeaveRecord(item.IDm)
                
# MySQLdbのインポート
import MySQLdb
def WriteEnterRecord(IDm):
    # データベースへの接続とカーソルの生成
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='root',
        db='MIK')
    cursor = connection.cursor()
    
    # ここに実行したいコードを入力します
    stmt1 = "select user_id from m_user where user_IDm = %s"
    cursor.execute(stmt1, (IDm, ))
    # fetchone()で1件ずつ取り出し
    rows = cursor.fetchone()
    stmt2 = "insert into t_enter (user_id)values(%s)"
    cursor.execute(stmt2, (rows, ))

    # 保存を実行
    connection.commit()
    
    # 接続を閉じる
    connection.close()

def WriteLeaveRecord(IDm): 
    # データベースへの接続とカーソルの生成
    connection = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='root',
        db='MIK')
    cursor = connection.cursor()
    
    # ここに実行したいコードを入力します
    stmt1 = "select user_id from m_user where user_IDm = %s"
    cursor.execute(stmt1, (IDm, ))
    # fetchone()で1件ずつ取り出し
    rows = cursor.fetchone()
    stmt2 = "insert into t_leave (user_id)values(%s)"
    cursor.execute(stmt2, (rows, ))

    # 保存を実行
    connection.commit()
    
    # 接続を閉じる
    connection.close()

    