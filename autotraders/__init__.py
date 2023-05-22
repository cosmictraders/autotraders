"""A spacetraders api"""
from datetime import datetime

import requests

from autotraders.session import AutoTradersSession


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
        s.announcements.append(Announcement(title=announcement["title"], body=announcement["body"]))
    s.links = []
    for link in j["links"]:
        s.links.append(Link(name=link["name"], url=link["url"]))
    return s


class SpaceTradersEntity:
    def __init__(self, session: AutoTradersSession, update, action_url):
        self.session: AutoTradersSession = session
        self.action_url = action_url
        if self.action_url[-1] != "/":
            self.action_url += "/"
        if update:
            self.update()

    def get(self, action: str = None) -> dict:
        if action is None:
            r = self.session.get(self.action_url[0: len(self.action_url) - 1])
        else:
            r = self.session.get(
                self.action_url + action,
            )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        return j

    def post(self, action: str, data=None) -> dict:
        self.session.headers["Content-Type"] = "application/json"
        r = self.session.post(
            self.action_url + action,
            data=data,
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        return j

    def update(self):
        pass
