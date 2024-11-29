FROM --platform=linux/arm64 python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install git -y
RUN apt-get install -y ffmpeg
COPY requirements.txt requirements.txt
COPY main.py main.py
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
