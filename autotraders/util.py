from datetime import datetime


def parse_time(time: str) -> datetime:
    try:
        return datetime.fromisoformat(time)
    except:
        try:
            return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            return datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
