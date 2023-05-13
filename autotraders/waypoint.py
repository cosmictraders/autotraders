import requests

from autotraders.trait import Trait


class Waypoint:
    def __init__(self, symbol, session: requests.Session, update=True):
        self.session = session
        self.symbol = symbol
        self.marketplace = False
        self.shipyard = False
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            split = self.symbol.split("-")
            system_symbol = split[0] + "-" + split[1]
            waypoint_symbol = self.symbol
            data = self.session.get(
                "https://api.spacetraders.io/v2/systems/"
                + system_symbol
                + "/waypoints/"
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


def get_all_waypoints(system, session):
    r = session.get("https://api.spacetraders.io/v2/systems/" + system + "/waypoints")
    data = r.json()["data"]
    waypoints = []
    for w in data:
        waypoint = Waypoint(w["symbol"], session, False)
        waypoint.update(w)
        waypoints.append(waypoint)
    return waypoints
