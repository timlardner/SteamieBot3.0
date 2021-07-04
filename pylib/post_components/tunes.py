import datetime as dt
import logging
import random
import re

import boto3
from googleapiclient.discovery import build

from config import db
from config.state import get_stateful
from post_components.base import PostInterface
from reddit import Reddit
from utils.common import Singleton
from utils.db import get_key

log = logging.getLogger(__name__)


class YouTubeInfo(metaclass=Singleton):
    def __init__(self):
        self.yt = self._auth()

    @staticmethod
    def _auth():
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(db.TABLE_NAME)
        response = table.get_item(Key={"key": get_key(db.GOOGLE_KEY)})
        api_key = response["Item"].get("api_key")
        yt = build("youtube", "v3", developerKey=api_key)
        return yt

    def get_title(self, this_id):
        response = self.yt.videos().list(part="id,snippet,statistics,contentDetails,status", id=this_id).execute()
        if not response["items"]:
            return None
        return response["items"][0]["snippet"]["title"]


class TuneInfo(PostInterface):
    def __init__(self):
        self.dry_run = get_stateful("dry_run")
        self.subreddit = get_stateful("subreddit")
        assert self.subreddit is not None

        self.pattern = re.compile(r"(?:youtube\.com/watch\?v=|youtu.be/)([0-9A-Za-z\-_]*)")
        self.author_link = []
        self.usage_age_floor = 3  # days

    def get_header(self) -> str:
        return "Tune of the day"

    def validate_message(self, message) -> bool:
        if message.was_comment:  # We don't want to include comment replies, just PMs
            return False

        time_difference = dt.datetime.utcnow() - dt.datetime.fromtimestamp(int(message.created_utc))
        if time_difference > dt.timedelta(days=1):  # We only want to look at messages from the last day
            return False

        if message.author in dict(self.author_link):
            log.debug(f"{message.author} has already submitted an eligible link today")
            return False

        if any(Reddit().subreddit(self.subreddit).banned(redditor=message.author)):
            log.debug(f"{message.author} is banned and ineligible to submit songs")
            return False

        sending_user = Reddit().redditor(message.author.name)
        time_difference = dt.datetime.utcnow() - dt.datetime.fromtimestamp(int(sending_user.created_utc))

        if time_difference < dt.timedelta(days=self.usage_age_floor):
            log.debug(f"{message.author.name} must be {self.usage_age_floor} days old to submit songs")
            return False

        return True

    def get_body(self) -> str:
        messages = Reddit().inbox.unread(mark_read=not self.dry_run)
        for message in messages:
            try:
                if not self.dry_run:
                    message.mark_read()

                log.debug(f"Received message from {message.author.name}")
                if not self.validate_message(message):
                    continue

                song_urls = self.pattern.findall(message.body + " " + message.subject)
                for url in song_urls:
                    if self.validate(url):
                        self.author_link.append((message.author.name, url))
                        break
            except Exception:
                log.exception("Failed to parse message")

        number_of_songs = len(self.author_link)

        if number_of_songs == 0:
            return self.get_scottish_music_string()
        elif number_of_songs == 1:
            suffix_string = f"Only one eligible link submitted today. [Suggest tomorrow's tune](https://www.reddit.com/message/compose/?to={Reddit().user.me().name}&subject=SongRequest&message=YouTube link here)."
        else:
            suffix_string = f"Picked from {number_of_songs} eligible links submitted today. [Suggest tomorrow's tune](https://www.reddit.com/message/compose/?to={Reddit().user.me().name}&subject=SongRequest&message=YouTube link here)."

        author, url = random.choice(self.author_link)
        title = self.get_song_title(url)
        return f"[{title}](https://youtu.be/{url}) (suggested by /u/{author}) \n\n{suffix_string}"

    def get_scottish_music_string(self):
        links_list = []
        suffix_string = f"No eligible links submitted today. [Suggest tomorrow's tune](https://www.reddit.com/message/compose/?to={Reddit().user.me().name}&subject=SongRequest&message=YouTube link here)."
        scottishmusictop = Reddit().subreddit("scottishmusic").hot(limit=5)
        for submission in scottishmusictop:
            song_urls = self.pattern.findall(submission.url)
            for url in song_urls:
                if self.validate(url):
                    links_list.append(submission.url)
        try:
            tune = random.choice(links_list)
        except IndexError:
            return f"Can't find a YouTube link on /r/ScottishMusic.\n\n{suffix_string}"
        title = self.get_song_title(tune)
        return f"[{title}]({tune})" f" (via /r/ScottishMusic) \n\n{suffix_string}"

    def get_song_title(self, vid):
        split_char = "/" if "youtu.be" in vid else "="
        return YouTubeInfo().get_title(vid.rsplit(split_char, 1)[-1])

    def validate(self, vid):
        return self.get_song_title(vid) is not None
