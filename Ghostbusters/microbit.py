#This code should be used in makecode.microbit.org Python editor with following extensions:
#Yahboom Tiny:bit extension for makecode.microbit.org - https://github.com/lzty634158/Tiny-bit
#esp8266 supporting MQTT extension for makecode.microbit.org - https://github.com/elecfreaks/pxt-esp8266iot

def on_mqtt_qos_list_qos0(message):
    global isGhost
    if message == "GHOST":
        basic.show_icon(IconNames.ANGRY)
        isGhost = 1
    elif message == "HUMAN":
        isGhost = 0
        basic.show_icon(IconNames.HAPPY)
        basic.pause(2000)
        basic.clear_screen()
ESP8266_IoT.mqtt_event("topic",
    ESP8266_IoT.QosList.QOS0,
    on_mqtt_qos_list_qos0)

isGhost = 0
ESP8266_IoT.break_mqtt()
basic.show_icon(IconNames.SURPRISED)
basic.pause(1000)
isGhost = 0
ESP8266_IoT.init_wifi(SerialPin.P1, SerialPin.P2, BaudRate.BAUD_RATE115200)
ESP8266_IoT.connect_wifi("ssid", "pass")
while ESP8266_IoT.wifi_state(False):
    basic.show_icon(IconNames.NO)
    basic.pause(1000)
basic.show_icon(IconNames.HEART)
basic.pause(1000)
ESP8266_IoT.set_mqtt(ESP8266_IoT.SchemeList.TCP,
    "client",
    "user",
    "pass",
    "")
ESP8266_IoT.connect_mqtt("server", 9991, False)
while not (ESP8266_IoT.is_mqtt_broker_connected()):
    basic.show_icon(IconNames.NO)
    basic.pause(1000)
basic.show_icon(IconNames.YES)
basic.pause(1000)
basic.clear_screen()

def on_forever():
    while isGhost:
        Tinybit.car_ctrl(Tinybit.CarState.CAR_SPINLEFT)
        Tinybit.RGB_Car_Big(Tinybit.enColor.WHITE)
        basic.pause(200)
        Tinybit.car_ctrl(Tinybit.CarState.CAR_SPINRIGHT)
        Tinybit.RGB_Car_Big(Tinybit.enColor.OFF)
        basic.pause(200)
    Tinybit.car_ctrl(Tinybit.CarState.CAR_STOP)
basic.forever(on_forever)
