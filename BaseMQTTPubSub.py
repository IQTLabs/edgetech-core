from time import sleep
from typing import Callable
import paho.mqtt.client as mqtt


class BaseMQTTPubSub:
    CONFIG_PATH = "./config/client.conf"
    HEARTBEAT_TOPIC = "/heartbeat"
    HEARTBEAT_FREQUENCY = 10  # seconds

    def __init__(
        self,
        config_path: str = CONFIG_PATH,
        heartbeat_topic: str = HEARTBEAT_TOPIC,
        heartbeat_frequency: int = HEARTBEAT_FREQUENCY,
    ) -> None:
        self.config_filepath = config_path
        self.client_connection_parameters = self._parse_config()
        self.heartbeat_topic = heartbeat_topic
        self.heartbeat_frequency = heartbeat_frequency

        self.connection_flag = None
        self.graceful_disconnect_flag = None

        self.client = mqtt.Client()

    def _parse_config(self) -> dict:
        with open(self.config_filepath, "r", encoding="utf-8") as file_pointer:
            parameters = {
                line.split("=")[0]: line.split("=")[-1]
                for line in file_pointer.read().splitlines()
            }
            return parameters

    def connect_client(self) -> None:
        def _on_connect(
            _client: mqtt.Client, _userdata: dict, _flags: dict, response_flag: int
        ):
            """
            0: Connection successful
            1: Connection refused - incorrect protocol version
            2: Connection refused - invalid client identifier
            3: Connection refused - server unavailable
            4: Connection refused - bad username or pasßsword
            5: Connection refused - not authorised 6-255: Currently unused.
            """
            if response_flag == mqtt.MQTT_ERR_SUCCESS:
                self.connection_flag = True
            else:
                self.connection_flag = False

        # connect to MQTT
        self.client.on_connect = _on_connect
        self.client.connect(
            self.client_connection_parameters["IP"],
            int(self.client_connection_parameters["PORT"]),
            int(self.client_connection_parameters["TIMEOUT"]),
        )
        self.client.loop_start()  # start callback thread

    def graceful_stop(self) -> None:
        def _on_disconnect(_client: mqtt.Client, _userdata: dict, response_flag: int):
            if response_flag == mqtt.MQTT_ERR_SUCCESS:
                self.graceful_disconnect_flag = True
            else:
                self.graceful_disconnect_flag = False

        self.client.disconnect()
        self.client.on_disconnect = _on_disconnect
        self.client.loop_stop()

    def setup_ungraceful_disconnect_publish(
        self,
        ungraceful_disconnect_topic: str,
        ungraceful_disconnect_payload: str,
        qos: int = 0,
        retain: bool = False,
    ) -> None:
        self.client.will_set(
            ungraceful_disconnect_topic, ungraceful_disconnect_payload, qos, retain
        )

    def add_subscribe_topic(
        self, topic_name: str, callback_method: Callable, qos: int = 2
    ) -> bool:
        self.client.message_callback_add(topic_name, callback_method)
        (result, _mid) = self.client.subscribe(topic_name, qos)
        return result == mqtt.MQTT_ERR_SUCCESS  # returns True if successful

    def add_subscribe_topics(
        self, topic_list: list, callback_method_list: list, qos_list: list
    ) -> bool:
        result_list = []
        assert (
            len(topic_list) == len(callback_method_list) == len(qos_list)
        )  # remove in prod
        for idx, _val in enumerate(topic_list):
            self.client.message_callback_add(topic_list[idx], callback_method_list[idx])
            (result, _mid) = self.client.subscribe(topic_list[idx], qos_list[idx])
            result_list.append(result)
        return result_list == [mqtt.MQTT_ERR_SUCCESS] * len(
            topic_list
        )  # returns True if all successful

    def remove_subscribe_topic(self, topic_name: str) -> None:
        self.client.message_callback_remove(topic_name)

    def publish_to_topic(
        self, topic_name, publish_payload, qos: int = 2, retain: bool = False
    ) -> bool:
        (result, _mid) = self.client.publish(topic_name, publish_payload, qos, retain)
        return result == mqtt.MQTT_ERR_SUCCESS  # returns True if successful

    def publish_hearbeat(self, payload):
        # Need to put this in your main loop with a tick of self.heartbeat_frequency
        # b/c MQTT is single threaded
        success = self.publish_to_topic(self.heartbeat_topic, payload)
        return success
