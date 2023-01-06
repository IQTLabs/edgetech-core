"""_summary_
    NOTE: these tests are written assuming the MQTT server is running
"""
from time import sleep
import paho.mqtt.client as mqtt
import pytest
from typing import Callable, Dict, Any
from BaseMQTTPubSub import BaseMQTTPubSub


@pytest.fixture()
def basepubsub() -> BaseMQTTPubSub:
    """Pytest fixture that returns an instance of the BaseMQTTPubSub class for testing.

    Returns:
        BaseMQTTPubSub: an instance of the class to be tested.
    """
    return BaseMQTTPubSub()


@pytest.fixture()
def ungraceful_disconnect_topic() -> str:
    """Pytest fixture topic name for the ungraceful last will and testament broadcast.

    Returns:
        str: topic name for the last will and testament.
    """
    return "/base/ungracefultest"


@pytest.fixture()
def ungraceful_disconnect_payload() -> str:
    """Pytest fixture payload for the ungraceful last will and testament broadcast.

    Returns:
        str: the content to be published to the specified topic for the last will and testament.
    """
    return "The process ungracefully disconnected"


@pytest.fixture()
def fixture_topic_one() -> str:
    """Pytest fixture topic name for subscriber testing.

    Returns:
        str: topic to subscribe/publish to for subscriber/publisher function testing.
    """
    return "/base/topictestone"


@pytest.fixture()
def fixture_callback_one() -> Callable[[mqtt.Client, Dict[Any, Any], Any], None]:
    """Pytest fixture that defines a nested funciton that will serve as the callback function
    for the topic one test.

    Returns:
        Callable: the callback function defined in the fixture.
    """

    def _callback_one(
        _client: mqtt.Client, _userdata: Dict[Any, Any], msg: Any
    ) -> None:
        """Standard callback fuction that prints the recieved message and topic name it is
        subscribed to.

        Args:
            _client (mqtt.Client): the MQTT client that was instatntiated in the constructor.
            _userdata (Dict[Any,Any]): data passed to the callback through the MQTT paho Client
            class contructor or set later through user_data_set().
            msg (Any): the recieved message over the subscribed channel that includes
            the topic name and payload after decoding.
        """
        print("Message Topic:", msg.topic)
        print("Message Payload:", str(msg.payload.decode("utf-8")))

    return _callback_one


@pytest.fixture()
def fixture_payload_one() -> str:
    """Pytest fixture that defines the payload to be published to the fixture_topic_one topic.

    Returns:
        str: string payload for publishing testing.
    """
    return "Payload One"


@pytest.fixture
def fixture_topic_two() -> str:
    """Pytest fixture topic name for multi-subscriber testing.

    Returns:
        str: topic to subscribe to for subscriber function testing.
    """
    return "/base/topictesttwo"


@pytest.fixture()
def fixture_callback_two() -> Callable[[mqtt.Client, Dict[Any, Any], Any], None]:
    """Pytest fixture that defines a nested funciton that will serve as the callback function
    for multiple subscriber test.

    Returns:
        Callable: the callback function defined in the fixture.
    """

    def _callback_two(
        _client: mqtt.Client, _userdata: Dict[Any, Any], msg: Any
    ) -> None:
        """Standard callback fuction that prints the recieved message and topic name it is
        subscribed to.

        Args:
            _client (mqtt.Client): the MQTT client that was instatntiated in the constructor.
            _userdata (Dict[Any,Any]): data passed to the callback through the MQTT paho Client
            class contructor or set later through user_data_set().
            msg (Any): the recieved message over the subscribed channel that includes
            the topic name and payload after decoding.
        """
        print("Message Topic:", msg.topic)
        print("Message Payload:", str(msg.payload.decode("utf-8")))

    return _callback_two


@pytest.fixture()
def fixture_heartbeat_payload() -> str:
    """Pytest fixture that defines the payload published to the heartbeat topic name defined
    in the BaseMQTTPubSub constructor.

    Returns:
        str: example heartbeat publish message for the base module that will be verified
        as recieved.
    """
    return "Base Alive"


@pytest.fixture()
def fixture_heartbeat_callback() -> Callable[[mqtt.Client, Dict[Any, Any], Any], None]:
    """pytest fixture that returns a callback for the heartbeat topic to verify that
    the published payload has been recieved correcrtly and shows and example usage of
    the userdata component of MQTT callbacks.

    Returns:
        Callable: the callback function defined in the fixture.
    """

    def _heartbeat_callback(
        client: mqtt.Client, _userdata: Dict[Any, Any], msg: Any
    ) -> None:
        """Heartbeat callback function that prints the payload and topic name as well
        as stores the decoded payload in the userdata attribute of the client.

        Args:
            client (mqtt.Client): the MQTT client that was instatntiated in the constructor.
            _userdata (Dict[Any,Any]): data passed to the callback through the MQTT paho Client
            class contructor or set later through user_data_set().
            msg (Any): the recieved message over the subscribed channel that includes
            the topic name and payload after decoding.
        """
        print("Message Topic:", msg.topic)
        print("Message Payload:", str(msg.payload.decode("utf-8")))
        # sets the userdata as the decoded payload
        client.user_data_set(str(msg.payload.decode("utf-8")))

    return _heartbeat_callback


def test_connect_client(basepubsub: BaseMQTTPubSub) -> bool:
    """Using the pytest module, this function verifies that the connection function
    effectively connects to the MQTT broker running on the device from the persepective
    of the broker.

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
    """
    assert basepubsub.connection_flag is None
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True  # successful connection


