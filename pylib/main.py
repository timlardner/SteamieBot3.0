import logging

from config.state import State, get_stateful
from post_components.builder import PostBuilder
from reddit import get_latest_submission, Reddit
from utils import local_time

log = logging.getLogger(__name__)


def main(is_update=False, dry_run=True, env="dev"):
    State.from_environment(env)

    pb = PostBuilder(is_update=is_update)
    title, post = pb.build_post()

    if is_update:
        active_post = get_latest_submission()
        if not dry_run:
            active_post.edit(post)
        else:
            log.info(f"Would update live post {active_post}")
    elif not dry_run:
        submission = (
            Reddit()
            .subreddit(get_stateful("subreddit"))
            .submit(
                title,
                selftext=post,
                flair_id=get_stateful("flair_id"),
                send_replies=False,
            )
        )
        if get_stateful("set_sticky"):
            submission.mod.sticky()
    else:
        log.info("Would create new post")


def lambda_handler(event, context):

    logging.basicConfig(level=logging.DEBUG)

    if not 6 <= local_time().hour <= 22:  # Run from 6am to 10om
        log.info("It's not time to make a post")
        return

    is_update = local_time().hour != 6
    main(is_update=is_update, dry_run=True)
