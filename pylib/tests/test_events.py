from moto import mock_dynamodb2

from post_components.events import EventInfo

from .common import setup_listcouk


@mock_dynamodb2
def test_events():
    setup_listcouk()

    ei = EventInfo()
    text = ei.get_body()
    assert text
