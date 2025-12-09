FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
	    && rm -rf /var/lib/apt/lists/*

COPY Publisher.py .

RUN pip install --no-cache-dir \
    paho-mqtt \
    w1thermsensor \
    adafruit-circuitpython-dht \
    adafruit-blinka \
    RPi-GPIO \
    gpiozero

CMD ["python", "Publisher.py"]
