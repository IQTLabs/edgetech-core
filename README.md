# EdgeTech-Core

EdgeTech-Core is a unified platform bringing functionality to edge-based devices with minimal development effort. At its core is an MQTT broker sercive with auxillary

Core Services:
- Core Library (python library for interacting with Core)
- MQTT Broker
- Heartbeat Monitor
Auxillary Services:
- File Save


## Running EdgeTech Core Services
`cd` into directory with `docker-compose.yaml`

`docker-compose up -d`

## Building Core Image
The image is automatically built via docker compose if not present. Alternatively, to only build the image use:
`docker build . -f Dockerfile -t iqtlabs/edgetech-core:latest`

## Pushing Docker Image to Registry

If needed, you can push the image to container registry with:
```bash
docker image push iqtlabs-edgetech-core:latest
```

Alternatively docker CI/CD pipeline will publish images with tag:

## Using as a Library

For building a container with the library, wither start with the edgetech-core base image in your `Dockerfile`:

```bash
FROM iqtlabs-edgetech-core:latest
```

or include the core folder in your base image of choice.
```bash
ADD core core/
```

and import the library from your python file.
```bash
from core import *
client=BaseMQTTPubSub.BaseMQTTPubSub()
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
will run the callback_function when a message is recieved from the /TOPIC

Publish to an MQTT Topic:
```python
core.publish(str:"/TOPIC", str:payload)
will publish a text payload to /TOPIC


## Building on top of Core

Inherit the core class and add methods

```python
from core import *

class CoreAddOn(BaseMQTTPubSub.BaseMQTTPubSub):
	def __init__(self):
		super().__init__()
```
