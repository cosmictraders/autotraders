class Shipyard:
    def __init__(self, waypoint: str, session, update=True):
        self.location = waypoint
        self.session = session
        if update:
            self.update()

    def update(self, data: dict = None):
        if data is None:
            split = self.location.split("-")
            system_symbol = split[0] + "-" + split[1]
            waypoint_symbol = self.location
            data = self.session.get("https://api.spacetraders.io/v2/systems/"
                                    + system_symbol + "/waypoints/"
                                    + waypoint_symbol + "/shipyard").json()["data"]
        self.ship_types = []
        for ship_type in data["shipTypes"]:
            self.ship_types.append(ship_type["type"])
