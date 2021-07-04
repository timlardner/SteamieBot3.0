import json
import logging

import boto3

from config import db
from utils.common import Singleton

log = logging.getLogger(__name__)


class State(metaclass=Singleton):
    def __init__(self):
        self.dry_run = True  # Always set dry run. It can be overridden later

    @classmethod
    def from_environment(cls, env):
        from utils.db import get_key

        set_stateful(env=env)
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(db.TABLE_NAME)
        config = table.get_item(Key={"key": get_key("env")})["Item"]
        config.pop("key")
        log.info(f"Updating {env} config with:\n{json.dumps(config, indent=2)}")
        set_stateful(**config)


def get_stateful(name, default=None):
    return getattr(State(), name, default)


def set_stateful(**kwargs):
    for k, v in kwargs.items():
        setattr(State(), k, v)
