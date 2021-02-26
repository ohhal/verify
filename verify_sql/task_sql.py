# -*- coding: utf-8 -*-
# @File: task_sql.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/28
# @Desc: task sql

import sqlite3
import time

from verify_sql.sql_config import exception_handler, tobe_verify_db_name

conn = sqlite3.connect(tobe_verify_db_name, check_same_thread=False)
cursor = conn.cursor()


@exception_handler
def created():
    cursor.execute('''CREATE TABLE TOBEVERIFY
           (task_id CHAR (50) PRIMARY KEY  NOT NULL ,
            web_key CHAR (50) ,
            expiration_time int (20),
            insertion_time int (20));''')
    conn.commit()


@exception_handler
def insert_task(task_id: str, web_key: str, expiration=60 * 1000):
    '''插入数据，expiration为过期时间，默认60s，单位ms'''
    insertion_time = str(int(time.time() * 1000))
    cursor.execute(
        "REPLACE  INTO TOBEVERIFY (task_id,web_key,expiration_time,insertion_time) VALUES ('%s','%s','%s','%s')" % (
            task_id, web_key, insertion_time, expiration))
    conn.commit()


@exception_handler
def delete_task(task_id: str):
    '''删除数据'''
    sql = "DELETE FROM TOBEVERIFY WHERE task_id='{}'".format(task_id)
    cursor.execute(sql)
    conn.commit()


@exception_handler
def select_task(web_key: str):
    '''根据网站查找已完成的task_id,随机返一个有效的task_id'''
    r_list = list()
    rows = cursor.execute(
        "SELECT task_id,expiration_time,insertion_time  FROM  TOBEVERIFY WHERE web_key='{}'".format(str(web_key)))
    now_time = int(time.time() * 1000)
    for row in rows:
        if now_time - int(row[2]) > int(row[1]):  # 超时直接删除
            delete_task(row[0])
            continue
        r_list.append(row[0])
    if len(r_list) > 0:
        return r_list[0]
    else:
        return False


if __name__ == "__main__":
    # created()
    # insert_task('asdsadasdwewqe','6LdLK0EUAAAAAOW4sWFiUm0FspjiEjX0pfhojEBt')
    a = select_task('6LdLK0EUAAAAAOW4sWFiUm0FspjiEjX0pfhojEBt')
    print(a)
