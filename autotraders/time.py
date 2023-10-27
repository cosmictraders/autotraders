import sys
from datetime import datetime, timezone


def parse_time(time: str) -> datetime:
    """
    :param time: A string representing a timestamp in either ISO format (YYYY-MM-DDTHH:MM:SS.SSSZ)
                 or a custom format (%Y-%m-%dT%H:%M:%S.%fZ).

    :return: A datetime object with the parsed timestamp.

    .. note::
        Works with python 3.9+ and parses timezones.
    """
    if sys.version_info.minor >= 11:
        return datetime.fromisoformat(time)
    else:  # Workaround for python before 3.11
        try:
            d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                d = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:  # Workaround for stoplight
                d = datetime.fromisoformat(time)
        d = d.replace(
            tzinfo=timezone.utc
        )  # Makes the time timezone aware, so it is consistent with python 3.11+
        return d
