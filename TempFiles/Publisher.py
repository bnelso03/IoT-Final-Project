import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from datetime import datetime
import time
import random
from w1thermsensor import W1ThermSensor
import adafruit_dht
import board


humidSensor = adafruit_dht.DHT11(board.D22)
tempSensor = W1ThermSensor()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1884, keepalive=60)

try:
	while True:
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		temp = tempSensor.get_temperature()
		humidity=humidSensor.humidity
		temp_str = f"{temp: .2f}°C"
		humidMessage=f"sensorID : {humidSensor._pin} : Humidity : {humidity} : Time : {timestamp}"
		tempMessage = f"sensorID : {tempSensor.id} : Temperature :{temp_str} : Time : {timestamp}"
		client.publish("temperature/data",  tempMessage)
		client.publish("humidity/data", humidMessage)
		print(f"{tempMessage}")
		print(f"{humidMessage}")
		time.sleep(5)
except KeyboardInterrupt:
	print("Exited")
	client.disconnect()
