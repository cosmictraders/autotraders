from typing import Union, Optional

from autotraders.error import SpaceTradersException
from autotraders.map.waypoint import Waypoint
from autotraders.paginated_list import PaginatedList
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.shared_models.system_symbol import SystemSymbol
from autotraders.space_traders_entity import SpaceTradersEntity


class System(SpaceTradersEntity):
    symbol: SystemSymbol
    x: int
    y: int
    waypoints: list[Waypoint]
    factions: list[str]
    star_type: str
    jump_gate: bool

    def __init__(
        self,
        symbol: Union[str, MapSymbol],
        session: AutoTradersSession,
        data: Optional[dict] = None,
    ):
        if symbol is None:
            symbol = data["symbol"]
        self.symbol = SystemSymbol(symbol)
        super().__init__(session, "systems/" + str(self.symbol) + "/", data)

    def update(self, data=None):
        data = super()._update(data)
        mappings = {"x": {}, "y": {}}
        super().update_attr(mappings, data)
        self.waypoints = [
            Waypoint(w["symbol"], self.session, w) for w in data["waypoints"]
        ]
        self.factions = [faction["symbol"] for faction in data["factions"]]
        self.star_type = data["type"]

    def __str__(self):
        return str(self.symbol)

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get("systems?limit=" + str(num_per_page) + "&page=" + str(p))
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(
                    j["error"], r.url, r.status_code, r.request.headers, r.headers
                )
            systems = []
            for system in j["data"]:
                s = System(system["symbol"], session, system)
                systems.append(s)
            return systems, j["meta"]["total"]

        return PaginatedList(paginated_func, page)

    def __eq__(self, other):
        return self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)
