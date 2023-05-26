from typing import Optional

from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.faction.contract import get_all_contracts, Contract
from autotraders.session import AutoTradersSession
from autotraders.ship import get_all_ships, Ship


class Agent(SpaceTradersEntity):
    def __init__(self, session: AutoTradersSession, update=True):
        self.contracts: Optional[list[Contract]] = None
        self.starting_faction: Optional[str] = None
        self.symbol: Optional[str] = None
        self.account_id: Optional[str] = None
        self.credits: Optional[int] = None
        self.ships: Optional[Ship] = None
        self.headquarters: Optional[MapSymbol] = None
        super().__init__(session, update, "my/agent")

    def update(self, data=None):
        """Uses 3 API requests to get all agent details"""
        if data is None:
            data = self.get()["data"]
        self.account_id = data["accountId"]
        self.symbol = data["symbol"]
        self.headquarters = MapSymbol(data["headquarters"])
        self.credits = data["credits"]
        self.starting_faction = data["startingFaction"]
        self.ships = get_all_ships(self.session)
        self.contracts = get_all_contracts(self.session)
