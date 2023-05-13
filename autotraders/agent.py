import requests

from autotraders.ship import get_all_ships
from autotraders.contract import get_all_contracts


class Agent:
    def __init__(self, session: requests.Session, update=True):
        self.session = session
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get("https://api.spacetraders.io/v2/my/agent")
            j = r.json()
            if "error" in j:
                raise IOError(j["error"]["message"])
            data = j["data"]
        self.account_id = data["accountId"]
        self.symbol = data["symbol"]
        self.headquarters = data["headquarters"]
        self.credits = data["credits"]
        self.ships = get_all_ships(self.session)
        self.contracts = get_all_contracts(self.session)
