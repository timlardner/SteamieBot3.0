from moto import mock_dynamodb2

from post_components.weather import Weather

from .common import setup_darksky


@mock_dynamodb2
def test_get_body():
    setup_darksky()

    t = Weather()
    response = t.get_body()
    assert response
