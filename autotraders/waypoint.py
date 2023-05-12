class Trait:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.name = data["name"]
        self.description = data["description"]

    def __str__(self):
        return self.name


class Waypoint:
    def __init__(self, symbol, session, update=True):
        self.session = session
        self.symbol = symbol
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


def get_waypoints(system, session):
    r = session.get("https://api.spacetraders.io/v2/systems/" + system + "/waypoints")
    data = r.json()["data"]
    waypoints = []
    for w in data:
        waypoint = Waypoint(w["symbol"], session, False)
        waypoint.update(w)
        waypoints.append(waypoint)
    return waypoints
