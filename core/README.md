# Core 

The core module that is a python wrapper around intereacting with MQTT system, heartbeats and tests.

## Building on top of Core

Inherit the core class and add methods

```python
class CoreAddOn(BaseMQTTPubSub):
    def __init__(self):
        super().__init__()
```