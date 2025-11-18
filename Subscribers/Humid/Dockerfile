FROM python:3.11-slim
WORKDIR /Humid
COPY HumidSubscribe.py .
RUN pip install paho-mqtt prometheus-client
CMD ["python", "-u", "HumidSubscribe.py"]
