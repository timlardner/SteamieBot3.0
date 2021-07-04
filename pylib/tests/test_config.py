from moto import mock_dynamodb2

from config import state

from .common import _create_table


@mock_dynamodb2
def test_config():
    table = _create_table()
    table.put_item(Item={"key": "env-test", "foo": "bar"})

    assert state.get_stateful("foo") is None
    state.State.from_environment("test")
    assert state.get_stateful("foo") == "bar"
