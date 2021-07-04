from moto import mock_dynamodb2
from utils import YouTubeInfo

from .common import setup_google


@mock_dynamodb2
def test_get_yt_title():
    setup_google()
    test_id = "WhBoR_tgXCI"
    youtube = YouTubeInfo()
    assert youtube.get_title(test_id) == "Dub FX 'Flow' feat. Mr Woodnote"
