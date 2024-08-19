FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY bot.py ./
COPY config.py ./
COPY utils/song.py ./utils/
COPY utils/queue_manager.py ./utils/
COPY requirements.txt ./
COPY .env ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "bot.py"]