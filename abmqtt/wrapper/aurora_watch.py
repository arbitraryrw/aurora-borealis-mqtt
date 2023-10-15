from datetime import datetime, timedelta, timezone

import requests
import os

import xml.etree.ElementTree as ET


class AuroraWatch:
    BASE_URL = "http://aurorawatch-api.lancs.ac.uk"

    # Ref: https://aurorawatch.lancs.ac.uk/api-info/
    HEADERS = {
        "User-Agent": "aurora-borealis-mqtt",
    }

    STATUS = {}

    def __init__(self) -> None:
        self._populate_status_definitions()

    def _populate_status_definitions(self) -> None:
        status_path = "0.2/status-descriptions.xml"

        response = requests.get(
            os.path.join(self.BASE_URL, status_path), headers=self.HEADERS
        )

        response.raise_for_status()

        # Parse the XML response
        root = ET.fromstring(response.text)

        for status in root.findall("status"):
            self.STATUS[status.get("id")] = {
                "description": status.find("description").text,
                "meaning": status.find("meaning").text,
            }

    def get_status(self) -> None:
        # ref: http://aurorawatch-api.lancs.ac.uk/0.2/status/

        status_path = "0.2/status/alerting-site-activity.xml"

        response = requests.get(
            os.path.join(self.BASE_URL, status_path), headers=self.HEADERS
        )

        response.raise_for_status()

        # Parse the XML response
        root = ET.fromstring(response.text)

        last_updated = datetime.strptime(
            root.find("updated/datetime").text, "%Y-%m-%dT%H:%M:%S%z"
        )

        current_time = datetime.now(timezone.utc)

        if current_time - last_updated > timedelta(minutes=15):
            raise ValueError("Stale status Data")

        # for activity in root.findall("activity"):
        #     print(activity.get("status_id"))

        #     date_time = activity.find("datetime").text
        #     value = float(activity.find("value").text)

        #     print(date_time, value)

        most_recent_activity = root.findall("activity")[-1]

        datetime_object = datetime.strptime(
            most_recent_activity.find("datetime").text, "%Y-%m-%dT%H:%M:%S%z"
        )

        formatted_time = datetime_object.strftime("%Y-%m-%d %H:%M")

        return {
            # "status": most_recent_activity.get("status_id"),
            "last_updated": formatted_time,
            "value": float(most_recent_activity.find("value").text),
        }
