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


def travel_fuel(distance, mode):
    if mode == "CRUISE":
        return distance
    elif mode == "DRIFT":
        return 1
    elif mode == "BURN":
        return 2 * distance
    elif mode == "STEALTH":
        return distance


def travel_time(distance, ship_speed, mode):
    if mode == "CRUISE":
        return 15 + 10 * distance / ship_speed
    elif mode == "DRIFT":
        return 15 + 100 * distance / ship_speed
    elif mode == "BURN":
        return 15 + 5 * distance / ship_speed
    elif mode == "STEALTH":
        return 15 + 20 * distance / ship_speed
