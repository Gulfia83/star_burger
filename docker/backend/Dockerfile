FROM python:3.10-slim

WORKDIR /star_burger

COPY requirements.txt .

RUN apt update && apt-get install -y build-essential libpq-dev python3-dev  && pip install --no-cache-dir -r requirements.txt

COPY . .
