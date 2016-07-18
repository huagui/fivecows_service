#-*-coding:utf-8-*- 
import web
#import setting
import traceback
import MySQL.mysql
import MySQL.tableDevAccount
import MySQL.tableDevices
import MySQL.tableDUD
import time
import datetime
import json

import sys 
sys.path.append("..")
import setting


class update:
    def GET(self):
        data = web.input(
                        #deviceMac = None, 
                        deviceIp = '',
                        deviceWifi = '', 
                        devicePwd = '',
                        extraInfo = '',
                        deviceName = "新设备"
                        )
        try:
            accountKey = data.accountKey
            deviceMac = data.deviceMac
            deviceIp = data.deviceIp
            deviceWifi = data.deviceWifi
            devicePwd = data.devicePwd
            extraInfo = data.extraInfo
            deviceName = data.deviceName
        except:
            return '''{"error_code":101}'''

        try:
            code = check_account(accountKey, deviceMac)
            return_data = {"deviceId":deviceMac, "success":None, "error_code":code}
                   
            if code==0 or 203: # account is valid and device is registered
                result = MySQL.mysql.get_developer_account_by_key(accountKey) 
                developId = result[0]
                return_data["error_code"] = 0
                MySQL.tableDevices.update_device(DeveloperId=developId, DeviceMac=deviceMac, DeviceIp=deviceIp,
                                        DeviceWifi=deviceWifi, Devicepwd=devicePwd, ExtraInfo=extraInfo, DeviceName=deviceName)
                return_data["success"] = 1
                jsondata = json.dumps(return_data) 
                return jsondata
            else: 
                return_data["success"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata      
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''


class register:
    def GET(self):
        data = web.input(
                        #deviceMac = None, 
                        deviceIp = '',
                        deviceWifi = '', 
                        devicePwd = '',
                        extraInfo = '',
                        deviceName = "新设备"
                        )
        try:
            accountKey = data.accountKey
            deviceMac = data.deviceMac
            deviceIp = data.deviceIp
            deviceWifi = data.deviceWifi
            devicePwd = data.devicePwd
            extraInfo = data.extraInfo
            deviceName = data.deviceName
        except:
            return '''{"error_code":101}'''

        try:
            code = check_account(accountKey, deviceMac)
            return_data = {"deviceId":deviceMac, "success":None, "error_code":code}
            if code == 101 or code == 103: # account is invalid or accountKey is wrong
                return_data["success"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata              
            else:
                result = MySQL.mysql.get_developer_account_by_key(accountKey) 
                developId = result[0]
                return_data["error_code"] = 0
                MySQL.tableDevices.register_device(DeveloperId=developId, DeviceMac=deviceMac, DeviceIp=deviceIp,
                                        DeviceWifi=deviceWifi, Devicepwd=devicePwd, ExtraInfo=extraInfo, DeviceName=deviceName)
                return_data["success"] = 1
                jsondata = json.dumps(return_data) 
                return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''


class bind:
    def GET(self):
        data = web.input()
        try:
            accountKey = data.accountKey
            deviceId = data.deviceId
            userId = data.userId
        except:
            return '''{"error_code":101}''' 

        try:
            code = check_account(accountKey, deviceId)
            return_data = {"deviceId":deviceId, "success":None, "error_code":code}
            if code == 0 or code == 203: # account is valid
                MySQL.tableDUD.bind_device(accountKey, userId, deviceId)
                return_data["success"] = 1
                return_data["error_code"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata
            else:
                return_data["success"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''

class remove:
    def GET(self):
        data = web.input()
        try:
            accountKey = data.accountKey
            deviceId = data.deviceId
            userId = data.userId
        except:
            return '''{"error_code":101}''' 

        try:
            code = check_account(accountKey, deviceId)
            return_data = {"deviceId":deviceId, "success":None, "error_code":code}
            if code == 0 or code == 203: # account is valid
                MySQL.tableDUD.remove_device(accountKey, userId, deviceId)
                return_data["success"] = 1
                return_data["error_code"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata
            else:
                return_data["success"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''

class list:
    def GET(self):
        data = web.input()
        try:
            accountKey = data.accountKey
            userId = data.userId
        except:
            return '''{"error_code":101}''' 

        try:
            code = check_account(accountKey, deviceId=None)
            return_data = {"success":None, "error_code":code}
            if code == 0 or code == 203 or 201: # account is valid
                result_list = MySQL.tableDUD.list_devices(accountKey, userId)


                devices_list = []
                for result in result_list:
                    devices_list.append( [{"deviceName":result[1] }, {"deviceId":result[2] }] )

                return_data["devices_list"] =  devices_list  
                return_data["success"] = 1
                return_data["error_code"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata
            else:
                return_data["success"] = 0
                jsondata = json.dumps(return_data) 
                return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''


class isOnline:
    def GET(self):
        data = web.input()
        # return str(data)
        try:
            accountKey = data.accountKey
            deviceId = data.deviceId
        except:
            return '''{"error_code":101}''' 

        try:
            #now = datetime.datetime.now()
            code = check_account(accountKey, deviceId)
            status = 0

            if code == 0: # device is online
                status = 1   
            else:
                status = 0

            return_data = {"deviceId":deviceId, "isOnline":status, "error_code":code}
            jsondata = json.dumps(return_data) 
            return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''


def check_account(accountKey, deviceId):
    try:
        invalid = MySQL.tableDevAccount.isInvalid(accountKey)
        if invalid == "work":  #whether developer account works 
            developerId = MySQL.tableDevAccount.get_account_by_key(accountKey)[0] #get developerId in table develop_account
            mac = MySQL.tableDevices.get_device_by_mac(deviceId) 
            
            if mac == None:
                return 201 #"device is not registered"
            else:
                developerId_in_table_Devices = mac[7]
            
                if  developerId == developerId_in_table_Devices:
                    #return "device is online" 
                    return isOnline(deviceId)
                else:
                    return 202 #"this device does not belong the developer"

        else:
            if invalid == "invalid":
                return 102 #"developer account is invalid"
            if invalid == "not exist":
                return 103 #"key is wrong"
    except :
        f=open("log.txt",'a')  
        traceback.print_exc(file=f)  
        f.flush()  
        f.close()


def isOnline(mac):
    result = MySQL.mysql.get_by_id(mac)
    if result == None:
        return 203 #"this device is offline"
    else:
        now = datetime.datetime.now()
        updateTime = result[5]
        offlineTime = (now-updateTime).seconds
        if offlineTime <= setting.BEATTIM * 2:
            #return "device is online and it sent Heartbeat before " + str(offlineTime) + " seconds ago" 
            return 0
        else:
            #return "device is offline and it sent Heartbeat before " + str(offlineTime) + " seconds ago" 
            return 203

def send_to_device(deviceId, userId, command):

    device_data = MySQL.mysql.get_by_id(deviceId)
    if device_data == None:
        return -1
    device_ip = device_data[3]
    device_port = str(device_data[4])

    #return device_ip,device_port
    msg = "command:" + command + ";" + "userId" + userId + ";"
    #return myudpserver.socket_dict
    try:
        socket = setting.socket_dict[str(deviceId)]
        socket.sendto(msg, (device_ip, int(device_port)))
    except:
        f=open("log.txt",'a')  
        traceback.print_exc(file=f)  
        f.flush()  
        f.close()  
        return -1
    else:
        return 0