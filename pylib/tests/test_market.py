from moto import mock_dynamodb2

from post_components.market import MarketInfo

from .common import setup_praw


@mock_dynamodb2
def test_glasgow_market():
    setup_praw()

    body = MarketInfo().get_body()
    assert body
