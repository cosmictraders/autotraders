from datetime import datetime

import requests

from autotraders.error import SpaceTradersException
from autotraders.time import parse_time


class LeaderboardPlayer:
    symbol: str
    value: int


class Leaderboard:
    name: str
    players: list[LeaderboardPlayer]


class Announcement:
    title: str
    body: str

    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body


class Link:
    name: str
    url: str

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url


class Status:
    """
    :ivar status: User-Readable description of the server status
    :ivar version: The server version
    :ivar reset_date: A datetime of the last reset date
    :ivar description: A user-readable description of the server
    :ivar stats: A dictionary of stats. The keys are agents, ships, systems, and waypoints
    :ivar leaderboards: The list of leaderboards (most credits, most charts)
    :ivar next_reset: A datetime of the next reset
    :ivar reset_frequency: A user-readable description of the server reset frequency
    :ivar announcements: A list of announcements
    :ivar links: A list of useful links
    """

    status: str
    version: str
    reset_date: datetime
    description: str
    stats: dict[str, int]
    leaderboards: list[Leaderboard]
    next_reset: datetime
    reset_frequency: str
    announcements: list[Announcement]
    links: list[Link]


def get_status(session=None) -> Status:
    """returns the API status, with reset dates, see the Status class for more info."""
    if session is None:
        r = requests.get("https://api.spacetraders.io/v2/")
    else:
        r = session.get("https://api.spacetraders.io/v2/")
    j = r.json()
    if "error" in j:
        raise SpaceTradersException(j["error"], r.status_code)
    s = Status()
    s.status = j["status"]
    s.version = j["version"]
    s.reset_date = parse_time(j["resetDate"])
    s.description = j["description"]
    s.stats = j["stats"]
    s.next_reset = parse_time(j["serverResets"]["next"])
    s.reset_frequency = j["serverResets"]["frequency"]
    s.announcements = []
    for announcement in j["announcements"]:
        s.announcements.append(
            Announcement(title=announcement["title"], body=announcement["body"])
        )
    s.links = []
    for link in j["links"]:
        s.links.append(Link(name=link["name"], url=link["url"]))
    return s
