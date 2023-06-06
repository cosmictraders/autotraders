import sys
from datetime import datetime, timezone

from autotraders.ship.states import FlightMode


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
    if mode == FlightMode.CRUISE:
        return distance
    elif mode == FlightMode.DRIFT:
        return 1
    elif mode == FlightMode.BURN:
        return 2 * distance
    elif mode == FlightMode.STEALTH:
        return distance


def travel_time(distance, ship_speed, mode):
    if mode == FlightMode.CRUISE:
        return 15 + 10 * distance / ship_speed
    elif mode == FlightMode.DRIFT:
        return 15 + 100 * distance / ship_speed
    elif mode == FlightMode.BURN:
        return 15 + 5 * distance / ship_speed
    elif mode == FlightMode.STEALTH:
        return 15 + 20 * distance / ship_speed
