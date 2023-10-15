from abmqtt.wrapper.aurora_watch import AuroraWatch
import paho.mqtt.client as mqtt
import json


class Core:
    # Aurora watch API Client
    CLIENT = None

    # Broker details
    BROKER = None
    PORT = None
    USERNAME = None
    PASSWORD = None

    # MQTT topic to publish to
    TOPIC = None

    def __init__(
        self, broker: str, port: int, username: str, password: str, topic: str
    ) -> None:
        self.CLIENT = AuroraWatch()

        self.BROKER = broker
        self.PORT = port
        self.USERNAME = username
        self.PASSWORD = password
        self.TOPIC = topic

    def start(self) -> None:
        client = mqtt.Client()
        client.username_pw_set(username=self.USERNAME, password=self.PASSWORD)

        client.connect(self.BROKER, port=self.PORT, keepalive=60)

        data = self.CLIENT.get_status()

        client.publish(
            topic=self.TOPIC,
            payload=json.dumps(data),
            qos=1,
            retain=False,
        )

        print(f"Published reading:\n{json.dumps(data, indent=4)}")
