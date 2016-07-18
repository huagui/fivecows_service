#-*-coding:utf-8-*- 
"""
udpserver module

This module is uesd for communicating with devices by udp
"""

import SocketServer
import MySQL.mysql
import MySQL.tableDevices
import MySQL.tableCommands
import Http.device
import threading
import traceback
import setting

import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

HOST = "" #localhost
PORT = 54321


# mutex = threading.Lock() #create a lock for handling database
                  
class MyUDPHandler(SocketServer.BaseRequestHandler):
  
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        if "connection" in data:
            socket.sendto("success", self.client_address)
        handle_msg(data, self.client_address, socket)
        
        print "{} wrote:".format(self.client_address[0])
        print data
        
        
def handle_msg(data, addr, socket):
    '''
    addr[0] is ip ,addr[1] is port
    '''
    # global socket_dict
    if "connection" in data:

        if "deviceID" in data and "userID" in data and "userKey" in data : 
        #msg format: connection;userID:tommego;userKey:123456;deviceID:d0:10:00:00:00:e1;attachDatas:device extra heart data;
            
            try:
                UserKey  = data.split("userKey:")[1].split(";")[0]
                DeviceId = data.split("deviceID:")[1].split(";")[0]
                UserId   = data.split("userID:")[1].split(";")[0]
                code = Http.device.check_account(UserKey, DeviceId)
                if code == 203 or code ==  0:
                    pass
                else:
                    error_msg = '''error_code:{};'''.format(code)
                    socket.sendto(error_msg, addr)
                setting.socket_dict[DeviceId] = socket

                # global mutex  
                # if mutex.acquire(): 
                if MySQL.tableDevices.isExist(DeviceId): #whether this device is registered 

                    if MySQL.mysql.get_by_id(DeviceId) == None: 
                        MySQL.mysql.create(DeviceId, UserId, UserKey, addr[0], addr[1]) #id,ip,port
                    else:
                        MySQL.mysql.update(DeviceId, addr[0], addr[1])
                
                # mutex.release() 

            except:
                f=open("log.txt",'a')  
                traceback.print_exc(file=f)  
                f.flush()  
                f.close() 
                error_msg = '''error_code:104;'''
                socket.sendto(error_msg, addr)
        else:
            error_msg = '''error_code:101;'''
            socket.sendto(error_msg, addr)
            
    if "response" in data: # msg format: response:xxxxxx;userId:xxxx;accountKey:xxx;deviceID:d0:10:00:00:00:e1;success:x;
        if "deviceID"   in data and "userID" in data and "success" in data and "accountKey" in data:
            
            try:
                UserId = data.split("userID:")[1].split(";")[0]
                DeviceId = data.split("deviceID:")[1].split(";")[0]
                Response = data.split("response:")[1].split(";")[0]
                Success = data.split("success:")[1].split(";")[0]
                UserKey = data.split("accountKey:")[1].split(";")[0]

                code = Http.device.check_account(UserKey, DeviceId)
                if code == 203 or code ==  0:
                    pass
                else:
                    error_msg = '''error_code:{};'''.format(code)
                    socket.sendto(error_msg, addr)

                setting.response[DeviceId] = {}
                setting.response[DeviceId][UserId] = Response 
                if Success == '1':
                    MySQL.tableCommands.alter_status(DeviceId, UserId, status=3) #command is process 
                if Success == '0':
                    MySQL.tableCommands.alter_status(DeviceId, UserId, status=2) #device received msg
                # print setting.response[DeviceId]
            except:
                f=open("log.txt",'a')  
                traceback.print_exc(file=f)  
                f.flush()  
                f.close()  
        else:
            error_msg = '''error_code:101;'''
            socket.sendto(error_msg, addr)

    if "register" in data: # register:deviceMac:xxxx;deviceIp:xxxx;deviceWifi:xxxx;devicePwd:xxxx;extraInfo:xxxx;accountKey:abcdefgh;
        register(data, addr, socket)

def register(data, addr, socket):
    try:
        # deviceMac = None
        deviceIp = None
        deviceWifi = None
        devicePwd = None
        extraInfo = None
        deviceName = "新设备"
        if "accountKey"   in data:
                accountKey = data.split("accountKey:")[1].split(";")[0]
        if "deviceMac" in data:
                deviceMac   = data.split("deviceMac:")[1].split(";")[0]
        if "deviceIp" in data:
                deviceIp = data.split("deviceIp:")[1].split(";")[0]
        if "deviceWifi" in data:
                deviceWifi = data.split("deviceWifi:")[1].split(";")[0]
        if "devicePwd" in data:
                devicePwd = data.split("devicePwd:")[1].split(";")[0]
        if "extraInfo" in data:
                extraInfo = data.split("extraInfo:")[1].split(";")[0]
        if "deviceName" in data:
                deviceName = data.split("deviceName:")[1].split(";")[0]

        code = Http.device.check_account(accountKey, deviceMac)
        if code == 203 or code ==  0 or code == 201:
            pass
        else:
            error_msg = '''error_code:{};'''.format(code)
            socket.sendto(error_msg, addr)

   
        result = MySQL.mysql.get_developer_account_by_key(accountKey) 
        if result == None:  # check that whether the accountKey exsit
            pass
        else:
            developId = result[0]

            if MySQL.tableDevices.isExist(deviceMac): # whether this device is registered 
                MySQL.tableDevices.update_device(DeveloperId=developId, DeviceMac=deviceMac, DeviceIp=deviceIp,
                                    DeviceWifi=deviceWifi, Devicepwd=devicePwd, ExtraInfo=extraInfo,  DeviceName=deviceName)
            else:
                MySQL.tableDevices.register_device(DeveloperId=developId, DeviceMac=deviceMac, DeviceIp=deviceIp,
                                    DeviceWifi=deviceWifi, Devicepwd=devicePwd, ExtraInfo=extraInfo, DeviceName=deviceName)

        error_msg = '''success:1;'''
        socket.sendto(error_msg, addr)
    except:
        f=open("log.txt",'a')  
        traceback.print_exc(file=f)  
        f.flush()  
        f.close()
        # print "注册信息格式出错，注册失败"
        



def startservice():
    """
    start udp service
    """
    server = SocketServer.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()

if __name__ == "__main__":
    
    
    startservice()
