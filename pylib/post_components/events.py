import boto3
import datetime as dt
import random
import requests

from config import db
from utils.db import get_key
from post_components.base import PostInterface
from utils.common import local_time


class EventInfo(PostInterface):
    def __init__(self):
        self.base_url = "https://api.list.co.uk/v1"

    def _truncate(self, string, maxchars=100):
        string = string.split("\n", 1)[0]
        string = string.replace("*", " ").replace("_", " ")  # Remove markdown stuff
        if len(string) > maxchars:
            return f"{string[:(maxchars-3)]}..."
        else:
            return string

    def _format_event(self, name, url, location, description):
        return f"[{name}]({url}) ({location})\n\n{description}"

    def _get_api_key(self):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(db.TABLE_NAME)
        response = table.get_item(Key={"key": get_key(db.LISTCOUK_KEY)})
        praw_secrets = response["Item"]
        api_key = praw_secrets.pop("api_key")
        if not api_key:
            raise RuntimeError("List.co.uk API key must be set")
        return api_key

    def get_header(self) -> str:
        return "What's On Today"

    def _send_list_request(self, endpoint):
        header = {"Authorization": f"Bearer {self._get_api_key()}"}
        return requests.get(f"{self.base_url}/{endpoint}", headers=header)

    def get_body(self) -> str:
        today_str = local_time().strftime("%Y-%m-%d")
        tomorrow_str = (local_time() + dt.timedelta(days=1)).strftime("%Y-%m-%d")

        res = self._send_list_request(
            f"events?near=55.8621,-4.2465/5&min_date={today_str}&max_date={tomorrow_str}"
        ).json()
        events = []
        for event in res:
            title = event["name"]
            locations = ", ".join(schedule["place"]["name"] for schedule in event["schedules"])
            description = self._truncate(random.choice(event["descriptions"])["description"])
            try:
                url = random.choice(random.choice(random.choice(event["schedules"])["performances"])["links"])["url"]
            except IndexError:
                url = None
            events.append((title, url, locations, description))

        return "\n\n".join(self._format_event(*evt) for evt in events)

    @classmethod
    def can_update(cls) -> bool:
        return True
