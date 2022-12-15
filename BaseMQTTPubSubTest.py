import paho.mqtt.client as mqtt
import pytest
from time import sleep
from BaseMQTTPubSub import BaseMQTTPubSub

# NOTE: these tests are written assuming the MQTT client is running


@pytest.fixture
def basepubsub():
    return BaseMQTTPubSub()


@pytest.fixture
def config_parse_result():
    return {"IP": "127.0.0.1", "PORT": "8883", "TIMEOUT": "60"}


@pytest.fixture
def ungraceful_disconnect_topic():
    return "/base/ungracefultest"


@pytest.fixture
def ungraceful_disconnect_payload():
    return "The process ungracefully disconnected"


@pytest.fixture
def fixture_topic_one():
    return "/base/topictestone"


@pytest.fixture
def fixture_callback_one_variable():
    callback_one_variable = ""
    return callback_one_variable


@pytest.fixture
def fixture_callback_one():
    def _callback_one(_client: mqtt.Client, _userdata: dict, msg: str) -> str:
        print("Message Topic:", msg.topic)
        print("Message Payload:", str(msg.payload.decode("utf-8")))

    return _callback_one


@pytest.fixture
def fixture_payload_one():
    return "Payload One"


@pytest.fixture
def fixture_topic_two():
    return "/base/topictesttwo"


@pytest.fixture
def fixture_callback_two():
    def _callback_two(_client: mqtt.Client, _userdata: dict, msg: str) -> str:
        print("Message Topic:", msg.topic)
        print("Message Payload:", str(msg.payload.decode("utf-8")))

    return _callback_two


@pytest.fixture
def fixture_heartbeat_payload():
    return "Base Alive"


@pytest.fixture
def fixture_heartbeat_callback_variable():
    heatbeat_callback_variable = None
    return heatbeat_callback_variable


@pytest.fixture
def fixture_heartbeat_callback():
    def _heartbeat_callback(client: mqtt.Client, _userdata: dict, msg: str) -> str:
        print("Message Topic:", msg.topic)
        print("Message Payload:", str(msg.payload.decode("utf-8")))
        client.user_data_set(str(msg.payload.decode("utf-8")))

    return _heartbeat_callback


def test_pase_config(basepubsub, config_parse_result):
    assert basepubsub.client_connection_parameters == config_parse_result


def test_connect_client(basepubsub):
    assert basepubsub.connection_flag is None
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True


def test_graceful_stop(basepubsub):
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    assert basepubsub.graceful_disconnect_flag is None
    basepubsub.graceful_stop()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.graceful_disconnect_flag is True


def test_setup_ungraceful_disconnect_publish(
    basepubsub, ungraceful_disconnect_topic, ungraceful_disconnect_payload
):
    # TODO: instantiate on another thread and kill only the thread that
    # the client instantiated in this function is running on and capture
    # the published topic from MQTT
    pass


def test_add_subscribe_topic(basepubsub, fixture_topic_one, fixture_callback_one):
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.add_subscribe_topic(fixture_topic_one, fixture_callback_one)
    assert result is True


def test_add_subscribe_topics(
    basepubsub,
    fixture_topic_one,
    fixture_callback_one,
    fixture_topic_two,
    fixture_callback_two,
):
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.add_subscribe_topics(
        [fixture_topic_one, fixture_topic_two],
        [fixture_callback_one, fixture_callback_two],
        [2, 2],
    )
    assert result is True


def test_remove_subscribe_topic(basepubsub, fixture_topic_one, fixture_callback_one):
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    add_result = basepubsub.add_subscribe_topic(fixture_topic_one, fixture_callback_one)
    assert add_result is True
    sleep(1)  # default MQTT connection wait
    basepubsub.remove_subscribe_topic(fixture_topic_one)
    # TODO: message_callback_remove() does not return anything, so what
    # to assert as test success. Code:
    # https://github.com/eclipse/paho.mqtt.python/blob/9782ab81fe7ee3a05e74c7f3e1d03d5611ea4be4/src/paho/mqtt/client.py#L2327


def test_publish_to_topic(basepubsub, fixture_topic_one, fixture_payload_one):
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.publish_to_topic(fixture_topic_one, fixture_payload_one)
    assert result is True


def test_publish_heartbeat(
    basepubsub,
    fixture_heartbeat_payload,
    fixture_heartbeat_callback,
):
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.add_subscribe_topic(
        basepubsub.heartbeat_topic, fixture_heartbeat_callback
    )
    basepubsub.client.user_data_set("")
    assert result is True
    success = basepubsub.publish_hearbeat(fixture_heartbeat_payload)
    assert success is True
    sleep(1)  # default MQTT connection wait
    assert basepubsub.client._userdata == fixture_heartbeat_payload
