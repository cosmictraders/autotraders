from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.map.waypoint import Waypoint
from autotraders.shared_models.map_symbol import MapSymbol


class System(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.symbol = MapSymbol(symbol)
        self.x = None
        self.y = None
        self.waypoints = None
        self.factions = None
        self.star_type = None
        super().__init__(
            session, update, session.base_url + "systems/" + str(self.symbol) + "/"
        )

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
        self.waypoints = []
        self.x = data["x"]
        self.y = data["y"]
        self.factions = data["factions"]
        self.star_type = data["type"]
        for w in data["waypoints"]:
            waypoint = Waypoint(w["symbol"], self.session, False)
            waypoint.update(w)
            self.waypoints.append(waypoint)

    @staticmethod
    def all(session, page=1) -> (list, int):
        r = session.get(session.base_url + "systems?limit=20&page=" + str(page))
        j = r.json()["data"]
        systems = []
        for system in j:
            s = System(system["symbol"], session, False)
            s.update(system)
            systems.append(s)
        return systems, r.json()["meta"]["total"]

    def __eq__(self, other):
        return self.symbol == other.symbol


def list_systems(session, page=1) -> (list[System], int):
    System.all(session, page)
