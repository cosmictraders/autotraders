from datetime import datetime

import httpx
from pydantic import BaseModel, PositiveInt, Field, AwareDatetime, AnyUrl
from autotraders.error import SpaceTradersException


class LeaderboardPlayer(BaseModel):
    symbol: str
    value: int


class Leaderboard(BaseModel):
    name: str
    players: list[LeaderboardPlayer]


class Announcement(BaseModel):
    title: str
    body: str


class Link(BaseModel):
    name: str
    url: AnyUrl


class Status(BaseModel):
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
    reset_date: AwareDatetime = Field(alias="resetDate")
    description: str
    stats: dict[str, PositiveInt]
    leaderboards: list[Leaderboard]
    next_reset: datetime = Field(alias="nextReset")
    reset_frequency: str = Field(alias="resetFrequency")
    announcements: list[Announcement]
    links: list[Link]


def get_status(session=None) -> Status:
    """returns the API status, with reset dates, see the Status class for more info."""
    if session is None:
        r = httpx.get("https://api.spacetraders.io/v2/")
    else:
        r = session.get("https://api.spacetraders.io/v2/")
    j = r.json()
    if "error" in j:
        raise SpaceTradersException(j["error"], r.status_code)
    s = Status(**j)
    return s
