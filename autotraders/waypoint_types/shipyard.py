import requests

from autotraders.ship import Frame, Reactor, Engine, Module, Mount


class ShipyardShip:
    def __init__(self, data):
        self.ship_type = data["type"]
        self.name = data["name"]
        self.description = data["description"]
        self.purchase_price = data["purchasePrice"]
        self.frame = Frame(data["frame"])
        self.reactor = Reactor(data["reactor"])
        self.engine = Engine(data["engine"])
        self.modules = [Module(d) for d in data["modules"]]
        self.mounts = [Mount(d) for d in data["mounts"]]


class Shipyard:
    def __init__(self, waypoint: str, session: requests.Session, update=True):
        self.location = waypoint
        self.session = session
        if update:
            self.update()

    def update(self, data: dict = None):
        if data is None:
            split = self.location.split("-")
            system_symbol = split[0] + "-" + split[1]
            waypoint_symbol = self.location
            data = self.session.get(
                "https://api.spacetraders.io/v2/systems/"
                + system_symbol
                + "/waypoints/"
                + waypoint_symbol
                + "/shipyard"
            ).json()["data"]
        self.ship_types = []
        for ship_type in data["shipTypes"]:
            self.ship_types.append(ship_type["type"])
        self.ships = None
        if "ships" in data:
            self.ships = []
            for ship in data["ships"]:
                ShipyardShip(ship)

    def purchase(self, ship_type: str):
        self.session.post(
            "https://api.spacetraders.io/v2/my/ships",
            data={"shipType": ship_type, "waypointSymbol": self.location},
        )
