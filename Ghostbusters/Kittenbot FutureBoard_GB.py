#code for Kittenbot FutureBoard

#micropython and FutureBoard libs
from time import sleep
from future import *
from sugar import *
import mqttsimple
import _thread

#set of functions

def alarmLight(): #function to light LEDs as single B-R-B and R-B-R sequence
  neopix.setColor(0, (0, 0, 255))
  neopix.setColor(1, (255, 0, 0))
  neopix.setColor(2, (0, 0, 255))
  neopix.update()
  sleep(0.5)
  neopix.setColor(0, (255, 0, 0))
  neopix.setColor(1, (0, 0, 255))
  neopix.setColor(2, (255, 0, 0))
  neopix.update()
  sleep(0.5)

def gbTheme(): #function to play Ghostbusters theme.
# it is split into gbTheme1, gbTheme2, gbTheme3 and gbTheme to ease debugging
#there are many if isGhost checks inside the functions to interrupt the sound immediately if condition changed 	
  global isGhost
  for count in range(2):
    gbTheme1()
    if isGhost == 0:
      return
  gbTheme2()
  if isGhost == 0:
    return
  for count in range(2):
    gbTheme3()
    if isGhost == 0:
      return
    gbTheme1()
    if isGhost == 0:
      return
    note = [60, 60, 63, 64, 67, 70, 65]
    duration = [1/2, 1/2, 1/4, 1/4, 1/2, 1, 1/2]
    for z in range(7):
      buzzer.note(note[z], duration[z])
      if isGhost == 0:
        return
  buzzer.note(60,1/2)
  if isGhost == 0:
    return
  gbTheme4()
  if isGhost == 0:
    return

def gbTheme1(): #part of Ghostbusters theme
  global isGhost
  note = [60, 60, 63, 64, 67, 70, 65]
  duration = [1/2, 1/2, 1/4, 1/4, 1/2, 1, 1]
  for z in range(7):
    buzzer.note(note[z], duration[z])
    if isGhost == 0:
      return

def gbTheme2(): #part of Ghostbusters theme
  global isGhost
  note = [60, 72, 72, 76, 72, 74, 70, 65, 60, 60, 72, 72, 72, 72, 70, 72, 65, 60, 72, 72, 76, 72, 74, 70, 65, 60, 60, 72, 72, 72, 72, 70, 74, 72]
  duration = [1/2, 1/4, 1/4, 1/2, 1/2, 1/2, 1/2, 1, 1/2, 1/2, 1/4, 1/4, 1/4, 1/4, 1/2, 1/2, 1, 1/2, 1/4, 1/4, 1/2, 1/2, 1/2, 1/2, 1, 1/2, 1/2, 1/4, 1/4, 1/4, 1/4, 1/2, 1/2, 1/2]
  for z in range(34):
    buzzer.note(note[z], duration[z])
    if isGhost == 0:
      return

def gbTheme3(): #part of Ghostbusters theme
  global isGhost
  note = [72, 72, 75, 72, 75, 70, 65, 72, 70, 72, 72, 72, 70, 65]
  duration = [1/4, 1/4, 1/2, 1/2, 1, 1, 1/2, 1/4, 1/4, 1/2, 1/2, 1, 1, 1]
  for z in range(14):
    buzzer.note(note[z], duration[z])
    if isGhost == 0:
      return

def gbTheme4(): #part of Ghostbusters theme
  global isGhost
  for count in range(2):
    note = [75, 72, 75, 72, 75, 72, 75, 72, 75, 72, 70, 71, 72]
    duration = [1, 1/2, 1, 1/2, 1, 1/2, 1, 1/2, 1/2, 1/2, 1/4, 1/4, 1/2]
    for z in range(13):
      buzzer.note(note[z], duration[z])
      if isGhost == 0:
        return
  for count in range(2):
    note = [79, 75, 79, 75, 79, 75, 79, 75, 79, 75, 70, 71, 72]
    duration = [1, 1/2, 1, 1/2, 1, 1/2, 1, 1/2, 1/2, 1/2, 1/4, 1/4, 1/2]
    for z in range(13):
      buzzer.note(note[z], duration[z])
      if isGhost == 0:
        return

#MQTT broker listener, LCD display, LEDs and buzzer run in multithread

def thread1(): #thread to listen to MQTT broker for messages
#this one will be a MAIN thread
  global isGhost
  global message
  while True:
    mqtt.check_msg()
    sleep(1)
    message = str(mqtt.mqttRead("USER/TOPIC"))
  
def thread2(): #thread to check the message, set variable isGhost after condition is satisfied, change LCD screen
  global isGhost
  global constGHOST
  global constHUMAN
  global message
  message = ""
  while True:
    if isGhost == 0:
      if constGHOST in message:
        isGhost = 1
        screen.loadPng('gb.png',0,0) #show picture, uploaded to FutureBoard in advance
    if isGhost == 1:
      if constHUMAN in message:
        isGhost = 0
        screen.clear()        

def thread3(): #thread to run LEDs function in repeat loop until condition is satisfied, then LEDs off immediately
  global isGhost
  while True:
    while isGhost:
      alarmLight()
    neopix.setColorAll((0,0,0))   

def thread4(): #thread to play buzzer function in repeat loop until condition is satisfied, then buzzer turns off immediately
  global isGhost
  while True:
    while isGhost:
      gbTheme()
      
#MAIN CODE

neopix=NeoPixel("P7",3) #define LEDs

isGhost = 0
constGHOST = "GHOST" #define data to look for from MQTT message
constHUMAN = "HUMAN" #define data to look for ftom MQTT message

wifi.connect(str("SSID"), "PASS") #connect to local WiFi - SSID and PASS

while not wifi.sta.isconnected(): #wait until connected
  pass

mqtt = mqttsimple.MQTTClient("SERVER", "CLIENT",user=str("USER"), password=str("PASS"),port=9991) #MQTT broker address, user ID, password, MQTT port
mqtt.connect() #connect to MQTT

mqtt.subscribe("USER/TOPIC") #subscribe to MQTT topic

screen.clear() #clean screen, fill black

secondThread = _thread.start_new_thread(thread2, ()) #start thread2
thirdThread = _thread.start_new_thread(thread3, ()) #start thread3
fourthhread = _thread.start_new_thread(thread4, ()) #start thread4

thread1() #run function as a MAIN