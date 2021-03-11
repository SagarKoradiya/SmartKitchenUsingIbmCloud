import time
import sys
import ibmiotf.application
import ibmiotf.device
import random


organization = "d1lwhk"
deviceType = "nodemcu"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='Efanon':
                print("Exhaust Fan is on")
        elif i=='Efanoff':
                print("Exhaust Fan is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()

while True:
        
        jar = 50
        gas = 2
        gasw =1
        #Send Value  to IBM Watson
        data = {'d':{'jar' : jar, 'gas' : gas,'gasw' : gasw,}}
        
        #print (data)
        def myOnPublishCallback():
            print ("jar quantity is = %s %%" % jar,"Gas Sensor Value is = %s " % gas, "Cylinder Weight is = %s Kg" % gasw)    
        if jar <= 10 :
                print("Jar Quantity is Low.....Please fill the Jar !!!")
        if gas >10 :
                print("Gas Leakage Found.....Turn Off Gas knob .....Please Be alert !!!")
                print("please start Exhaust Fan")
        if gasw <=2:
                print("Gas Cylinder will Empty In next 5 Days.....Please Book your cylinder as soon as Possible !!!")
               
        
        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()


