import pickle

from moto import mock_dynamodb2

from config import db, reddit
from config.state import set_stateful
from post_components.builder import PostBuilder, MODULE_LIST
from utils.db import get_key

from .common import setup_listcouk, setup_praw, setup_google, setup_darksky


@mock_dynamodb2
def test_post_builder():
    setup_listcouk()
    setup_praw()
    setup_google()
    setup_darksky()

    set_stateful(dry_run=True, subreddit=reddit.TEST_SUBREDDIT)

    pb = PostBuilder(is_update=False)

    title, body = pb.build_post()
    assert "The Steamie" in title
    assert len(body) < 10000
    res = pb.table.get_item(Key={"key": get_key(db.DATA_KEY)})
    assert len(pickle.loads(res["Item"]["data"].value)) == len(MODULE_LIST)
