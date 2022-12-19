FROM python:3.11-slim

RUN pip install paho-mqtt==1.6.1
RUN apt update
RUN apt install screen -y

WORKDIR /root
ADD core core/
ADD config config/