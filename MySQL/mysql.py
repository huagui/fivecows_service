#-*-coding:utf-8-*- 
import MySQLdb, time
import traceback
import threading

HOST = 'localhost'
USER = 'root'
PASSWD = '4c1fadc64b' #4c1fadc64b
PORT = 3306
DBNAME = 'fivecows'
TABLE = 'ipinfo'
socket = "/tmp/mysql.sock"
TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

try:
    conn=MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,port=PORT,unix_socket=socket, charset="utf8")
    conn.select_db("fivecows")
    cur=conn.cursor()
    
    # try:  #check and  create database if it doesn't exist
    #     cur.execute('create database if not exists %s'%DBNAME)
    # except:
    #     print(" fail to create database ")
    # finally:
    #     conn.select_db(DBNAME)
    # cur.close()

    try:   #check or create table if it doesn't exist
        cur.execute('''create table if not exists %s(  
                DeviceId CHAR(40) NOT NULL,  
                UserId VARCHAR(10) NOT NULL,  
                UserKey VARCHAR(10) NOT NULL,  
                Ip VARCHAR(15) NOT NULL,  
                Port INT(5) NOT NULL,   
                UpdateTime datetime default NULL, 
                PRIMARY KEY (DeviceId))  
                '''%TABLE)
    except:
        print("fail to create table")

    conn.commit()
    cur.close()
except MySQLdb.Error,e:
     print "Mysql Error %d: %s" % (e.args[0], e.args[1])


def connect_mysql():
    try:
        conn=MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,port=PORT,unix_socket=socket, charset="utf8")
        conn.select_db("fivecows")
        return conn
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
     
def keep_connection():
    cur = conn.cursor()
    # sql = 'select * from devices'
    sql = "set wait_timeout=24*3600"
    
    try:
        cur.execute(sql)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    #result = cur.fetchall()
    #result = cur.fetchone()
    #print result
    cur.close()
    # timer = threading.Timer(3600, keep_connection)
    # timer.start()

def get_developer_account_by_key(key): 
    conn = connect_mysql()
    cur = conn.cursor()

    sql = 'select * from developer_account '+ 'WHERE accountKey=%s'
    value=[key]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    # result = cur.fetchall()
    result = cur.fetchone()
    cur.fetchall()
    cur.close()
    conn.close()
    return result





     
def create(DeviceId, UserId, UserKey, Ip, Port):  #insert a new line into the table
    conn = connect_mysql()
    cur = conn.cursor()
    current_time = time.strftime(TIMEFORMAT, time.localtime()) 
    sql = 'insert into %s '%TABLE + 'values(%s,%s,%s,%s,%s,%s)'
    value=[DeviceId, UserId, UserKey, Ip, Port, current_time]
     
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()
        
def update(DeviceId, Ip, Port): #update a line in the table
    conn = connect_mysql()
    cur = conn.cursor()
    current_time = time.strftime(TIMEFORMAT, time.localtime()) 
    sql = 'update %s '%TABLE + \
          'set Ip=%s, Port=%s, UpdateTime=%s where DeviceId=%s'
    value=[ Ip, Port, current_time, DeviceId]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()

def delete(DeviceId): #delete a line from the table
    conn = connect_mysql()
    cur = conn.cursor()
    sql = '''DELETE FROM developer_user_device  WHERE'''\
        +  '''(accountKey, userId,deviceId) in((%s, %s, %s))'''
    value=[DeviceId]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()

def get_by_id(DeviceId):
    conn = connect_mysql()
    cur = conn.cursor()
    sql = 'select * from %s '%TABLE + 'WHERE DeviceId=%s'
    value=[DeviceId]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    #result = cur.fetchall()
    result = cur.fetchone()
    cur.fetchall()
    cur.close()
    conn.close()
    return result

if __name__ == "__main__":
    
    # update(1, "192.168.255.255", 1234)
    #delete(5)
    print get_by_id("d0:10:00:0")
    #send_to_device("d0:10:00:0","start")
    #create(5,"huagui","falkdjf", '192.168.121.215', 55552,time.strftime(TIMEFORMAT, time.localtime()))
    #update(5,'192.168.121.220', 12354,time.strftime(TIMEFORMAT, time.localtime()))
