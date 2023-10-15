# Aurora Borealis MQTT

The purpose of this project is to improve my chances of seeing the [Aurora Borealis](https://en.wikipedia.org/wiki/Aurora)/Northern Lights in the UK. This a Python3 Command Line Interface (CLI) tool that obtains electromagnetic readings and publishes them over [MQTT](https://mqtt.org/). The goal of this is to ingest the data in home automation like [Home Assistant](https://www.home-assistant.io/), and build automation around this data. For example, if the electromagnetic reading is greater than 80/100 (high chance that the Aurora Borealis is visible to the naked eye) I want to be notified.

Note, this tool is powered through the folks over at [Aurora Watch](https://aurorawatch.lancs.ac.uk/), big shoutout, thank you.

## Usage

```python3
➜ virtualenv env
➜ source env/bin/activate
➜ python3 -m pip install -r requirements.txt
➜ python3 cli.py --mqtt_topic <topic name>
```

Note, this project depends on environment variables to avoid persisting credentials to disk. These environment variables include:

1. `MQTT_BROKER_URL`
1. `MQTT_BROKER_PORT`
1. `MQTT_BROKER_USERNAME`
1. `MQTT_BROKER_PASSWORD`

The message that is published over MQTT is a string JSON object that contains two key/value pairs. The first key is a `value` that contains the electromagnetic reading. The second is the `last_updated` key that contains the time the reading was updated.

```json
{
    "last_updated": <%Y-%m-%d %H:%M Timestamp>,
    "value": <float reading out of 100>,
}
```

Note, **the reading is updated hourly** because that's when Aurora Watch updates. To avoid having to awkwardly integrate sleep logic I run this script hourly using [Cron](https://en.wikipedia.org/wiki/Cron). I offset the job by 3/4 minutes past the hour to give Aurora Watch some time to publish the latest reading.

## Requirements

See `requirements.txt` but also remember to setup a MQTT broker(such as [mosquitto](https://mosquitto.org/)).
