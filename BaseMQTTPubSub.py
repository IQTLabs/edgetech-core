import paho.mqtt.client as mqtt
import argparse
from time import sleep
from typing import Callable

class BaseMQTTPubSub:
    CONFIG_PATH = './config/client.conf'
    HEARTBEAT_TOPIC = '/heartbeat'
    HEARTBEAT_FREQUENCY = 10 # seconds
    
    def __init__(self, config_path=CONFIG_PATH: str, heartbeat_topic=HEARTBEAT_TOPIC: str, heartbeat_frequency=HEARTBEAT_FREQUENCY: int) -> None:
        self.config_filepath = config_path        
        self.client_connection_parameters = self._parse_config()
        
        self.connection_flag = None
        self.graceful_disconnect_flag = None

    def _parse_config(self) -> dict:
        with open(self.config_filepath, "r") as f:
            parameters = {line.split('=')[0]:line.split('=')[-1] for line in f.read().splitlines()}
            return parameters
        
    def connect_client(self) -> None:
        self.client = mqtt.Client() # connect to MQTT 
        self.client.connect(self.client_connection_parameters['IP'], 
                            int(self.client_connection_parameters['PORT']), 
                            int(self.client_connection_parameters['TIMEOUT']))
        self.client.on_connect = self._on_connect
        
    def _on_connect(self, client, userdata, flags, rc):
        '''
        0: Connection successful 
        1: Connection refused - incorrect protocol version 
        2: Connection refused - invalid client identifier 
        3: Connection refused - server unavailable 
        4: Connection refused - bad username or password 
        5: Connection refused - not authorised 6-255: Currently unused.
        '''
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self.connection_flag = True
        else:
            self.connection_flag = False
    
    def graceful_stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
        self.client.on_disconnect = self._on_disconnect

    def _on_disconnect(self, client, userdata, rc):
        if rc == mqtt.MQTT_ERR_SUCCESS:
            self.graceful_disconnect_flag = True
        else:
            self.graceful_disconnect_flag = False
    
    def setup_ungraceful_disconnect_publish(self, ungraceful_disconnect_topic: str, ungraceful_disconnect_payload: str, qos=0: int, retain=False, bool) -> None:
        self.will_set(ungraceful_disconnect_topic, ungraceful_disconnect_payload, qos, retain)

    def add_subscribe_topic(self, topic_name: str, callback_method: Callable, qos=2: int) -> bool:
        self.client.message_callback_add(topic_name, callback_method)
        (result, mid) = self.client.subscribe(topic_name, qos)
        return result == mqtt.MQTT_ERR_SUCCESS # returns True if successful
    
    def add_subscribe_topics(self, topic_list: list, callback_method_list: list, qos_list=[2]: list) -> bool:
        result_set = set()
        assert len(topic_list) == len(callback_method_list) == len(qos_list) # remove in prod
        for idx in range(len(topic_list)):
            self.client.message_callback_add(topic_list[idx], callback_method_list[idx])
            (result, mid) = self.client.subscribe(topic_list[idx], qos_list[idx])
            result_set.add(result)
        return result_set == set(mqtt.MQTT_ERR_SUCCESS) # returns True if all successful
        
    def remove_subscribe_topic(self, topic_name: str)  -> bool:
        (result, mid) = self.client.message_callback_remove(topic_name) #TODO: check this 
        return result == mqtt.MQTT_ERR_SUCCESS # returns True if successful
    
    def publish_to_topic(self, topic_name, publish_payload, qos=2: int, retain=False: bool) -> bool:
        (result, mid) = self.client.publish(topic_name, publish_payload, qos, retain)
        return result == mqtt.MQTT_ERR_SUCCESS # returns True if successful

    def start_client_loop(self) -> None:
        self.client.loop_start()
        
    def publish_hearbeat(self, payload):
        while True:
            time.sleep(self.heartbeat_frequency)
            success = self.publish_to_topic(self.heartbeat_topic, payload)
            assert success == True