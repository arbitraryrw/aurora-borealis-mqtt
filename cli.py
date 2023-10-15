from abmqtt.core.core import Core
from abmqtt.util.util import Util
import argparse


def main() -> None:
    arguments = parse_arguments()

    try:
        c = Core(
            broker=Util.get_env_variable("MQTT_BROKER_URL"),
            port=int(Util.get_env_variable("MQTT_BROKER_PORT")),
            username=Util.get_env_variable("MQTT_BROKER_USERNAME"),
            password=Util.get_env_variable("MQTT_BROKER_PASSWORD"),
            topic=arguments.mqtt_topic,
        )
    except ValueError:
        missing_env_variables = []
        required_env_variables = [
            "MQTT_BROKER_URL",
            "MQTT_BROKER_PORT",
            "MQTT_BROKER_USERNAME",
            "MQTT_BROKER_PASSWORD",
        ]

        for env_var in required_env_variables:
            try:
                Util.get_env_variable(env_var)
            except ValueError:
                missing_env_variables.append(env_var)

        print(
            f"[!] Fatal error, missing environment variables: {missing_env_variables}"
        )
        exit(1)

    c.start()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Obtains electromagnetic readings and sends them over MQTT."
    )

    parser.add_argument(
        "--mqtt_topic",
        type=str,
        required=False,
        default="/homeassistant/electromagnetic",
        help="MQTT topic to publish readings to, by default this is '/homeassistant/electromagnetic'",
    )

    return parser.parse_args()


if __name__ == "__main__":
    print("--- Aurora Borealis MQTT---")

    main()
