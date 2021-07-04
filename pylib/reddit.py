import configparser
import datetime as dt

import boto3
import praw

from config import db, state
from utils.common import Singleton
from utils.db import get_key


class Reddit(praw.Reddit, metaclass=Singleton):
    def __init__(self, *args, **kwargs):
        self._patch_praw()
        super().__init__(*args, **kwargs)
        assert self.user.me()

    @staticmethod
    def _patch_praw():
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(db.TABLE_NAME)
        response = table.get_item(Key={"key": get_key(db.PRAW_KEY)})
        praw_secrets = response["Item"]
        praw_secrets.pop("key")

        praw_config = configparser.ConfigParser()
        praw_config["DEFAULT"].update(praw_secrets)

        with open("praw.ini", "w") as f:
            praw_config.write(f)


def get_latest_submission():
    for submission in Reddit().user.me().submissions.new():
        if (dt.datetime.utcnow() - dt.datetime.fromtimestamp(int(submission.created_utc))) > dt.timedelta(days=1):
            return  # Only check for a day's worth of posts
        if submission.subreddit.display_name == state.get_stateful("subreddit"):
            return submission