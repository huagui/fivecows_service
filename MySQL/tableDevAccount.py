#-*-coding:utf-8-*- 
import mysql
import MySQLdb


def get_account_by_key(key):
    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = 'select * from developer_account '+ 'WHERE accountKey=%s'
    value=[key]
    
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    #result = cur.fetchall()
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def isInvalid(key): 

    result = get_account_by_key(key)
    if result == None:
		return  "not exist"  #  means  that account does not exist 
    else:
    	if result[9] == 1:
    		return  "invalid" #　means  that account is invalid  
        if result[9] == 0:
            return "work" #　means  that account works 