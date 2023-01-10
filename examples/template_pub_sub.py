import os
from time import sleep, time
import json
from typing import Any, Dict
import schedule
from datetime import datetime

from base_mqtt_pub_sub import BaseMQTTPubSub

# inherit functionality from BaseMQTTPubSub parent this way
class TemplatePubSub(BaseMQTTPubSub):
    def __init__(
        self: Any,
        env_variable: Any,
        debug: bool = False,
        **kwargs: Any,
    ):
        # Pass enviornment variables as parameters (include **kwargs) in super().__init__()
        super().__init__(**kwargs)
        self.env_variable = env_variable
        # include debug version
        self.debug = debug

        # Connect client in constructor 
        self.connect_client()
        sleep(1)
        self.publish_registration("Template Module Registration")
        
    def _example_callback(
        self: Any, _client: mqtt.Client, _userdata: Dict[Any, Any], msg: Any
    ) -> None:
        # Decode message:
        # Always publishing a JSON string with {timestamp: ____, data: ____,} 
        # TODO: more on this to come w/ a JSON header after talking to Rob
        payload = json.loads(str(msg.payload.decode("utf-8")))
        
        # Do something when a message is recieved 
        pass
 
    def main(self: Any) -> None:
        # main funciton wraps functionality and always includes a while True
        # (make sure to include a sleep)
        
        # include schedule heartbeat in every main()
        schedule.every(10).seconds.do(
            self.publish_heartbeat, payload="Template Module Heartbeat"
        )
        
        # If subscribing to a topic: 
        self.add_subscribe_topic(
            topic_name: str, callback_method: Callable[[mqtt.Client, Dict[Any, Any], Any], None], qos: int = 2
        )
        
        example_data = {
            "timestamp": str(int(datetime.utcnow().timestamp())),
            "data": "Example data payload"
        }
        
        # example publish data every 10 minutes
        schedule.every(10).minutes.do(
            self.publish_to_topic, topic_name="Template Module Heartbeat", publish_payload=json.dumps(example_data)
        )
        
        # or just publish once 
        self.publish_to_topic(self.example_publish_topic, json.dumps(example_data))

        while True:
            try:
                # run heartbeat and anything else scheduled if clock is up
                schedule.run_pending()
                # include a sleep so loop does not run at CPU time
                sleep(0.001)
                
            except Exception as e:
                if self.debug:
                    print(e)


if __name__ == "__main__":
    # instantiate an instance of the class
    # any variables in BaseMQTTPubSub can be overriden using **kwargs 
    # and enviornment variables should be in the docker compose (in a .env file)
    template = TemplatePubSub(mqtt_ip=os.environ.get("MQTT_IP"))
    # call the main function
    template.main()


######################## TODO: ########################
# Have an example of default values that are stored 
# somewhere (an envinornment wiki typing)
#######################################################