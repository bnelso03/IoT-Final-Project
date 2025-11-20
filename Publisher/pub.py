import time
from datetime import datetime

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

from w1thermsensor import W1ThermSensor
import board
import adafruit_dht


thermal = W1ThermSensor()

humid = adafruit_dht.DHT11(board.D22)

BROKER_IP = "10.95.102.161"
BROKER_PORT = 1884
TOPIC = "temperature/humidity/data"

client = mqtt.Client(
    client_id="pi-sensor-pub",
    protocol=mqtt.MQTTv5,
    transport="tcp",
    callback_api_version=CallbackAPIVersion.VERSION2,
)

client.connect(BROKER_IP, BROKER_PORT, keepalive=60)


try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        temp = thermal.get_temperature()
        temp_str = f"{temp:.2f}"

   
        try:
            humidity = humid.humidity
            dht_temp = humid.temperature 

            if humidity is None:
                print("Failed to read from DHT11 sensor")
            else:
                message = (
                    f"Humidity: {humidity:.1f}% "
                    f"Temperature: {temp_str}°C "
                    f"Time: {timestamp}"
                )

                client.publish(TOPIC, message)
                print(message)

        except RuntimeError as e:
            print(f"DHT11 read error: {e}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Exited by user")

finally:
    client.disconnect()
    print("MQTT client disconnected")
