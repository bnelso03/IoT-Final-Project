FROM python:3.11-slim
WORKDIR /CPU
COPY CPUSubscribe.py .
RUN pip install paho-mqtt prometheus-client
CMD ["python", "-u", "CPUSubscribe.py"]
