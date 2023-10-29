from typing import Optional

from pydantic import Field, BaseModel

from autotraders import SpaceTradersException
from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.transaction import ShipyardTransaction
from autotraders.ship import Frame, Reactor, Engine, Module, Mount, Ship


class ShipyardShip(BaseModel):
    ship_type: str = Field(alias="type")
    name: str
    description: str
    purchase_price: int = Field(alias="purchasePrice")
    frame: Frame
    reactor: Reactor
    engine: Engine
    modules: list[Module]
    mounts: list[Mount]


class Shipyard(WaypointType):
    ship_types: list[str]
    ships: Optional[list[ShipyardShip]]
    modifications_fee: int

    def __init__(
        self, waypoint: str, session: AutoTradersSession, data: Optional[dict] = None
    ):
        super().__init__(waypoint, "shipyard", session, data)

    def update(self, data: Optional[dict] = None):
        if data is None:
            data = self.get()["data"]
        self.ship_types = []
        for ship_type in data["shipTypes"]:
            self.ship_types.append(ship_type["type"])
        self.ships = None
        if "ships" in data:
            self.ships = []
            for ship in data["ships"]:
                self.ships.append(ShipyardShip(**ship))
        self.transactions = None
        if "transactions" in data:
            self.transactions = []
            for i in data["transactions"]:
                self.transactions.append(ShipyardTransaction(i))
        modifications_fee = data["modificationsFee"]

    def purchase(self, ship_type: str):
        r = self.session.post(
            "my/ships",
            json={"shipType": ship_type, "waypointSymbol": str(self.location)},
        )  # TODO: Fix
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(
                j["error"], r.url, r.status_code, r.request.headers, r.headers
            )
        return Ship(
            j["data"]["ship"]["symbol"], self.session, j["data"]["ship"]
        ), ShipyardTransaction(j["data"]["transaction"])
