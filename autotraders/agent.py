from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.faction.contract import get_all_contracts
from autotraders.session import AutoTradersSession
from autotraders.ship import get_all_ships


class Agent(SpaceTradersEntity):
    def __init__(self, session: AutoTradersSession, update=True):
        self.contracts = None
        self.starting_faction = None
        self.symbol = None
        self.account_id = None
        self.credits = None
        self.ships = None
        self.headquarters = None
        super().__init__(session, update, session.base_url + "my/agent")

    def update(self, data=None):
        """Uses 3 API requests to get all agent details"""
        if data is None:
            data = self.get()["data"]
        self.account_id = data["accountId"]
        self.symbol = data["symbol"]
        self.headquarters = data["headquarters"]
        self.credits = data["credits"]
        self.starting_faction = data["startingFaction"]
        self.ships = get_all_ships(self.session)
        self.contracts = get_all_contracts(self.session)
