FROM python:3.12-slim

WORKDIR /app

# Copy ONLY what we need:
COPY publisher.py .

# If the repo has other modules you want to import (like sensor helpers),
# you can copy the whole repo instead:
# COPY . .

RUN pip install --no-cache-dir paho-mqtt

CMD ["python", "publisher.py"]
