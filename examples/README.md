## Building on "Core" Template

### BaseMQTTPubSub Child Class

The core module that is a python wrapper around intereacting with MQTT system, heartbeats and tests. The `template_pub_sub.py` file includes examples of reccomended usage of the `BaseMQTTPubSub` module and how to build a child class using it. 

An outline of the basic functionality can be found below.

Inheriting `BaseMQTTPubSub`:
```python
from base_mqtt_pub_sub import BaseMQTTPubSub

class TemplatePubSub(BaseMQTTPubSub):
    def __init__(
        self: Any,
        ...
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
```
The use of `**kwargs` allows you to override any of the class parameters set in the `BaseMQTTPubSub` constructor. 

In the constructor of the child class, it is reccomended that you connect to the MQTT client and publish a message to the `/registration` topic upon successful connection.
```python
self.connect_client()
sleep(1)
self.publish_registration("Template Module Registration")
```

Every child class should include a `main()` function which includes a publishing to the `/heartbeat` channel to keep the connection alive and any subscriptions to other topics in the system. It should also include a `while True` loop to keep the main thread alive and flush all scheduled function calls.
```python
  def main(self: Any) -> None:
        schedule.every(10).seconds.do(
            self.publish_heartbeat, payload="Template Module Heartbeat"
        )

        self.add_subscribe_topic(self.example_topic, self._example_callback)

        ...

        while True:
            try:
                schedule.run_pending()
                sleep(0.001)

            except Exception as e:
                if self.debug:
                    print(e)
```

To call the child class see that the enviornment variables are passed via `docker compose` and passed to the constructor. The `main()` function is then called.

```python
    template = TemplatePubSub(
       ...
        mqtt_ip=os.environ.get("MQTT_IP"),
    )
    template.main()
```

### Docker

Examples of a `Dockerfile` and `docker-compose.yaml` can also be found in this repo. Adding whatever enviornment variables that your class needs should go under the `enviornment:` flag in the `docker-compose.yaml` as an array and paths/names will need to be adjusted as well. The `Dockerfile` should only require script name/path changes as well. Any dependencies should be added to the `requirements.txt` file.

### Topic Names

Reccomended topic names should follow the format specified below.

```python
f"{DEVICE}/{HOST_NAME}/{DATA_TYPE}/{CONTAINER_NAME}/{TYPE_LITERAL}"
```

Example:
```python
f"/AISonobuoy/{HOST_NAME}/AIS/edgetech-daisy/bytestring
```

### TODO:
 -  `.env` file with environment variables to be passed via `docker compose` that incldues default values
 - how to write tests for a child class of the core module