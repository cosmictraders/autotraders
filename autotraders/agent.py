from typing import Optional

from autotraders.faction.contract import Contract
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.ship import Ship


class Agent(SpaceTradersEntity):
    def __init__(self, session: AutoTradersSession, data=None):
        self.contracts: Optional[list[Contract]] = None
        self.starting_faction: Optional[str] = None
        self.symbol: Optional[str] = None
        self.account_id: Optional[str] = None
        self.credits: Optional[int] = None
        self.ships: Optional[Ship] = None
        self.headquarters: Optional[MapSymbol] = None
        super().__init__(session, "my/agent", data)

    def update(self, data=None):
        """Uses 3 API requests to get all agent details"""
        if data is None:
            data = self.get()["data"]
        self.account_id = data["accountId"]
        self.symbol = data["symbol"]
        self.headquarters = MapSymbol(data["headquarters"])
        self.credits = data["credits"]
        self.starting_faction = data["startingFaction"]
        self.ships = Ship.all(self.session)
        self.contracts = Contract.all(self.session)
