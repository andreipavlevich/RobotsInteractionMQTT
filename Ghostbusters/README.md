This folder contains python files for robots to interact in Ghostbusters scenario.

Robots:
  1. Kittenbot KOI
  2. Kittenbot FutureBoard
  3. Makeblock mBot2

Scenario description:
  Alarm is started when the ghost is detected. Ghostbusters are coming for the ghost if alarm is started. When the ghost is captured and ghostbuster approve that the alarm is turning off.

Scenario details:
  1. Kittenbot KOI. Recognizes object in front of camera in real time. If there is nothting in front of it, KOI classifes the view as 'NONE'. If there is an object which was classified as a ghost, KOI sends MQTT message containing 'GHOST' string. If there is an object which was classified as a ghostbuster, KOI sends MQTT message containin 'HUMAN' string.
  2. Kittenbot FutureBoard. It is listening to MQTT broker. If there is a message containing 'GHOST' string, FutureBoard will start an alarm - flashing lights and playing Ghostbusters theme. Alarm stops immediately if FutureBoard receives the message containing 'HUMAN' string.
  3. Makeblock mBot2. It is listening to MQTT broker. If there is a message containing 'GHOST' string, mBot2 will start to flash lights and move to capture the ghost. If there is a message containing 'HUMAN' string, mBot2 will turn off the lights and move backward.

Files:
