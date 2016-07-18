#-*-coding:utf-8-*- 
import mysql
import MySQLdb


def bind_device(accountKey, userId, deviceId): 
    """register;deviceID:mdeviceID;userID:muserid;userKey:muserkey;"""

    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = """insert into developer_user_device (accountKey, userId, deviceId)""" + """values(%s,%s,%s)"""

    value = [accountKey, userId, deviceId]
     
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()


def remove_device(accountKey, userId, deviceId): 
    
    conn = mysql.connect_mysql()
    cur = conn.cursor()

    sql = '''DELETE FROM developer_user_device  WHERE (accountKey, userId,deviceId) in((%s, %s, %s))'''   
    value=[accountKey, userId, deviceId]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()


def list_devices(accountKey, userId): 
    
    conn = mysql.connect_mysql()
    cur = conn.cursor()

    sql = '''SELECT * FROM developer_user_device  WHERE (accountKey, userId) in((%s, %s))'''   
    value=[accountKey, userId]
    
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