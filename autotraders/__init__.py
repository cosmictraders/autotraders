"""A spacetraders api"""
from datetime import datetime

import requests


class Status:
    status: str
    version: str
    reset_date: datetime
    description: str
    stats: dict[str, int]


def get_status():
    """returns the API status, with reset dates, see the Status class for more info."""
    r = requests.get("https://api.spacetraders.io/v2/")
    j = r.json()
    s = Status()
    s.status = j["status"]
    s.version = j["version"]
    s.reset_date = j["resetDate"]
    s.description = j["description"]
    s.stats = j["stats"]
