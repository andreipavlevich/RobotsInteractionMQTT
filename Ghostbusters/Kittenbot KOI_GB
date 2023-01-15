#code for Kittenbot KOI

#micropython and KOI libs
import time
from koi import *

#setting up camera
#flipping camera is more robust than flipping LCD IMHO
sensor.set_vflip(1) #camera vertical flip
sensor.set_hmirror(1) #camera horizontal mirror
sensor.set_jb_quality(30) #set camera quality to 30 to inmpove performance

#MAIN CODE
#classifier initialization
cla.reset()
time.sleep(1)

#variables
train = 0
click = 0
counter = 0
aPressed = 0
bPressed = 0
bothPressed = 0

drawString(5,5,"dblA->train", 5000) #informing that if you'd like to train KOI just double press A button within 5seconds

#doubleclick handler
start = time.ticks_ms() #starting timer
while time.ticks_diff(time.ticks_ms(), start) < 5000: #5 second countdown
  img = sensor.snapshot() #camera -> LCD
  lcd.display(img) #camera -> LCD
  if btnAValue():
    click += 1 #counting button-A clicks within 5 seconds
  time.sleep(0.1) #delay for robustness and stability

if click > 1: #if doubleclick or more - train mode
  train = 1 #train mode flag
  drawString(5,5,"TRAIN MODE", 500) #LCD notification
  
if train == 0: #if train mode is not selected -> proceed with recognize/classifier mode
  cla.load("lego.json") #loading train data

#MAIN LOOP
while True:
  
  if train == 1: #if train mode
    #button handler - A, B or A+B pressed. This is necessary to avoid single A or B pressing when A+B is pressed
    while btnAValue():
      aPressed = 1
      bPressed = 0
      bothPressed = 0
      if btnBValue():
        bothPressed = 1 #first pressed A then B = A+B
        aPressed = 0
        time.sleep(0.1)      
    while btnBValue():
      aPressed = 0 
      bPressed = 1
      bothPressed = 0
      if btnAValue():
        bothPressed = 1 #first pressed B then A = A+B
        bPressed = 0
        time.sleep(0.1)

    time.sleep(0.1) #delay for stability
    #actions for various button pressed. Also there is a counter variable to write a train file when 41 pictures captured - maximal allowed for KOI
    if bothPressed:
      cla.addImage('NONE') #if A+B then there is no GHOST and no GHOSTBUSTER, mark it as 'NONE'
      counter += 1
      bothPressed = 0
    elif aPressed:
      cla.addImage('HUMAN') #if A then there is a GHOSTBUSTER, mark it as 'HUMAN'
      counter += 1
      aPressed = 0
    elif bPressed:
      cla.addImage('GHOST') #if B then there is a GHOST, mark it as 'GHOST'
      counter += 1
      bPressed = 0
 
    if counter == 41: #when counter reaches 41 -> stop training and write train file. SD CARD IS NECESSARY!
        cla.save('lego.json')
  
  if train == 0: #if recognize/classify mode
    #perorming in real-time
    #!!! there is no need to initiate WiFi connection and connection to MQTT broker each time KOI starts!
    #!!! it should be done once! than you can connect to KOI via IP using web-browser to setup both network and MQTT
    tag=cla.getImageTag() #recognize image from camera
    if tag=='GHOST': #if recognized GHOST -> sends to MQTT broker and specific topic a message "GHOST"
      wifi.mqttpub("USER/TOPIC", "GHOST")
    elif tag=='HUMAN': #if recognized GHOSTBUTER -> sends to MQTT broker and specific topic a message "HUMAN"
      wifi.mqttpub("USER/TOPIC", "HUMAN")
    #class "NONE" is not used in any action
  
  #camera->LCD handler
  img = sensor.snapshot()
  lcd.display(img)
  time.sleep(0.1)