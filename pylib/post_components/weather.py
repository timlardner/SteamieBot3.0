import boto3
import requests

from config import db
from post_components.base import PostInterface
from utils.db import get_key


class Weather(PostInterface):
    def _get_api_key(self):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(db.TABLE_NAME)
        response = table.get_item(Key={"key": get_key(db.DARKSKY_KEY)})
        praw_secrets = response["Item"]
        api_key = praw_secrets.pop("api_key")
        if not api_key:
            raise RuntimeError("Darksky API key must be set")
        return api_key

    @classmethod
    def format_header(cls, header):
        return header

    @classmethod
    def can_update(cls) -> bool:
        return True

    def get_header(self) -> str:
        return "**Weather** [(Powered by Dark Sky)](https://darksky.net/poweredby/)"

    def get_body(self) -> str:
        data = requests.get(f"https://api.darksky.net/forecast/{self._get_api_key()}/55.8580,-4.2590?units=si").json()

        min_temp = int(data["daily"]["data"][0]["temperatureMin"])
        max_temp = int(data["daily"]["data"][0]["temperatureMax"])

        weather_string = f"{data['hourly']['summary']}\n\n"

        if min_temp == max_temp:
            weather_string += f"Around {max_temp} degrees."
        else:
            weather_string += f"Around {min_temp} to {max_temp} degrees.\n\n"

        if "alerts" in data:
            weather_string += (
                f"[**Weather Warning**]({data['alerts'][-1]['uri']})\n\n{data['alerts'][-1]['description']}"
            )
        return weather_string
