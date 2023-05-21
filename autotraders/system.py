import math

from autotraders.session import AutoTradersSession
from autotraders.waypoint import Waypoint


class System:
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.session = session
        self.symbol = symbol
        self.x = math.nan
        self.y = math.nan
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get(self.session.base_url + "systems/" + self.symbol)
            data = r.json()["data"]
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


def list_systems(session, page=1) -> (list[System], int):
    System.all(session, page)
