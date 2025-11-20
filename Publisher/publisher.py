import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from datetime import datetime
import time
import random
from w1thermsensor import W1ThermSensor

thermal = W1ThermSensor()
humid = adafruit_dht.DHT11(board.D22)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("10.95.102.161", 1884, keepalive=60)

try:
	while True:
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		temp = thermal.get_temperature()
		temp_str = f"{temp: .2f}"
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        humidity, temperature = humid.humidity, thermal.temperature
		message = f"Humidity :{humid.humidity} : Temperature :{temp_str} : Time : {timestamp}"
		client.publish("temperature/humidity/data",  message)
		print(f"{message}")
		time.sleep(5)
except KeyboardInterrupt:
	print("Exited")
	client.disconnect()
