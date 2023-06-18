from autotraders.faction.contract import Contract
from autotraders.paginated_list import PaginatedList
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.ship import Ship


class Agent(SpaceTradersEntity):
    contracts: PaginatedList
    starting_faction: str
    symbol: str
    account_id: str
    credits: int
    ships: PaginatedList
    headquarters: MapSymbol

    def __init__(self, session: AutoTradersSession, data=None):
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
