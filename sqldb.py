# coding=utf-8
import os
import datetime
import sqlite3



class DbManager:
    def __init__(self):
        self.db_file = ".\\car.db"
        self._conn = sqlite3.connect(self.db_file)

    def create_table(self):
        sql = ''' create table if not exists carinfo (
            id integer primary key autoincrement,
            license text,
            entertime text,
            exittime text,
            flag integer
        )'''
        with self._conn:
            cur = self._conn.cursor()
            cur.execute(sql)

    def insert_info(self, car_license):
        cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        new_data = "insert into carinfo (license, entertime, exittime, flag) values ('%s', '%s', '%s', %d)" %(car_license, cur_time, 'null', 0)

        check = "select license, flag from carinfo where license == '%s'" %car_license
        print(check)
        
        
        with self._conn:
            cur = self._conn.cursor()
            cur.execute(check)
            query_result = cur.fetchall()
            num = len(query_result)
            if num == 0:
                cur.execute(new_data)
            else:
                flag = query_result[0][1]
                carlicense = query_result[0][0]
                if flag == 0:
                    ## update exittime
                    update_exittime = "update carinfo set exittime='%s', flag=1 where license=='%s'" %(cur_time, carlicense)
                    cur.execute(update_exittime)
                else:
                    #update entertime
                    update_entertime = "update carinfo set entertime='%s', flag=0, exittime='null' where license=='%s'" %(cur_time, carlicense)
                    cur.execute(update_entertime)
                
