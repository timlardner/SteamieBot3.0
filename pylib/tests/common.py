import base64
import os

import boto3
import yaml

from config import db
from utils.db import (populate_dynamodb_darksky, populate_dynamodb_google,
                      populate_dynamodb_listcouk, populate_dynamodb_praw)


def get_test_data():
    """All variables are stored in this encoded block"""
    encoded = os.getenv("TEST_DATA")
    if not encoded:
        return {}

    data = yaml.safe_load(base64.b64decode(encoded.encode()).decode())
    return data


def setup_praw():
    table = _create_table()
    populate_dynamodb_praw(table, **get_test_data())
    return table


def setup_google():
    table = _create_table()
    populate_dynamodb_google(table, **get_test_data())


def setup_darksky():
    table = _create_table()
    populate_dynamodb_darksky(table, **get_test_data())


def setup_listcouk():
    table = _create_table()
    populate_dynamodb_listcouk(table, **get_test_data())


def _create_table():
    """Mock the caller with `moto` before calling this function"""
    dynamodb = boto3.resource("dynamodb")
    try:
        table = dynamodb.create_table(
            TableName=db.TABLE_NAME,
            KeySchema=[{"AttributeName": "key", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "key", "AttributeType": "S"}],
        )
        table.meta.client.get_waiter("table_exists").wait(TableName=db.TABLE_NAME)
        assert table.table_status == "ACTIVE"
        return table
    except Exception:
        return dynamodb.Table(db.TABLE_NAME)
