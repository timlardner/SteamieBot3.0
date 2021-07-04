from moto import mock_dynamodb2

from config import state
from utils.db import get_key

from .common import _create_table


@mock_dynamodb2
def test_config():
    state.set_stateful(env="unittest")

    table = _create_table()
    table.put_item(Item={"key": get_key("env"), "foo": "bar"})

    assert state.get_stateful("foo") is None
    state.State.from_environment("unittest")
    assert state.get_stateful("foo") == "bar"
