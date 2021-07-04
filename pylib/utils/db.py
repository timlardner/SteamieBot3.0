import argparse
import os

import boto3
import yaml

from config import db, state


def get_key(name):
    env = state.get_stateful("env")
    return f"{env}-{name}"


def populate_dynamodb_praw(table, **kwargs):
    table.put_item(
        Item={
            "key": get_key(db.PRAW_KEY),
            "client_id": kwargs.get("REDDIT_CLIENT_ID"),
            "client_secret": kwargs.get("REDDIT_CLIENT_SECRET"),
            "username": kwargs.get("REDDIT_USERNAME"),
            "password": kwargs.get("REDDIT_PASSWORD"),
            "user_agent": kwargs.get("REDDIT_USER_AGENT"),
        }
    )


def populate_dynamodb_google(table, **kwargs):
    table.put_item(
        Item={
            "key": get_key(db.GOOGLE_KEY),
            "client_id": kwargs.get("GOOGLE_TOKEN"),
            "api_key": kwargs.get("GOOGLE_API_KEY"),
        }
    )


def populate_dynamodb_darksky(table, **kwargs):
    table.put_item(
        Item={
            "key": get_key(db.DARKSKY_KEY),
            "api_key": kwargs.get("DARKSKY_API_KEY"),
        }
    )


def populate_dynamodb_listcouk(table, **kwargs):
    table.put_item(
        Item={
            "key": get_key(db.LISTCOUK_KEY),
            "api_key": kwargs.get("LIST_API_KEY"),
        }
    )


def populate_dynamodb_env(table, **kwargs):
    table.put_item(
        Item={
            "key": get_key(db.ENV_KEY),
            "dry_run": kwargs.get("DRY_RUN"),
            "set_sticky": kwargs.get("SET_STICKY"),
            "subreddit": kwargs.get("SUBREDDIT"),
            "flair_id": kwargs.get("FLAIR_ID"),
        }
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility for uploading SteamieBot configs")
    parser.add_argument(
        "--env",
        help="Which environment should I be looking to upload settings for?",
        required=True,
    )
    args = parser.parse_args()

    steamie_config_folder = os.getenv("STEAMIE_CONFIG_FOLDER", default="~/.config/steamiebot/")
    filename = os.path.join(steamie_config_folder, f"{args.env}.yaml")

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(db.TABLE_NAME)

    with open(os.path.expanduser(filename), "r") as f:
        data = yaml.safe_load(f)

    populate_dynamodb_praw(table, **data)
    populate_dynamodb_google(table, **data)
    populate_dynamodb_darksky(table, **data)
    populate_dynamodb_listcouk(table, **data)
    populate_dynamodb_env(table, **data)
