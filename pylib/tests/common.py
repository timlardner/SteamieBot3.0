import boto3

from config import db
from utils import (
    populate_dynamodb_google,
    populate_dynamodb_praw,
    populate_dynamodb_darksky,
    populate_dynamodb_listcouk,
)

TABLE_CREATED = False


def setup_praw():
    table = _create_table()
    populate_dynamodb_praw(table)
    return table


def setup_google():
    table = _create_table()
    populate_dynamodb_google(table)


def setup_darksky():
    table = _create_table()
    populate_dynamodb_darksky(table)


def setup_listcouk():
    table = _create_table()
    populate_dynamodb_listcouk(table)


def _create_table():
    """Mock the caller with `moto` before calling this function"""
    global TABLE_CREATED
    dynamodb = boto3.resource("dynamodb")
    if TABLE_CREATED:
        return dynamodb.Table(db.TABLE_NAME)
    TABLE_CREATED = True
    return dynamodb.create_table(
        TableName=db.TABLE_NAME,
        KeySchema=[{"AttributeName": "key", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "key", "AttributeType": "S"}],
    )
