import asyncio
import time
from datetime import datetime, timezone
from enum import Enum
from typing import Union, Optional

from pydantic import BaseModel, Field

from autotraders.error import SpaceTradersException
from autotraders.map.system import System
from autotraders.map.waypoint import Waypoint
from autotraders.paginated_list import PaginatedList
from autotraders.session import AutoTradersSession
from autotraders.shared_models.item import Item
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.shared_models.transaction import MarketTransaction, ShipyardTransaction
from autotraders.shared_models.waypoint_symbol import WaypointSymbol
from autotraders.ship.cargo import Cargo
from autotraders.ship.cooldown import Cooldown
from autotraders.ship.cooldown import Cooldown
from autotraders.ship.fuel import Fuel
from autotraders.ship.fuel import Fuel
from autotraders.ship.nav import Nav
from autotraders.ship.ship_components import Frame, Reactor, Engine, Module, Mount
from autotraders.ship.states import FlightMode
from autotraders.ship.survey import Survey
from autotraders.space_traders_entity import SpaceTradersEntity


class RotationEnum(str, Enum):
    RELAXED = "RELAXED"
    STRICT = "STRICT"


class Crew(BaseModel):
    current: int
    required: int
    capacity: int
    morale: int
    wages: int
    rotation: RotationEnum


class Registration(BaseModel):
    name: str
    faction_symbol: str = Field(alias="factionSymbol")
    role: str


class Capabilities:
    """
    :ivar warp: can the ship warp
    :ivar jump: can the ship jump without a jump gate
    :ivar mine: can the ship mine (experimental)
    """

    def __init__(self, modules, mounts):
        warp_drives = [module for module in modules if "warp" in module.symbol.lower()]
        jump_drives = [module for module in modules if "jump" in module.symbol.lower()]
        mine = [mount for mount in mounts if "mining" in mount.symbol.lower()]
        self.warp = any(warp_drives)
        self.jump = any(jump_drives)
        self.mine = any(mine)


