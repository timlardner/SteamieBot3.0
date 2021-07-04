import datetime as dt

from post_components.base import PostInterface
from reddit import Reddit


class MarketInfo(PostInterface):
    def get_header(self):
        return "/r/GlasgowMarket Digest"

    def get_body(self):
        posts = {}
        for post in Reddit().subreddit("GlasgowMarket").new():
            if post.link_flair_text is not None:
                continue
            received_time = dt.datetime.fromtimestamp(int(post.created_utc))
            time_difference = dt.datetime.utcnow() - received_time
            if time_difference < dt.timedelta(days=7):
                posts[post.permalink] = post.title
            else:
                break  # We're looking at posts over 7 days old now
        return "\n\n".join(f"[{value}]({key})" for key, value in posts.items()) or "No recent posts"

    @classmethod
    def can_update(cls) -> bool:
        return True
