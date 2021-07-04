import pickle
import sys

import boto3

from config import db
from post_components.events import EventInfo
from post_components.footer import Footer
from post_components.history import History
from post_components.market import MarketInfo
from post_components.travel import TravelInfo
from post_components.tunes import TuneInfo
from post_components.weather import Weather
from utils.common import local_time
from utils.db import get_key

MODULE_LIST = [Weather, TravelInfo, EventInfo, History, MarketInfo, TuneInfo, Footer]


class PostBuilder:
    def __init__(self, is_update=False):
        dynamodb = boto3.resource("dynamodb")
        self.table = dynamodb.Table(db.TABLE_NAME)
        self.is_update = is_update

    @staticmethod
    def _build_title():
        format_key = "#" if sys.platform == "win32" else "-"
        return local_time().strftime(f"The Steamie - %A %{format_key}d %B %Y")

    def _write_body(self, body):
        self.table.put_item(
            Item={
                "key": get_key(db.DATA_KEY),
                "data": pickle.dumps(body),
            }
        )

    def _read_body(self):
        response = self.table.get_item(Key={"key": get_key(db.DATA_KEY)})
        if response and (data := response.get("Item")):
            return pickle.loads(data["data"].value)
        else:
            return {}

    def _build_body(self):
        posts = self._read_body()
        if self.is_update and posts:
            modules = [module for module in MODULE_LIST if module.can_update()]
        else:
            posts = {}
            modules = MODULE_LIST

        # We could do the below more concisely, but this ensures dictionary order if posts is pre-populated
        for module in modules:
            posts[module.__name__] = module().get_info()

        self._write_body(posts)
        return posts

    def build_post(self):
        return self._build_title(), "\n\n".join(self._build_body().values())
