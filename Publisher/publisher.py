import time
import json
import random
import paho.mqtt.client as mqtt

# ====== CONFIG ======
BROKER_IP = "10.95.102.161"  # <-- put the broker VM's bridged IP here
BROKER_PORT = 1884

TOPIC_TEMP = "sensors/temperature"
TOPIC_HUM  = "sensors/humidity"


def generate_sensor_payload():
    return {
        "sensor_id": "lab-sensor-1",
        "temp_c": round(random.uniform(20.0, 30.0), 2),
        "humidity_pct": round(random.uniform(30.0, 60.0), 1),
        "ts": time.time()
    }

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("[PUBLISHER] Connected to broker")
    else:
        print(f"[PUBLISHER] Connect failed, reason_code={reason_code}")

def main():
    client = mqtt.Client(
        client_id="virtual-sensor-pub",
        protocol=mqtt.MQTTv5,
        transport="tcp",
        userdata=None,
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    )

    client.on_connect = on_connect

    # connect to Mosquitto broker
    client.connect(BROKER_IP, BROKER_PORT, keepalive=60)

    # start network loop in the background
    client.loop_start()

    try:
        while True:
            reading = generate_sensor_payload()


            temp_msg = json.dumps({
                "sensor_id": reading["sensor_id"],
                "temp_c": reading["temp_c"],
                "ts": reading["ts"]
            })
            hum_msg = json.dumps({
                "sensor_id": reading["sensor_id"],
                "humidity_pct": reading["humidity_pct"],
                "ts": reading["ts"]
            })

            r1 = client.publish(
                topic=TOPIC_TEMP,
                payload=temp_msg,
                qos=0,
                retain=False,
                properties=None
            )
            r2 = client.publish(
                topic=TOPIC_HUM,
                payload=hum_msg,
                qos=0,
                retain=False,
                properties=None
            )

            print(f"[PUBLISH] {TOPIC_TEMP} -> {temp_msg} (rc={r1.rc})")
            print(f"[PUBLISH] {TOPIC_HUM}  -> {hum_msg} (rc={r2.rc})")
            print("-----")

            time.sleep(2)

    except KeyboardInterrupt:
        print("[PUBLISHER] Stopping virtual sensor...")

    finally:
        client.loop_stop()
        client.disconnect()
        print("[PUBLISHER] Disconnected from broker")

if __name__ == "__main__":
    main()
