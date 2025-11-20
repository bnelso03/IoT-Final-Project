FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

COPY publisher.py .

RUN pip install --no-cache-dir \
    paho-mqtt \
    w1thermsensor \
    adafruit-circuitpython-dht \
    adafruit-blinka

CMD ["python", "publisher.py"]
