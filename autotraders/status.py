from datetime import date
from typing import Any

import httpx
from pydantic import BaseModel, PositiveInt, Field, AwareDatetime, AnyUrl

from autotraders.error import SpaceTradersException


class Announcement(BaseModel):
    title: str
    body: str


class Link(BaseModel):
    name: str
    url: AnyUrl


class ServerResets(BaseModel):
    next: AwareDatetime
    frequency: str


class Status(BaseModel):
    """
    :ivar status: User-Readable description of the server status
    :ivar version: The server version
    :ivar reset_date: A datetime of the last reset date
    :ivar description: A user-readable description of the server
    :ivar stats: A dictionary of stats. The keys are agents, ships, systems, and waypoints
    :ivar leaderboards: The list of leaderboards (most credits, most charts)
    :ivar announcements: A list of announcements
    :ivar links: A list of useful links
    :ivar server_resets: Info about the server resets
    """

    status: str
    version: str
    reset_date: date = Field(alias="resetDate")
    description: str
    stats: dict[str, PositiveInt]
    leaderboards: dict[str, list[dict[str, Any]]]
    server_resets: ServerResets = Field(alias="serverResets")
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
        raise SpaceTradersException(
            j["error"], r.url, r.status_code, r.request.headers, r.headers
        )
    s = Status(**j)
    return s
