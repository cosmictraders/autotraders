from typing import Optional

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.transaction import ShipyardTransaction
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


class Shipyard(WaypointType):
    def __init__(self, waypoint: str, session: AutoTradersSession, update=True):
        self.ship_types: Optional[list[str]] = None
        self.ships: Optional[list[ShipyardShip]] = None
        super().__init__(waypoint, "shipyard", session, update)

    def update(self, data: dict = None):
        if data is None:
            data = self.get()["data"]
        self.ship_types = []
        for ship_type in data["shipTypes"]:
            self.ship_types.append(ship_type["type"])
        self.ships = None
        if "ships" in data:
            self.ships = []
            for ship in data["ships"]:
                self.ships.append(ShipyardShip(ship))

    def purchase(self, ship_type: str):
        j = self.session.post(
            self.session.base_url + "my/ships",
            data={"shipType": ship_type, "waypointSymbol": self.location},
        ).json()
        return ShipyardTransaction(j["data"]["transaction"])
