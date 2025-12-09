import paho.mqtt.client as mqtt
from datetime import datetime
from prometheus_client import Gauge, start_http_server
import random, time

def on_message(client, any, msg):
	message = msg.payload.decode()
	#will need to change below to match our publisher's formatting
	parts = [p.strip() for p in message.split(':')]
	temp_value = parts[parts.index("Temperature") + 1]
	sensor_id= parts[parts.index("sensorID")+1]
	temp_gague.labels(sensor_id=sensor_id).set(temp_value)
	print(f"Received: {message}")
	
print("Starting Temperature Subscriber")
temp_gague= Gauge('temperature', 'Temperature in Celcius', ['sensor_id'])
start_http_server(8001)
sensor_id="temp_sensor"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1884, keepalive = 60)
client.subscribe("temperature/data")
client.loop_start()
try:
	while True:
		pass
except KeyboardInterrupt:
	print("Exited")
	client.loop_stop()
	client.disconnect()
