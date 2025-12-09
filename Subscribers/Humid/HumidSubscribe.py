import paho.mqtt.client as mqtt
from datetime import datetime
from prometheus_client import Gauge, start_http_server
import random, time

def on_message(client, any, msg):
	message = msg.payload.decode()
	#will probably change below to fit our publisher formatting
	parts = [p.strip() for p in message.split(':')]
	humidity_value = parts[parts.index("Humidity") + 1]
	sensor_id= parts[parts.index("sensorID")+1]
	humidity_gague.labels(sensor_id=sensor_id).set(humidity_value)
	print(f"Received: {message}")
	
print("Starting Humidity Subscriber")
humidity_gague= Gauge('humidity', 'Humidity in percent', ['sensor_id'])
start_http_server(8002)
sensor_id="humidity_sensor"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("localhost", 1884, keepalive = 60)
client.subscribe("humidity/data")
client.loop_start()
try:
	while True:
		pass
except KeyboardInterrupt:
	print("Exited")
	client.loop_stop()
	client.disconnect()
