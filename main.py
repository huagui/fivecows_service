#-*-coding:utf-8-*- 
import web
import time
import datetime
import MySQL.mysql
import MySQL.tableDevAccount
import MySQL.tableDevices
import traceback
import socket
import SocketServer
import myudpserver
import threading
import Http.device
import Http.command


urls = (
        '/','index',
        '/test', 'test', # for test
        # '/FiveCows/device/register','Http.device.register',# register device
        '/FiveCows/device/isOnline','Http.device.isOnline', # whether the device is online
        '/FiveCows/device/bind','Http.device.bind', 
        '/FiveCows/device/remove','Http.device.remove',
        '/FiveCows/device/list','Http.device.list',
        '/FiveCows/device/register','Http.device.register',
        '/FiveCows/device/update','Http.device.update',
        '/FiveCows/command/send','Http.command.send', # send command
        '/FiveCows/command/check','Http.command.check', 
        '/FiveCows/command/history','Http.command.history', 
       )

class index():
    def GET(self):
        return "home page"

class test:
    def GET(self):
      #data = web.input()
      #return "==> GET method , data : ",str(data)
      return "==> GET method"
    def POST(self):
      i = web.data()
        
      return "==> POST method , data : ",str(i)
      



web.webapi.internalerror = web.debugerror #show debug info
if __name__ == "__main__":
  try:
    threading.Thread(target=myudpserver.startservice).start()
    #threading.Thread(target=mytcpserver.startservice).start()
    #MySQL.mysql.keep_connection()

  except:
    print "fail to create threads"
    f=open("log.txt",'a')  
    traceback.print_exc(file=f)  
    f.flush()  
    f.close()
  app = web.application(urls, globals())
  app.run()
  
