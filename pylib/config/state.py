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
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(db.TABLE_NAME)
        config = table.get_item(Key={"key": f"env-{env}"})["Item"]
        config.pop("key")
        log.info(f"Updating {env} config with:\n{json.dumps(config, indent=2)}")
        set_stateful(env=env, **config)


def get_stateful(name):
    return getattr(State(), name, None)


def set_stateful(**kwargs):
    for k, v in kwargs.items():
        setattr(State(), k, v)
