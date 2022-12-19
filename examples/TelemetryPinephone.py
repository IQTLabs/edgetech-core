from BaseMQTTPubSub import BaseMQTTPubSub
import paho.mqtt.client as mqtt
import argparse
from time import sleep

class TelemetryPinephone(BaseMQTTPubSub):
    def __init__(self):
        with open("/sys/bus/iio/devices/iio\:device2/in_magn_z_raw", "r") as f:
            val = f.readlines()
            print(val)


        
if __name__ == "__main__":
    telemetry = TelemetryPinephone()
    