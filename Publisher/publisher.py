import paho.mqtt.client as mqtt
from paho.mqtt.client import CallbackAPIVersion
from datetime import datetime
import time
import random
from w1thermsensor import W1ThermSensor
import adafruit_dht
import board
from gpiozero import CPUTemperature

humidSensor = adafruit_dht.DHT11(board.D22)
tempSensor = W1ThermSensor()
cpuSensor= CPUTemperature()

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost", 1884, keepalive=60)

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        while True:
            try:
                temp = tempSensor.get_temperature()
                break  # success → exit retry loop
            except Exception as e:
                print(f"Temp sensor not ready: {e}")
                time.sleep(0.5)


        try:
            humidity = humidSensor.humidity
        except RuntimeError as e:
            print(f"DHT read error: {e}")
            time.sleep(2)
            continue
        except Exception as e:
            humidSensor.exit()
            raise e

        temp_str = f"{temp: .2f}"
        humidMessage = (
            f"sensorID : GPIO{humidSensor._pin} : Humidity : {humidity} : Time : {timestamp}"
        )
        tempMessage = (
            f"sensorID : {tempSensor.id} : Temperature : {temp_str} : Time : {timestamp}"
        )
        
        cpuMessage= (
            f"sensorID: 1 : Temperature : {cpuSensor.temperature:.2f} : Time : {timestamp}"
        )

        client.publish("temperature/data", tempMessage)
        client.publish("cputemp/data", cpuMessage)
        client.publish("humidity/data", humidMessage)

        print(tempMessage)
        print(humidMessage)

        time.sleep(5)

except KeyboardInterrupt:
    print("Exited")
    client.disconnect()
