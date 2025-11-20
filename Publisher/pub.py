import time
from datetime import datetime

import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion

from w1thermsensor import W1ThermSensor
import board
import adafruit_dht

# ---------- SENSOR SETUP ----------

# 1-Wire temperature sensor (e.g. DS18B20)
thermal = W1ThermSensor()

# DHT11 on GPIO22 (BCM) -> physical pin 15
humid = adafruit_dht.DHT11(board.D22)

# ---------- MQTT SETUP ----------

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

        # Read temperature from 1-Wire sensor (°C)
        temp = thermal.get_temperature()
        temp_str = f"{temp:.2f}"

        # Read humidity (and optional temp) from DHT11
        try:
            humidity = humid.humidity
            dht_temp = humid.temperature  # if you want to log it too

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
            # DHT11 can be flaky; ignore occasional bad reads
            print(f"DHT11 read error: {e}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Exited by user")

finally:
    client.disconnect()
    print("MQTT client disconnected")
