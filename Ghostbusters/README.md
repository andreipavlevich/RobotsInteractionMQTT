This folder contains python files for robots to interact in Ghostbusters scenario.

Robots:
  1. Kittenbot KOI
  2. Kittenbot FutureBoard
  3. Makeblock mBot2
  4. Yahboom Tiny:bit powered with micro:bit and esp8266 (esp-01)

Scenario description:
Alarm is started when the ghost is detected and robot starts to panic. Ghostbusters are coming for the ghost if alarm is started. When the ghost is captured and ghostbuster approves that - the alarm is turning off and robot stops panic.
VIDEO: https://youtu.be/NCv5_SvhqPY

Scenario details:
  1. Kittenbot KOI. Recognizes object in front of camera in real time. If there is nothting in front of it, KOI classifes the view as 'NONE'. If there is an object which was classified as a ghost, KOI sends MQTT message containing 'GHOST' string. If there is an object which was classified as a ghostbuster, KOI sends MQTT message containin 'HUMAN' string.
  2. Kittenbot FutureBoard. It is listening to MQTT broker. If there is a message containing 'GHOST' string, FutureBoard will start an alarm - flashing lights and playing Ghostbusters theme. Alarm stops immediately if FutureBoard receives the message containing 'HUMAN' string.
  3. Makeblock mBot2. It is listening to MQTT broker. If there is a message containing 'GHOST' string, mBot2 will start to flash lights and move to capture the ghost. If there is a message containing 'HUMAN' string, mBot2 will turn off the lights and move backward.
  4. Yahboom Tiny:bit. It is listening to MQTT broker. If there is a message containing 'GHOST' string, Tiny:bit will start to panic - short turns to left and to right with flashing headlights and showing ghost image on micro:bit led display. If there is a message containing 'HUMAN' string, Tiny:bit will stop any movement, turn off headlights, show happy face on micro:bit led display for few seconds and off then.

Files:
1. Kittenbot KOI_GB.py -> main script for Kittenbot KOI to recognize ghosts or ghostbusters captured on camera in realtime and to send call-to-action data to MQTT. It allows KOI to train on ghosts/ghostbusters images and save the data if doubleclicked A button at the start. WiFi and MQTT broker data should be set in advance and one time only - KOI stores this info when turned off.
2. Kittenbot FutureBoard_GB.py -> main script for Kittenbot FutureBoard to start an alarm (show Ghostbusters logo, blink LEDs and play Ghostbusters theme) or to stop an alarm (black LCD, LEDs off, buzzer off) if call-to-action data received from MQTT.
3. Makeblock mBot2_GB.py -> main script for Makeblock mBot2 to move with alarm leds to capture a ghost when call-to-action from MQTT is received and move back with lights off when the ghostbusters take situation under control (another call-to-action from MQTT).
4. microbit.py -> code that can be used in block editor like makecode.microbit.org in Python mode. To use that code to connect to MQTT broker and listen to topic, to rotate wheels and flash the headlights - tiny:bit and esp8266 extensions should be used. The code operates esp8266 (wifi connection -> mqtt connection -> mqtt topic listener) by micro:bit UART at P01 and P02 using AT commands.
