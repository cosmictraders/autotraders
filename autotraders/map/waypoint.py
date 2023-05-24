from typing import Optional

from autotraders.session import AutoTradersSession
from autotraders.shared_models.trait import Trait

from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity


class Waypoint(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.waypoint_type: Optional[str] = None
        self.faction = None
        self.traits = None
        self.marketplace: Optional[bool] = None
        self.shipyard: Optional[bool] = None
        self.symbol = MapSymbol(symbol)
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        super().__init__(session, update, session.base_url
                         + "systems/"
                         + self.symbol.system
                         + "/waypoints/"
                         + self.symbol.waypoint)

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
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
    def all(system, session) -> (list, int):
        r = session.get(session.base_url + "systems/" + system + "/waypoints?limit=20")
        data = r.json()["data"]
        waypoints = []
        for w in data:
            waypoint = Waypoint(w["symbol"], session, False)
            waypoint.update(w)
            waypoints.append(waypoint)
        return waypoints, r.json()["meta"]["total"]

    def __eq__(self, other):
        return self.symbol == other.symbol


def get_all_waypoints(system, session):
    return Waypoint.all(system, session)
