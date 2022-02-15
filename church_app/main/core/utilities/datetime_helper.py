import pytz

from datetime import datetime, timezone

SUNDAY = 7


def add_utc_time_zone(dt: datetime):
    return dt.astimezone(pytz.UTC)


def now_with_utc_timezone():
    return datetime.now(timezone.utc)


def is_sunday(dt: datetime) -> bool:
    return dt.isoweekday() == SUNDAY


def youtube_datetime_to_datetime(dt_str: str) -> datetime:
    # youtube date format: '2022-02-13T07:00:24Z'
    dt = datetime.strptime(dt_str.replace('Z', '+0000'), '%Y-%m-%dT%H:%M:%S%z')
    return add_utc_time_zone(dt)
