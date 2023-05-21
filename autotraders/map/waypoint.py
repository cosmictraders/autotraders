import math

from autotraders.session import AutoTradersSession
from autotraders.trait import Trait


class Waypoint:
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.session = session
        self.symbol = symbol
        self.x = math.nan
        self.y = math.nan
        split = self.symbol.split("-")
        self.sector = split[0]
        self.system_symbol = split[0] + "-" + split[1]

        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            waypoint_symbol = self.symbol
            data = self.session.get(
                self.session.base_url
                + "systems/"
                + self.system_symbol
                + "/waypoints/?limit=20"
                + waypoint_symbol
            ).json()["data"]
        self.waypoint_type = data["type"]
        self.x = data["x"]
        self.y = data["y"]
        if "faction" in data:
            self.faction = data["faction"]["symbol"]
        else:
            self.faction = None
        self.traits = []
        if "traits" in data:
            for trait in data["traits"]:
                self.traits.append(Trait(trait))
        self.marketplace = (
            len([trait for trait in self.traits if trait.symbol == "MARKETPLACE"]) > 0
        )
        self.shipyard = (
            len([trait for trait in self.traits if trait.symbol == "SHIPYARD"]) > 0
        )

    @staticmethod
    def all(system, session):
        r = session.get(session.base_url + "systems/" + system + "/waypoints")
        data = r.json()["data"]
        waypoints = []
        for w in data:
            waypoint = Waypoint(w["symbol"], session, False)
            waypoint.update(w)
            waypoints.append(waypoint)
        return waypoints


def get_all_waypoints(system, session):
    return Waypoint.all(system, session)
