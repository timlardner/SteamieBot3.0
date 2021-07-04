import datetime as dt

import pytz


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def local_time(timezone="Europe/London") -> dt.datetime:
    utc_now = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
    new_tz = pytz.timezone(timezone)
    return utc_now.astimezone(new_tz)
