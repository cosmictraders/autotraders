from typing import Union

from autotraders.error import SpaceTradersException
from autotraders.paginated_list import PaginatedList
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.map.waypoint import Waypoint
from autotraders.shared_models.map_symbol import MapSymbol


class System(SpaceTradersEntity):
    symbol: MapSymbol
    x: int
    y: int
    waypoints: list[Waypoint]
    factions: list[str]
    star_type: str
    jump_gate: bool

    def __init__(
        self, symbol: Union[str, MapSymbol], session: AutoTradersSession, data=None
    ):
        self.symbol: MapSymbol = MapSymbol(symbol)
        super().__init__(session, "systems/" + str(self.symbol) + "/", data)

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
        self.waypoints = [
            Waypoint(w["symbol"], self.session, w) for w in data["waypoints"]
        ]
        self.x = data["x"]
        self.y = data["y"]
        self.factions = data["factions"]
        self.star_type = data["type"]

    def __str__(self):
        return str(self.symbol)

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get(
                session.base_url
                + "systems?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(j["error"], r.status_code)
            systems = []
            for system in j["data"]:
                s = System(system["symbol"], session, system)
                systems.append(s)
            return systems, j["meta"]["total"]

        return PaginatedList(paginated_func, page)

    def __eq__(self, other):
        return self.symbol == other.symbol
