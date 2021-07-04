from moto import mock_dynamodb2

from config import reddit
from config.state import set_stateful
from post_components.tunes import TuneInfo, YouTubeInfo
from reddit import Reddit

from .common import setup_google, setup_praw


@mock_dynamodb2
def test_tunes():
    set_stateful(dry_run=True, subreddit=reddit.TEST_SUBREDDIT)

    setup_praw()
    setup_google()

    Reddit().user.me().message("Song suggestion", "https://www.youtube.com/watch?v=M3BZ8hnLyRc")

    t = TuneInfo()
    response = t.get_body()
    assert "No eligible links" in response


@mock_dynamodb2
def test_get_yt_title():
    setup_google()
    test_id = "WhBoR_tgXCI"
    youtube = YouTubeInfo()
    assert youtube.get_title(test_id) == "Dub FX 'Flow' feat. Mr Woodnote"
