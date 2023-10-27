"""A spacetraders api"""

import httpx


from autotraders.error import SpaceTradersException
from autotraders.session import AutoTradersSession  # noqa F401
from autotraders.status import get_status  # noqa F401
from autotraders.version import __version__  # noqa F401


def register_agent(
    symbol: str, faction: str, email=None, url="https://api.spacetraders.io/v2/"
):  # TODO: Update
    r = httpx.post(
        url + "register",
        json={
            "faction": faction.upper(),
            "symbol": symbol,
            "email": email,
        },
    )
    j = r.json()
    if "error" in j:
        raise SpaceTradersException(
            j["error"], r.url, r.status_code, r.request.headers, r.headers
        )
    return j["data"]["token"]
