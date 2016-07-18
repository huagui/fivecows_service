#-*-coding:utf-8-*- 
import mysql
import MySQLdb


def register_device(DeviceMac, DeviceIp,
    DeviceWifi, Devicepwd, ExtraInfo, DeveloperId, DeviceName, catId=1, 
    Status=1):  #insert the info of device into table
    """register;deviceID:mdeviceID;userID:muserid;userKey:muserkey;"""

    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = """insert into devices (deviceName, deviceMac, deviceIp,
             deviceWifi, devicepwd, extraInfo, developerId, catId, status)""" \
        + """values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    value = [DeviceName, DeviceMac, DeviceIp,
        DeviceWifi, Devicepwd, ExtraInfo, DeveloperId, catId, Status]
     
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()

def update_device(DeviceMac, DeviceIp,
    DeviceWifi, Devicepwd, ExtraInfo, DeveloperId, DeviceName, catId=1, 
    Status=1):  # update the info of device  
    """register;deviceID:mdeviceID;userID:muserid;userKey:muserkey;"""

    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = 'update devices ' + \
          """set deviceName=%s, deviceIp=%s, deviceWifi=%s, 
          devicepwd=%s, extraInfo=%s, developerId=%s, catId=%s, status=%s
           where deviceMac=%s"""

    value = [DeviceName, DeviceIp, DeviceWifi, Devicepwd, 
                ExtraInfo, DeveloperId ,catId, Status, DeviceMac]
     
    try:
        cur.execute(sql,value)
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    conn.commit()
    cur.close()
    conn.close()

def get_device_by_mac(mac):

    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = 'select * from devices '+ 'WHERE deviceMac=%s'
    value=[mac]
    
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


def isExist(mac): 

	if get_device_by_mac(mac) == None:
		return  False
	else:
		return True


def get_device_by_developerId(developerId):

    conn = mysql.connect_mysql()
    cur = conn.cursor()
    sql = 'select * from devices '+ 'WHERE developerId=%s'
    value=[developerId]
    
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
