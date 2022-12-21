# IQT Labs: EdgeTech-Core

EdgeTech-Core is a unified platform bringing functionality to edge-based devices with minimal development effort. The core is a dynamic message/event-based infrastructure that is enabled via MQTT. This is very much a working repo and is under active development.

Core Services:

- MQTT Broker (this module is dependent on the [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto) docker contianer running and uses [mqtt-paho](https://www.eclipse.org/paho/index.php?page=clients/python/index.php) to interact with this broker)
- Heartbeat Monitor (keep the TCP/IP connection with the MQTT broker alive)
- Core Library (python library for interacting with MQTT e.g. adding publishers/subscribers, connecting, disconnecting, etc.)

Auxiliary Services:

- TBA

## Running EdgeTech Core

`cd` into directory with `docker-compose.yaml` and then run: `docker-compose build && docker-compose up`.

## Running EdgeTech Core Tests

`cd` into directory with `docker-compose.yaml`, uncomment the `# CMD pytest BaseMQTTPubSubTest.py` line, comment out the `CMD python -u BaseMQTTPubSub.py` line, and then run: `docker-compose build && docker-compose up`.

<!-- 
## Building Core Image

The image is automatically built via docker-compose if not present. Alternatively, to only build the image use:

`docker build . -f BaseDockerfile -t iqtlabs-edgetech-core:latest`

## Using as a Library

For building a container with the library, either start with the edgetech-core base image in your `Dockerfile`:

```bash
FROM iqtlabs-edgetech-core:latest
```

or include the core folder in your base image of choice.

```bash
ADD core .
```

and import the library from your python file.

```bash
import iqtlabs-edgetech-core as core
```

### Usage

The edgetech-core object handles message passing and syncronization with the core MQTT system.

```pyhton
core = core.core(MQTT_IP, PORT)
```

will start a connection to the MQTT broker and initialize all needed functions


Subscribe to an MQTT topic:

```python
core.subscribe(str:"/TOPIC". callback_function)
```

will run the callback_function when a message is received from the /TOPIC

Publish to an MQTT Topic:

```python
core.publish(str:"/TOPIC", str:payload)
```

will publish a text payload to /TOPIC -->

## Building on top of Core

Inherit the core class and add methods

```python
class CoreAddOn(BaseMQTTPubSub):
    def __init__(self):
        super().__init__()
```
