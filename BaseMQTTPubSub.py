import paho.mqtt.client as mqtt
import argparse
from time import sleep

class BaseMQTTPubSub:
    def __init__(self):
        self.args = self.parse_cli() # parse 
        
        self.client = mqtt.Client() # connect to MQTT 
        self.client.connect(self.args.mqtt_host_ip_address, 8883, 60)
        
        self.client.message_callback_add(self.args.mqtt_subscribe_topic, self._subscriber_callback) # specify the callback function for subscriber
        self.client.subscribe(self.args.mqtt_subscribe_topic) # adding a subscriber
        
        self.client.loop_start()
        

    def parse_cli(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--mqtt-host-ip-address", type=str)
        parser.add_argument("--mqtt-subscribe-topic", type=str)
        parser.add_argument("--mqtt-publish-topic", type=str)
        return parser.parse_args()

    def _subscriber_callback(self, client, userdata, msg):
        print("message received " ,str(msg.payload.decode("utf-8")))
        print("message topic=",msg.topic)
        print("message qos=",msg.qos)
        print("message retain flag=",msg.retain)
        
    
    # def add_subscribe_topics(self, topic_list: list, callback_method_list: list, qos_list=[2]: list) -> bool:
    #     result_set = set()
    #     assert len(topic_list) == len(callback_method_list) == len(qos_list)
    #     for idx in range(len(topic_list)):
    #         self.client.message_callback_add(topic_list[idx], callback_method_list[idx])
    #         (result, mid) = self.client.subscribe(topic_list[idx], qos_list[idx])
    #         result_set.add(result)
    #     return result_set == set(mqtt.MQTT_ERR_SUCCESS)
        
    # def remove_subscribe_topic(self, topic_name: str, callback_method: Callable)  -> None:
    #     self.client.message_callback_remove(topic_name)
        
    
    def spin(self):
        run = True
        while run:
            publisher_payload = "test"
            topic_name = self.args.mqtt_publish_topic
            self.client.publish(topic_name, publisher_payload) # adding a publisher
            sleep(1)
  
if __name__ == "__main__":
    pub_sub = BaseMQTTPubSub()
    pub_sub.spin()