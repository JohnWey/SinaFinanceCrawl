# -*- coding: UTF-8 -*-

import ConfigParser
import MySQLdb
import sys



def init_db(conf,tar_dbname):
    try:
        conn = MySQLdb.connect(host=conf.get(tar_dbname, 'host'),
                    user=conf.get(tar_dbname, 'user'),
                    passwd=conf.get(tar_dbname, 'passwd'),
                    db=conf.get(tar_dbname, 'db'),
                    charset='utf8')
        return conn
    except:
        print "Error:数据库连接错误"
    return None

def select_demo(conn, sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except MySQLdb.Error, e:
        try:
            sqlError = "Error %d:%s" % (e.args[0], e.args[1])
            print sqlError
            return None
        except IndexError:
            print "MySQL Error:%s" % str(e)

    finally:
        conn.close()


def update_demo():
    pass

def delete_demo():
    pass

#这里的data是个tuple
def insert_demo(conn,tabname,hdngs,data):
    try:

        cursor = conn.cursor()

        #构造sql
        #构造表头字段名称
        #headings = ','.join([x for x in hdngs])

        #构造Value部分
        '''
        for record in data:
            record_fmt = ','.join(
                [str(s) if isinstance(s, int) else '\'' + s + '\'' for s in list(record)])  # 为什么str(x)是tuple类型？
           # sql = 'insert into ' + tabname + ' ( ' + headings + ' ) values ( ' + record_fmt + ');'
        '''
        sql = 'insert into ' + tabname + ' ( ' + hdngs + ' ) values ( ' + data + ');'
        #print sql

        cursor.execute(sql)
        conn.commit()
        return 0

    except MySQLdb.Error,e:
        try:
            sqlError = "Error %d:%s" % (e.args[0], e.args[1])
            print sqlError
            print sql
            return -1
        except IndexError:
            print "MySQL Error:%s" % str(e)
    finally:
        cursor.close()

def close_conn(conn):
    conn.close()

if __name__ == '__main__':
    conf = ConfigParser.ConfigParser()
    conf.read('mysql.conf')
    proc = conf.get('Database', 'table_name')
    proc_fmt='\''+proc.replace(',','\',\'')+'\''
    conn = init_db()
    sql = "select body from mysql.proc where db = 'cscecdw' and `type` = 'PROCEDURE' and name in ("+proc_fmt+")"
    data = select_demo(conn, sql)

    with open('C:\\Users\\admin\\Desktop\\t1.txt', 'w') as f:
        for row in data:
            line=str(row[0])
            f.write(line+'\n')


