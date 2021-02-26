# -*- coding: utf-8 -*-
# @File: log_sql.py
# @Author: https://github.com/ohhal
# @Date: 2021/02/03
# @Desc: web日志查询sql


import sqlite3
import time

from verify_sql.sql_config import verify_log_db, exception_handler

conn = sqlite3.connect(verify_log_db, check_same_thread=False)
cursor = conn.cursor()


@exception_handler
def created(table_name):
    cursor.execute(f'''CREATE TABLE {table_name}
           (id CHAR (20) NOT NULL ,
            api CHAR(20),
            change_time CHAR(20),
            log longtext,
            PRIMARY KEY (`id`,`change_time`));''')
    conn.commit()


@exception_handler
def insert(table_name, id, api, logger):
    change_time = str(int(time.time() * 1000 * 1000))
    cursor.execute(
        "REPLACE  INTO '%s' (id,api,change_time,log) VALUES ('%s','%s','%s','%s')" % (
            table_name, id, api, change_time, logger))
    conn.commit()


def _get_current_date():
    timeStamp = int(time.time())
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y%m%d", timeArray)


@exception_handler
def logsql(id, api, logger):
    current_date = _get_current_date()
    table_name = f'VERIFYLOG_{current_date}'
    created(table_name)
    insert(table_name, id, api, logger)


def _get_date(timeStamp):
    timeArray = time.localtime(int(timeStamp/1000))
    return time.strftime("%Y%m%d", timeArray)


@exception_handler
def select_log(timestamp: int = None, search: str = None, type: str = 'id'):
    '''
    id,search二选一
    :param timestamp:1612322928549
    :type timestamp: int
    :param type:choose['id','log']
    :type type:选择查询方式
    :param search:唯一id或log中的参数
    :type search:str
    :return:
    :rtype:
    '''
    table_list = _list_table()
    if timestamp:
        table = f"VERIFYLOG_{_get_date(timestamp)}"
        print(table)
        if table in table_list:
            table_list = [table]
    r_list = list()
    table_list = table_list
    for table_name in table_list:
        sqls = set()
        if search:
            if type == 'id':
                sqls.add(f'SELECT * from {table_name} WHERE id="{search}"')
            else:
                sqlid = f'SELECT id from {table_name} where log Like "%{search}%"'
                rs = cursor.execute(sqlid)
                for r in rs:
                    sqls.add(f'SELECT * from {table_name} WHERE id="{r[0]}"')
        else:
            sqls.add(f'SELECT * from {table_name}')
        for sql in sqls:
            rows = cursor.execute(sql)
            for row in rows:
                data = dict()
                data['id'] = row[0]
                data['api'] = row[1]
                data['time'] = row[2]
                data['log'] = row[3]
                r_list.append(data)
    return r_list


@exception_handler
def select_log_id(timestamp: int = None, search: str = None, type: str = 'id'):
    table_list = _list_table()
    select_table = list()
    if timestamp:
        table = f"VERIFYLOG_{_get_date(timestamp)}"
        if table in table_list:
            select_table.append(table)
    else:
        select_table = table_list
    r_list = list()
    for table_name in select_table:
        sqls = set()
        if search:
            if type == 'id':
                sqls.add(f'SELECT id,max(cast(change_time as int)) from {table_name} WHERE id="{search}"')
            else:
                sqlid = f'SELECT id,max(cast(change_time as int)) from {table_name}  where log Like "%{search}%" group by id'
                sqls.add(sqlid)
        else:
            sqls.add(f'SELECT id,max(cast(change_time as int)) from {table_name} group by id')
        for sql in sqls:
            rows = cursor.execute(sql)
            for row in rows:
                data = dict()
                data['id'] = row[0]
                data['table'] = table_name
                data['time'] = row[1]
                if data not in r_list:
                    r_list.append(data)
    return r_list


def _list_table():
    results = []
    cursor.execute('''select name from sqlite_master where type='table' order by name''')
    result = cursor.fetchall()
    for i in result:
        results.append(i[0])
    return results


if __name__ == '__main__':
    # a = created()
    # print(a)
    # logsql('asdasdasd','/task','test')
    # ad = select_log_id()
    # print(ad)
    a = _get_date(1612195200000)
    # print(ad)
    # a = select()
    print(a)
