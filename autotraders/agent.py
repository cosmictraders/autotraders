import math

from autotraders.contract import get_all_contracts
from autotraders.session import AutoTradersSession
from autotraders.ship import get_all_ships


class Agent:
    def __init__(self, session: AutoTradersSession, update=True):
        self.session = session
        self.credits = math.nan
        self.ships = None
        self.headquarters = None
        if update:
            self.update()

    def update(self, data=None):
        """Uses 3 API requests to get all agent details"""
        if data is None:
            r = self.session.get(self.session.base_url + "my/agent")
            j = r.json()
            print(j)
            if "error" in j:
                raise IOError(j["error"]["message"])
            data = j["data"]
        self.account_id = data["accountId"]
        self.symbol = data["symbol"]
        self.headquarters = data["headquarters"]
        self.credits = data["credits"]
        self.starting_faction = data["startingFaction"]
        self.ships = get_all_ships(self.session)
        self.contracts = get_all_contracts(self.session)
