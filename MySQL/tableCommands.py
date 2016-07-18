#-*-coding:utf-8-*- 
import mysql
import MySQLdb


def insert(deviceId, userId, command, status=1):  
    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = """insert into commands (deviceId, userId, command, status)""" \
        + """values(%s,%s,%s,%s)"""

    value = [deviceId, userId, command, status]
     
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()


def get_last(deviceId, userId): 
    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = '''select * from commands  WHERE  (deviceId, userId) in((%s,%s)) ORDER BY commandId DESC'''
    value=[deviceId, userId]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    # result = cur.fetchall()
    result = cur.fetchone() 
    cur.close()
    conn.close()
    return result


def get_history(deviceId, userId, num):
    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = '''select * from commands  WHERE  (deviceId, userId) in((%s,%s)) ORDER BY commandId DESC LIMIT 1,%s'''   
    value=[deviceId, userId, num]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    result = cur.fetchall()
    # result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def alter_status(deviceId, userId, status):
    conn = mysql.connect_mysql()
    cur = conn.cursor() 
    sql = '''update  commands set status=%s   WHERE  (deviceId, userId) in((%s,%s))  order by commandId desc limit 1'''
    value=[ status, deviceId, userId]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return -1
    conn.commit()
    cur.close()
    conn.close()
    return 0