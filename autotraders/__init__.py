"""A spacetraders api"""
import httpx

from autotraders.session import AutoTradersSession  # noqa F401
from autotraders.status import get_status  # noqa F401

__version__ = "2.0.0-alpha.1"


def register_agent(
    symbol: str, faction: str, email=None, url="https://api.spacetraders.io/v2/"
):  # TODO: Update
    j = httpx.post(
        url + "register",
        data={
            "faction": faction.upper(),
            "symbol": symbol,
            "email": email,
        },
    ).json()["data"]
    return j["token"]
