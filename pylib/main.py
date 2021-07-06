import logging

from config.state import State, get_stateful
from post_components.builder import PostBuilder
from reddit import Reddit, get_latest_submission
from utils.common import init_logging, local_time

log = logging.getLogger(__name__)


def main(is_update=False, env="dev"):
    State.from_environment(env)
    dry_run = get_stateful("dry_run", default=True)

    active_post = get_latest_submission()
    is_update = is_update and active_post is not None

    pb = PostBuilder(is_update=is_update)
    title, post = pb.build_post()

    if is_update:
        if not dry_run:
            active_post.edit(post)
            log.info(f"Updated {active_post.title}")
        else:
            log.info(f"Would update live post {active_post.title} with:\n{post}")
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
        log.info(f"Created new post: {submission.title}")
        if get_stateful("set_sticky"):
            submission.mod.sticky()
            log.info("Stickied")
    else:
        log.info(f"Would create new post: {title}\n{post}")


def lambda_handler(event, _):
    init_logging(level=logging.INFO)

    start_hour = event.get("start_time", 6)
    end_hour = event.get("end_time", 22)

    if not start_hour <= local_time().hour <= end_hour:  # Run from 6am to 10pm by default
        log.info("It's not time to make a post")
        return

    is_update = local_time().hour != start_hour and not event.get("force_post")
    main(is_update=is_update, env=event.get("env"))


if __name__ == "__main__":
    lambda_handler({"env": "prod"}, None)
