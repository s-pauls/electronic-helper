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


def str_isoformat_to_datetime(dt_str: str) -> datetime:
    # '2022-02-13T07:00:24+00:00'
    position = dt_str.find('+')
    dt_str = dt_str[:position] + dt_str[position:].replace(':', '')
    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S%z')
    return dt


def add_minsk_time_zone(dt: datetime) -> datetime:
    return dt.astimezone(pytz.timezone('Europe/Minsk'))
