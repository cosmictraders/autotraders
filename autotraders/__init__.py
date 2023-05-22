"""A spacetraders api"""
from datetime import datetime

import requests

from autotraders.session import AutoTradersSession


class Status:
    status: str
    version: str
    reset_date: datetime
    description: str
    stats: dict[str, int]


def get_status() -> Status:  # TODO: Improve
    """returns the API status, with reset dates, see the Status class for more info."""
    r = requests.get("https://api.spacetraders.io/v2/")
    j = r.json()
    s = Status()
    s.status = j["status"]
    s.version = j["version"]
    s.reset_date = j["resetDate"]
    s.description = j["description"]
    s.stats = j["stats"]
    return s


class SpaceTradersEntity:
    def __init__(self, session: AutoTradersSession, update, action_url):
        self.session: AutoTradersSession = session
        self.action_url = action_url
        if self.action_url[-1] != "/":
            self.action_url += "/"
        if update:
            self.update()

    def get(self, action: str = "") -> dict:
        if action == "":
            r = self.session.get(self.action_url[0 : len(self.action_url) - 1])
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
