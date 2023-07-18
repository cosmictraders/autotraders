"""A spacetraders api"""
import requests

from autotraders.session import AutoTradersSession  # noqa F401
from autotraders.status import get_status  # noqa F401

__version__ = "1.8.0"


def register_agent(
    symbol: str, faction: str, email=None, url="https://api.spacetraders.io/v2/"
):
    requests.post(
        url + "register",
        data={
            "faction": faction.upper(),
            "symbol": symbol,
            "email": email,
        },
    )
