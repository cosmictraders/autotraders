from typing import Optional

from autotraders.error import SpaceTradersException
from autotraders.faction.contract import Contract
from autotraders.paginated_list import PaginatedList
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.ship import Ship


class Agent(SpaceTradersEntity):
    contracts: Optional[PaginatedList]
    starting_faction: str
    symbol: str
    account_id: str
    credits: int
    ship_count: int
    ships: Optional[PaginatedList]
    headquarters: MapSymbol

    def __init__(self, session: AutoTradersSession, symbol=None, data=None):
        if symbol is None:
            super().__init__(session, "my/agent", data)
        else:
            super().__init__(session, "agents/" + symbol, data)

    def update(self, data=None):
        """Uses 3 API requests to get all agent details"""
        if data is None:
            data = self.get()["data"]
        if "account_id" in data:
            self.account_id = data["accountId"]
            self.ships = Ship.all(self.session)
            self.contracts = Contract.all(self.session)
        self.symbol = data["symbol"]
        self.headquarters = MapSymbol(data["headquarters"])
        self.credits = data["credits"]
        self.starting_faction = data["startingFaction"]
        if "shipCount" in data:
            self.ship_count = data["shipCount"]

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get(
                session.base_url
                + "agents?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(j["error"], r.status_code)
            agents = []
            for agent in j["data"]:
                a = Agent(session, agent["symbol"], agent)
                agents.append(a)
            return agents, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)

