# -*- coding: utf-8 -*-
# @File: task_sql.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/28
# @Desc: 平台sql
import sqlite3
import time

from verify_sql.sql_config import exception_handler, flask_app_db

conn = sqlite3.connect(flask_app_db, check_same_thread=False)
cursor = conn.cursor()


@exception_handler
def created():
    cursor.execute('''CREATE TABLE VERIFYAPP
           (name CHAR (20) PRIMARY KEY  NOT NULL ,
            current_platform CHAR(20),
            change_time CHAR(20));''')
    conn.commit()


@exception_handler
def modify(current_platform):
    change_time = str(int(time.time() * 1000))
    cursor.execute(
        "REPLACE  INTO VERIFYAPP (name,current_platform,change_time) VALUES ('change_platform','%s','%s')" % (
            current_platform, change_time))
    conn.commit()


@exception_handler
def select():
    r_list = list()
    rows = cursor.execute('SELECT current_platform from VERIFYAPP')
    for row in rows:
        current_platform = row[0]
        r_list.append(current_platform)
    return r_list[0]


if __name__ == '__main__':
    # created()
    ad = modify('anti')
    print(ad)
    a = select()
    print(a)
