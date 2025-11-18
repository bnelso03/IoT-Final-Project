FROM python:3.11-slim
WORKDIR /Temp
COPY TempSubscribe.py .
RUN pip install paho-mqtt prometheus-client
CMD ["python", "-u", "TempSubscribe.py"]
