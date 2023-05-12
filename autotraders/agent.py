from sdk.contract import Contract
from sdk.ships import Ship, get_all_ships

from autotraders.autotraders.contract import get_all_contracts


class Agent:
    def __init__(self, session):
        self.session = session
        self.update()

    def update(self):
        r = self.session.get("https://api.spacetraders.io/v2/my/agent")
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.account_id = j["data"]["accountId"]
        self.symbol = j["data"]["symbol"]
        self.headquarters = j["data"]["headquarters"]
        self.credits = j["data"]["credits"]
        self.ships = get_all_ships(self.session)
        self.contracts = get_all_contracts(self.session)
