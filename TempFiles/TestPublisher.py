import paho.mqtt.client as mqtt
from datetime import datetime
import random
import time

# --- MQTT broker info ---
BROKER = "test.mosquitto.org"   # public broker
PORT = 1883

TOPIC_HUMIDITY = "humidity/data"
TOPIC_TEMPERATURE = "temperature/data"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, keepalive=60)

try:
    while True:
        sensor_id = 1
        humidity = random.randint(20, 90)
        temperature = round(random.uniform(18.0, 32.0), 1)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create messages in same colon-separated format
        humidity_msg = f"sensorID : {sensor_id} : Humidity : {humidity} : Time : {timestamp}"
        temperature_msg = f"sensorID : {sensor_id} : Temperature : {temperature} : Time : {timestamp}"

        # Publish both
        client.publish(TOPIC_HUMIDITY, humidity_msg)
        client.publish(TOPIC_TEMPERATURE, temperature_msg)

        print(f"Published → {humidity_msg}")
        print(f"Published → {temperature_msg}")
        print("-" * 60)

        time.sleep(5)  # wait 5 seconds before next set

except KeyboardInterrupt:
    print("Stopped publisher.")
    client.disconnect()
