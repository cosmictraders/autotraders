from typing import Optional, Union

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
    def all(session, page=1) -> (list, int):
        r = session.get(session.base_url + "systems?limit=20&page=" + str(page))
        j = r.json()["data"]
        systems = []
        for system in j:
            s = System(system["symbol"], session, system)
            systems.append(s)
        return systems, r.json()["meta"]["total"]

    def __eq__(self, other):
        return self.symbol == other.symbol