class Ship(SpaceTradersEntity):
    cargo: Cargo
    fuel: Fuel
    nav: Nav
    symbol: str
    frame: Frame
    reactor: Reactor
    engine: Engine
    modules: list[Module]
    mounts: list[Mount]
    crew: Crew
    registration: Registration
    capabilities: Optional[Capabilities]
    cooldown: Optional[Cooldown]

    def __init__(
        self, symbol, session: AutoTradersSession, data: Optional[dict] = None
    ):
        if symbol is None:
            symbol = data["symbol"]
        self.symbol = symbol
        super().__init__(session, "my/ships/" + self.symbol, data)

    def update(self, data: Optional[dict] = None) -> None:
        if data is None:
            data = super()._update(data)
        mappings = {
            "crew": {"type": "object", "class": Crew},
            "frame": {"type": "object", "class": Frame},
            "cooldown": {"type": "dynamic", "class": Cooldown},
            "reactor": {"type": "object", "class": Reactor},
            "engine": {"type": "object", "class": Engine},
            "nav": {"type": "dynamic", "class": Nav},
            "fuel": {"type": "object", "class": Fuel},
            "cargo": {"type": "dynamic", "class": Cargo},
            "registration": {"type": "object", "class": Registration},
        }
        super().update_attr(mappings, data)
        if "modules" in data:
            self.modules = [Module(**d) for d in data["modules"]]
        if "mounts" in data:
            self.mounts = [Mount(**d) for d in data["mounts"]]
        if self.modules is not None and self.mounts is not None:
            self.capabilities = Capabilities(self.modules, self.mounts)

    def __str__(self):
        return self.symbol

    def wait_transit(self):
        if (
            sleep_time := (
                self.nav.route.arrival - datetime.now(timezone.utc)
            ).total_seconds()
            + 0.5
            > 0
        ):
            time.sleep(sleep_time)

    async def await_transit(self):
        if (
            sleep_time := (
                self.nav.route.arrival - datetime.now(timezone.utc)
            ).total_seconds()
            + 0.5
            > 0
        ):
            await asyncio.sleep(sleep_time)

    def wait_cooldown(self):
        if self.cooldown is not None:
            time.sleep(
                (self.cooldown.expiration - datetime.now(timezone.utc)).total_seconds()
                + 1
            )

    async def await_cooldown(self):
        if self.cooldown is not None:
            await asyncio.sleep(
                (self.cooldown.expiration - datetime.now(timezone.utc)).total_seconds()
                + 1
            )

    def navigate(self, waypoint: Union[str, MapSymbol]):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function exits immediately, and does not wait the ship to arrive.
        """
        self.fuel = self.nav.navigate(WaypointSymbol(waypoint))

    def jump(self, destination: Union[str, MapSymbol]):
        self.cooldown = self.nav.jump(destination)

    def warp(self, destination: Union[str, MapSymbol]):
        self.fuel = self.nav.warp(destination)

    def patch_navigation(self, new_flight_mode: Union[str, FlightMode]):
        self.nav.patch_flight_mode(new_flight_mode)

    def dock(self):
        self.nav.dock()

    def orbit(self):
        self.nav.orbit()

    def extract(self, extraction_survey: Optional[Survey] = None):
        if extraction_survey is None:
            j = self.post("extract")
        else:
            j = self.post(
                "extract/survey",
                data=extraction_survey.model_dump(mode="json"),
            )
        self.update(j["data"])
        return Item(
            symbol=j["data"]["extraction"]["yield"]["symbol"],
            quantity=j["data"]["extraction"]["yield"]["units"],
        )

    def siphon(self):
        j = self.post("siphon")
        self.update(j["data"])
        return Item(
            symbol=j["data"]["siphon"]["yield"]["symbol"],
            quantity=j["data"]["siphon"]["yield"]["units"],
        )

    def refuel(self, from_cargo=False, units=None):
        if units is None:
            j = self.post("refuel", data={"fromCargo": from_cargo})
        else:
            j = self.post("refuel", data={"units": units, "fromCargo": from_cargo})
        self.update(j["data"])
        return MarketTransaction(j["data"]["transaction"])

    def sell(self, cargo_symbol: str, quantity: int):
        j = self.post("sell", data={"symbol": cargo_symbol, "units": quantity})
        self.update(j["data"])
        return MarketTransaction(j["data"]["transaction"])

    def buy(self, cargo_symbol: str, quantity: int):
        j = self.post("purchase", data={"symbol": cargo_symbol, "units": quantity})
        self.update(j["data"])
        return MarketTransaction(j["data"]["transaction"])

    def transfer(self, destination: str, cargo_symbol: str, quantity: int):
        j = self.post(
            "transfer",
            data={
                "tradeSymbol": cargo_symbol,
                "units": quantity,
                "shipSymbol": destination,
            },
        )
        self.update(j["data"])

    def jettison(self, cargo_symbol: str, quantity: int):
        j = self.post(
            "jettison",
            data={"symbol": cargo_symbol, "units": quantity},
        )
        self.update(j["data"])

    def refine(self, output_symbol: str):
        j = self.post(
            "refine",
            data={"produce": output_symbol},
        )
        self.update(j["data"])
        return [
            Item(symbol=i["tradeSymbol"], quantity=i["units"])
            for i in j["data"]["produced"]
        ]

    def chart(self) -> Waypoint:
        """
        Charts the current waypoint

        :returns: The info about the waypoint that has been charted
        """
        j = self.post("chart")
        w = Waypoint(
            j["data"]["waypoint"]["symbol"], self.session, j["data"]["waypoint"]
        )
        return w

    def survey(self) -> list[Survey]:
        j = self.post("survey")
        surveys = []
        for s in j["data"]["surveys"]:
            surveys.append(Survey(**s))
        return surveys

    def scan_systems(self) -> list[System]:
        j = self.post("scan/systems")
        systems = []
        for system in j["systems"]:
            s = System(system["symbol"], self.session, system)
            systems.append(s)
        return systems

    def scan_waypoints(self) -> list[Waypoint]:
        j = self.post("scan/waypoints")
        waypoints = []
        for waypoint in j["waypoints"]:
            w = Waypoint(waypoint["symbol"], self.session, waypoint)
            waypoints.append(w)
        return waypoints

    def scan_ships(self) -> list:
        j = self.post("scan/ships")
        ships = []
        for ship in j["data"]["ships"]:
            s = ship["symbol"]
            ships.append(s)
        return ships

    def install_mount(self, mount_symbol: str):
        j = self.post("mounts/install", data={"symbol": mount_symbol})
        self.update(j["data"])
        return ShipyardTransaction(j["data"]["transaction"])

    def remove_mount(self, mount_symbol: str):
        j = self.post("mounts/remove", data={"symbol": mount_symbol})
        self.update(j["data"])
        return ShipyardTransaction(j["data"]["transaction"])

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get("my/ships?limit=" + str(num_per_page) + "&page=" + str(p))
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(
                    j["error"], r.url, r.status_code, r.request.headers, r.headers
                )
            ships = []
            for ship in j["data"]:
                s = Ship(ship["symbol"], session, ship)
                ships.append(s)
            return ships, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)
