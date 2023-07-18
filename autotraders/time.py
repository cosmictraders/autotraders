import sys
from datetime import datetime, timezone


def parse_time(time: str) -> datetime:
    """
    :param time: A string representing a timestamp in either ISO format (YYYY-MM-DDTHH:MM:SS.SSSZ) or a custom format (%Y-%m-%dT%H:%M:%S.%fZ).

    :return: A datetime object with the parsed timestamp.

    .. note::
        Works with python 3.9+ and parses timezones.
    """
    if sys.version_info.minor >= 11:
        return datetime.fromisoformat(time)
    else:
        try:
            d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                d = datetime.fromisoformat(time)
        d = d.replace(tzinfo=timezone.utc)
        return d
