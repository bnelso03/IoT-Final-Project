import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from datetime import datetime
import time
import random
import adafruit_dht
import board

sensor = adafruit_dht.DHT11(board.D22)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("10.183.240.41", 1883, keepalive=60)

try:
        while True:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                humidity, temperature = sensor.humidity, sensor.temperature
                message = f"sensorID : {sensor._pin} : Humidity :{sensor.humidity} : Time : {timestamp}"
                print(f"{message}")
                client.publish("humidity/data", message)
                time.sleep(5)
except KeyboardInterrupt:
        print("Exited")
        client.disconnect()
