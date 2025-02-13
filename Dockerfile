FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY /mnt/f/js-bambisleep-chat-MK-VIII/workers/python/tts.py ./src/tts.py

CMD ["python", "./src/tts-server.py"]