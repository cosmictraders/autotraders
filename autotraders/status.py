from datetime import datetime

import requests


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


def get_status() -> Status:
    """returns the API status, with reset dates, see the Status class for more info."""
    r = requests.get("https://api.spacetraders.io/v2/")
    j = r.json()
    s = Status()
    s.status = j["status"]
    s.version = j["version"]
    s.reset_date = j["resetDate"]
    s.description = j["description"]
    s.stats = j["stats"]
    s.next_reset = j["serverResets"]["nextReset"]
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
