import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from datetime import datetime
import time
import random
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("10.183.240.41", 1883, keepalive=60)

try:
	while True:
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		temp = sensor.get_temperature()
		temp_str = f"{temp: .2f}°C"
		message = f"sensorID : {sensor.id} : Temperature :{temp_str} : Time : {timestamp}"
		client.publish("temperature/data",  message)
		print(f"{message}")
		time.sleep(5)
except KeyboardInterrupt:
	print("Exited")
	client.disconnect()
