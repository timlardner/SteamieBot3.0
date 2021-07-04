from moto import mock_dynamodb2

from config.reddit import TEST_SUBREDDIT
from reddit import Reddit, get_latest_submission

from .common import setup_praw


@mock_dynamodb2
def test_reddit():
    setup_praw()

    submission = Reddit().subreddit(TEST_SUBREDDIT).submit("Test", selftext="Created by unit test")
    new_submission = get_latest_submission(subreddit=TEST_SUBREDDIT)
    try:
        assert submission == new_submission
    finally:
        submission.delete()