def test_graceful_stop(basepubsub: BaseMQTTPubSub) -> bool:
    """Using the pytest module, this function verifies that the graceful disconnect
    function effectively disconnects from the MQTT broker from its perspective.

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
    """
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    assert basepubsub.graceful_disconnect_flag is None
    basepubsub.graceful_stop()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.graceful_disconnect_flag is True  # successful disconnect


def test_setup_ungraceful_disconnect_publish(
    basepubsub: BaseMQTTPubSub,
    ungraceful_disconnect_topic: str,
    ungraceful_disconnect_payload: str,
) -> None:
    """Using the pytest module, this function is meant to verify that the last will and
    testament publish occurs if the connected client disconnects unexpectedly
    (without calling disconnect).

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
        ungraceful_disconnect_topic (str): the topic name to publish the last will
        and testament payload to.
        ungraceful_disconnect_payload (str): the data to publish given an ungraceful disconnect.
    """
    # TODO: instantiate on another thread and kill only the thread that
    # the client instantiated in this function is running on and capture
    # the published topic from MQTT
    pass


def test_add_subscribe_topic(
    basepubsub: BaseMQTTPubSub,
    fixture_topic_one: str,
    fixture_callback_one: Callable[[mqtt.Client, Dict[Any, Any], Any], None],
) -> bool:
    """Using the pytest module, this funciton is meant to verify the successful addition
    of a subscriber to the specified topic from the perspective of the MQTT broker.

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
        fixture_topic_one (str): the topic to subscribe to.
        fixture_callback_one (Callable): the callback function trigged by a publish to the topic.
    """
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.add_subscribe_topic(fixture_topic_one, fixture_callback_one)
    assert result is True


def test_add_subscribe_topics(
    basepubsub: BaseMQTTPubSub,
    fixture_topic_one: str,
    fixture_callback_one: Callable[[mqtt.Client, Dict[Any, Any], Any], None],
    fixture_topic_two: str,
    fixture_callback_two: Callable[[mqtt.Client, Dict[Any, Any], Any], None],
) -> bool:
    """Using the pytest module, this funciton is meant to verify the successful addition
    of multiple subscribers to the specified topics from the perspective of the MQTT broker

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
        fixture_topic_one (str): the first topic to subscribe to.
        fixture_callback_one (Callable): the callback function trigged by a publish to
        the first topic.
        fixture_topic_two (str): the second topic to subscribe to.
        fixture_callback_two (Callable): the callback function trigged by a publish to
        the second topic.
    """
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.add_subscribe_topics(
        [fixture_topic_one, fixture_topic_two],
        [fixture_callback_one, fixture_callback_two],
        [2, 2],
    )
    assert result is True


def test_remove_subscribe_topic(
    basepubsub: BaseMQTTPubSub,
    fixture_topic_one: str,
    fixture_callback_one: Callable[[mqtt.Client, Dict[Any, Any], Any], None],
) -> None:
    """Using the pytest module, this funciton calls the remove subscriber funciton,
    but will require additional development specified in the TODO to fully verify its accuracy.

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
        fixture_topic_one (str): _description_
        fixture_callback_one (Callable): _description_
    """
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    add_result = basepubsub.add_subscribe_topic(fixture_topic_one, fixture_callback_one)
    assert add_result is True
    sleep(1)  # default MQTT connection wait
    basepubsub.remove_subscribe_topic(fixture_topic_one)
    # TODO: message_callback_remove() does not return anything, so in order to test this
    # function you will need to add an additional subscriber to the same topic, then
    # publish a payload to the topic after removing the first subscriber using the function,
    # then assign the decoded payloads to the user data in the callbacks and compare the two
    # to make sure that the removed callback did not recievd the published message


def test_publish_to_topic(
    basepubsub: BaseMQTTPubSub, fixture_topic_one: str, fixture_payload_one: str
) -> bool:
    """Using the pytest module, this function tests successful publishing from the
    perspective of the MQTT broker.

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
        fixture_topic_one (str): the topic to publish to.
        fixture_payload_one (str): the payload to publish to the topic.
    """
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.publish_to_topic(fixture_topic_one, fixture_payload_one)
    assert result is True


def test_publish_heartbeat(
    basepubsub: BaseMQTTPubSub,
    fixture_heartbeat_payload: str,
    fixture_heartbeat_callback: Callable[[mqtt.Client, Dict[Any, Any], Any], None],
) -> bool:
    """Using the pytest module, his funciton tests multiple functionalities defiend in the class and can be considered
    a verification of the heartbeat function, the publish function, and the subscriber function
    as it publishes a payload to the heartbeat topic specified in the constructor of the class
    and then captures that payload with a callback subscribed to that topic and maintains that
    the decoded payload is the same as the one published.

    Args:
        basepubsub (BaseMQTTPubSub): a dynamic instantiation of the BaseMQTTPubSub
        class this testing suite is evaluating.
        fixture_heartbeat_payload (str): the payload to publish to the heartbeat topic.
        fixture_heartbeat_callback (Callable): the callback function that is subscribed to
        the heartbeat topic for verification of publish.
    """
    basepubsub.connect_client()
    sleep(1)  # default MQTT connection wait
    assert basepubsub.connection_flag is True
    result = basepubsub.add_subscribe_topic(
        basepubsub.heartbeat_topic, fixture_heartbeat_callback
    )
    basepubsub.client.user_data_set("")
    assert result is True
    success = basepubsub.publish_heartbeat(fixture_heartbeat_payload)
    assert success is True
    sleep(1)  # default MQTT connection wait
    assert basepubsub.client._userdata == fixture_heartbeat_payload
    # To avoid access to a protected attribute of the mqtt.Client class, I've made a PR here to MQTT
    # paho requesting the addition of a getter: https://github.com/eclipse/paho.mqtt.python/pull/695
