#code for Makeblock mBot2

#micropython and Makeblock mBot2 libs
import _thread, machine
import cyberpi, mbot2, time
from simple_mqtt import MQTTClient
import network

#sets of functions
def sub_cb(topic, msg): #MQTT broker listener handler
    global mBotGo
    if 'HUMAN' in msg: #there is no alarm
        mBotGo = 0
    if 'GHOST' in msg: #there is alarm
        mBotGo = 1

#MQTT listener, LEDs and moving commands run in multithread

def thread1(): #thread to listen to MQTT broker 
#this on will be a MAIN thread
    while True:
        client.wait_msg()
    
def thread2(): #thread to react to alarm
    global mBotGo
    mBotGo = 0
    isAlarm = 0
    while True:
        #if there is no alarm - nothing is happening
        while mBotGo: #while there is an alarm 'Blue LEDs-Move-Red LEDs-Move' cycle is running
            isAlarm = 1
            cyberpi.led.on('blue', 'all') 
            mbot2.straight(5, 50)
            cyberpi.led.on('red', 'all')
            mbot2.straight(5, 50)
        if isAlarm: #if alarm is stoped - turn off LEDs and move backward to start position
            cyberpi.led.on('black', 'all')
            mbot2.straight(-100, 50)
            isAlarm = 0
        
#MAIN CODE

sta_if = network.WLAN(network.STA_IF) #mode to connect to LAN using WIFI
sta_if.active(True)
sta_if.connect('SSID', 'PASS') #connect to WIFI
while not sta_if.isconnected(): #wait until connected
    cyberpi.console.println("NO CONNECTION")

cyberpi.console.println(str(sta_if.ifconfig())) #show connection details - IP, etc
time.sleep(1)

cyberpi.display.clear() #clear LCD of mBot2

client=MQTTClient(client_id='CLIENT', server='SERVER', port=9991, user='USER', password='PASS') #set MQTT broker
client.set_callback(sub_cb) #set listener
client.connect() #connect to MQTT broker

client.subscribe('USER/TOPIC') #subscribe to topic

secondThread = _thread.start_new_thread(thread2, ()) #start thread2
thread1() #run function as a MAIN