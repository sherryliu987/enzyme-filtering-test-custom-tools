FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas openpyxl

COPY . /app
RUN mkdir -p inputs out
