import sys
from datetime import datetime, timezone


def parse_time(time: str) -> datetime:
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
