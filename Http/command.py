#-*-coding:utf-8-*- 
import web
#import setting
import traceback
import MySQL.mysql
import MySQL.tableDevAccount
import MySQL.tableDevices
import MySQL.tableDUD
import MySQL.tableCommands
import time
import datetime
import json
import device

import sys 
sys.path.append("..")
import setting

class send:
    def GET(self):
        data = web.input()
        try: #get params
            accountKey = data.accountKey
            deviceId = data.deviceId
            command = data.command
            userId = data.userId
        except:
            return '''{"error_code":101}'''#"params are wrong"
        #return deviceId,command

        code = device.check_account(accountKey, deviceId)
        return_data = {"deviceId":deviceId, "error_code":code,"command":command,"userId":userId,"success":None}
        #global response
        if code == 0: # device is online
            pass   
        else:
            return_data["success"] = 0
            jsondata = json.dumps(return_data)
            return jsondata

        try:
        	binding_device = MySQL.tableDUD.list_devices(accountKey, userId) #get the list of  binding devices
        	deviceId_list = []
        	for item in binding_device:
        		deviceId_list.append(item[2])

        	if deviceId in deviceId_list:  # if user had bind this device
	            if device.send_to_device(str(deviceId), str(userId), command) == 0: #send msg to device successful
	            	MySQL.tableCommands.insert(deviceId, userId, command)
	                return_data["success"] = 1
	                jsondata = json.dumps(return_data) 
	                return jsondata
	            else:
	                return_data["success"] = 0
	                return_data["error_code"] = 301
	                jsondata = json.dumps(return_data) 
	                return jsondata
	        else:
	        	return_data["error_code"] = 302
	        	return_data["success"] = 0
	        	jsondata = json.dumps(return_data) 
	        	return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''


class check:
    def GET(self):
        data = web.input()
        try: #get params
            accountKey = data.accountKey
            deviceId = data.deviceId
            userId = data.userId
        except:
            return '''{"error_code":101}'''#"params are wrong"

        code = device.check_account(accountKey, deviceId)
        return_data = {"deviceId":deviceId, "error_code":code, "userId":userId}

        if code == 0 or code == 203: # device is online
            pass   
        else:
            return_data["success"] = 0
            jsondata = json.dumps(return_data)
            return jsondata

        try:
            result = MySQL.tableCommands.get_last(deviceId, userId) #get the last command 
            if result == None:
                return_data["error_code"] = 303
                return_data["success"] = 0
                jsondata = json.dumps(return_data)
                return jsondata
            else:
                status = result[4] 
                return_data["success"] = 1
                return_data["status"] = status
                try:
                    return_data["response"] = setting.response[deviceId][userId]
                except:
                    return_data["response"] = ''
                jsondata = json.dumps(return_data)
                return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''


class history:
    def GET(self):
        data = web.input(num=5)
        try: #get params
            accountKey = data.accountKey
            deviceId = data.deviceId
            userId = data.userId
            num = data.num
        except:
            return '''{"error_code":101}'''#"params are wrong"

        code = device.check_account(accountKey, deviceId)
        return_data = {"deviceId":deviceId, "error_code":code, "userId":userId}

        if code == 0 or code == 203: # device is online
            pass   
        else:
            return_data["success"] = 0
            jsondata = json.dumps(return_data)
            return jsondata

        try:
            if num > 15: 
                num = 15
            if num < 1:
                num = 5
            result = MySQL.tableCommands.get_history(deviceId, userId, int(num)) #get history 
            if result == None:
                return_data["error_code"] = 303
                return_data["success"] = 0
                jsondata = json.dumps(return_data)
                return jsondata
            else:
                command_history = []
                for item in result:
                    command_history.append(item[3])
                return_data["success"] = 1
                return_data["command_history"] = command_history
                jsondata = json.dumps(return_data)
                return jsondata
        except:
            f=open("log.txt",'a')  
            traceback.print_exc(file=f)  
            f.flush()  
            f.close()
            return '''{"error_code":104}'''