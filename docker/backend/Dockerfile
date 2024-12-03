FROM python:3.10-slim

WORKDIR /opt/star_burger

COPY requirements.txt .

RUN apt update && apt-get install libpq-dev -y && pip install --no-cache-dir -r requirements.txt

COPY . .
