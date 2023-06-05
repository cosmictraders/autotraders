from typing import Optional, Union

from autotraders.paginated_list import PaginatedList
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.map.waypoint import Waypoint
from autotraders.shared_models.map_symbol import MapSymbol


class System(SpaceTradersEntity):
    def __init__(
        self, symbol: Union[str, MapSymbol], session: AutoTradersSession, data=None
    ):
        self.symbol: MapSymbol = MapSymbol(symbol)
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        self.waypoints: Optional[list[Waypoint]] = None
        self.factions: Optional[list[str]] = None
        self.star_type: Optional[str] = None
        super().__init__(session, "systems/" + str(self.symbol) + "/", data)

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
        self.waypoints = []
        self.x = data["x"]
        self.y = data["y"]
        self.factions = data["factions"]
        self.star_type = data["type"]
        for w in data["waypoints"]:
            waypoint = Waypoint(w["symbol"], self.session, w)
            self.waypoints.append(waypoint)

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
            j = r.json()["data"]
            if "error" in j:
                raise IOError(j["error"]["message"])
            systems = []
            for system in j:
                s = System(system["symbol"], session, system)
                systems.append(s)
            return systems, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)

    def __eq__(self, other):
        return self.symbol == other.symbol
