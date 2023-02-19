# Core MQTT Broker

This is an MQTT Broker that runs locally, which is a version of the [Eclipse Mosquitto](https://hub.docker.com/_/eclipse-mosquitto) broker.

A config file is added to enable support for sending MQTT messages over WebSockets. This allows the Javascript MQTT client in the WebApp to connect directly to this MQTT Broker and receive messages.