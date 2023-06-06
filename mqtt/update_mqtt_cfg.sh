#! /bin/sh

# by design the path for lets encrypt certs is inaccessible
# copy certs to a location accessible by mosquitto and
# adjust config accordingly
cp -r /etc/letsencrypt/live/server.mqtt.local/*.pem /etc/mosquitto/certs/
chown -R mosquitto:mosquitto /etc/mosquitto/certs/

kill -SIGHUP $(cat /etc/mosquitto/pid)