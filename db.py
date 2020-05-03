# coding=utf-8
import os
import logging
import pymysql
from DBUtils.PooledDB import PooledDB


class DbManager:
    def __init__(self):
        self._pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，
            # 因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论
            # 设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=1,
            # ping MySQL服务端，检查是否服务可用。
            # 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created,
            # 4 = when a query is executed, 7 = always
            host='127.0.0.1',
            port=3306,
            user='root',  # 用户名
            password=None,  # 密码, None 或者字符串
            database='offline',  # 库名
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor  # 配置数据已字典的类型返回，不配置返回元组
            # 在默认情况下cursor方法返回的是BaseCursor类型对象，BaseCursor类型对象在执行查询后每条记录的结果以列表(list)表示。
            # 如果要返回字典(dict)表示的记录，就要设置cursorclass参数为pymysql.cursors.DictCursor类。
        )

    def getConn(self):
        return self._pool.connection()


##_dbManager = DbManager()


def getConn():
    """ 获取数据库连接 """
    return _dbManager.getConn()


def executeAndGetId(sql, param=None):
    """ 执行插入语句并获取自增id """
    conn = getConn()
    cursor = conn.cursor()
    if param == None:
        cursor.execute(sql)
    else:
        cursor.execute(sql, param)
    id = cursor.lastrowid
    cursor.close()
    conn.close()
    return id


def execute(sql, param=None):
    """ 执行sql语句 """
    logging.debug("DB.Execute: Running[%s]" % sql)
    conn = getConn()
    cursor = conn.cursor()
    if param == None:
        rowcount = cursor.execute(sql)
    else:
        rowcount = cursor.execute(sql, param)
    cursor.close()
    conn.close()
    return rowcount


def execute_with_commit(sql):
    # insert, update
    logging.debug("DB.ExecuteWithCommit: Running[%s]" % sql)
    conn = getConn()
    cursor = conn.cursor()
    is_succ = False
    try:
        rowcount = cursor.execute(sql)
        conn.commit()
        is_succ = True
    except Exception as e:
        logging.error("DB.ExecuteWithCommit: Error[%s], Rollingback" % str(e))
        conn.rollback()
        is_succ = False
    finally:
        cursor.close()
        conn.close()
    return is_succ


def queryOne(sql):
    """ 获取一条信息 """
    conn = getConn()
    cursor = conn.cursor()
    rowcount = cursor.execute(sql)
    if rowcount > 0:
        res = cursor.fetchone()
    else:
        res = None
    cursor.close()
    conn.close()
    return res


def queryAll(sql):
    """ 获取所有信息 """
    logging.debug("DB.QueryAll: Running[%s]" % sql)
    conn = getConn()
    cursor = conn.cursor()
    rowcount = cursor.execute(sql)
    if rowcount > 0:
        res = cursor.fetchall()
    else:
        res = None
    cursor.close()
    conn.close()
    return res
