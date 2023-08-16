# syntax=docker/dockerfile:1

FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -U pywaggle[all]

COPY . .

ENTRYPOINT ["python", "dario_main.py"]
