import asyncio
import json
from typing import Union, Optional

import requests

from autotraders.error import SpaceTradersException
from autotraders.paginated_list import PaginatedList
from autotraders.shared_models.item import Item
from autotraders.shared_models.transaction import MarketTransaction, ShipyardTransaction
from autotraders.ship.cargo import Cargo
from autotraders.ship.nav import Nav
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.map.system import System
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship.ship_components import Frame, Reactor, Engine, Module, Mount
from autotraders.ship.survey import Survey
from autotraders.time import parse_time
from autotraders.map.waypoint import Waypoint


class Fuel:
    def __init__(self, current, total):
        self.current = current
        self.total = total

    def __str__(self):
        return str(self.current) + "/" + str(self.total)


class Crew:
    def __init__(self, data):
        self.current: int = data["current"]
        self.required: int = data["required"]
        self.capacity: int = data["capacity"]
        self.morale = data["morale"]
        self.wages = data["wages"]
        self.rotation = data["rotation"]


class Registration:
    def __init__(self, data):
        self.name: str = data["name"]
        self.faction_symbol: str = data["factionSymbol"]
        self.role: str = data["role"]


class Capabilities:
    """
    :ivar warp: can the ship warp
    :ivar jump: can the ship jump without a jump gate
    :ivar mine: can the ship mine (experimental)
    """

    def __init__(self, modules, mounts):
        warp_drives = [module for module in modules if "warp" in module.symbol.lower()]
        jump_drives = [module for module in modules if "jump" in module.symbol.lower()]
        mine = [mount for mount in mounts if "mine" in mount.symbol.lower()]
        self.warp = len(warp_drives) > 0
        self.jump = len(jump_drives) > 0
        self.mine = len(mine) > 0


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

    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.symbol = symbol
        super().__init__(session, "my/ships/" + self.symbol, data)

    def update(self, data: dict = None) -> None:
        if data is None:
            data = self.get()["data"]

        if "crew" in data:
            self.crew = Crew(data["crew"])
        if "frame" in data:
            self.frame = Frame(data["frame"])
        if "reactor" in data:
            self.reactor = Reactor(data["reactor"])
        if "engine" in data:
            self.engine = Engine(data["engine"])
        if "modules" in data:
            self.modules = [Module(d) for d in data["modules"]]
        if "mounts" in data:
            self.mounts = [Mount(d) for d in data["mounts"]]
        if "nav" in data:
            self.nav = Nav(self.symbol, self.session, data["nav"])
        if "fuel" in data:
            self.fuel = Fuel(data["fuel"]["current"], data["fuel"]["capacity"])
        if "cargo" in data:
            self.cargo = Cargo(self.symbol, self.session, data["cargo"])
        if "registration" in data:
            self.registration = Registration(data["registration"])
        if self.modules is not None and self.mounts is not None:
            self.capabilities = Capabilities(self.modules, self.mounts)

    def __str__(self):
        return self.symbol

    async def navigate_async(self, waypoint: Union[str, MapSymbol], interval=1):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function waits for the ship to arrive.
        :param interval: Frequency of updates in seconds (default: 1)
        """
        j = self.post("navigate", data={"waypointSymbol": str(waypoint)})
        self.update(j["data"])
        while self.nav.status == "IN_TRANSIT":
            await asyncio.sleep(interval)
            self.update()

    def navigate(self, waypoint: Union[str, MapSymbol]):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function exits immediately, and does not wait the ship to arrive.
        """
        j = self.post("navigate", data={"waypointSymbol": str(waypoint)})
        self.update(j["data"])

    def jump(self, destination: Union[str, MapSymbol]):
        j = self.post(
            "jump",
            data={
                "systemSymbol": str(destination),
            },
        )
        self.update(j["data"])
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])

    def warp(self, destination: Union[str, MapSymbol]):
        j = self.post(
            "warp",
            data={
                "waypointSymbol": str(destination),
            },
        )
        self.update(j["data"])

    def patch_navigation(self, new_flight_mode):
        r = self.session.patch(
            self.session.base_url + "my/ships/" + self.symbol + "/nav",
            data=json.dumps(
                {"flightMode": new_flight_mode}
            )  # Requests is so dumb I spent 30 minutes debugging this
            # just to find that its requests fault for sending a body of "flightMode=DRIFT".
        )
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(j["error"], r.status_code)
        self.update({"nav": j["data"]})

    def dock(self):
        j = self.post("dock")
        self.update(j["data"])

    def orbit(self):
        j = self.post("orbit")
        self.update(j["data"])

    def extract(self, survey: Survey = None):
        if survey is None:
            j = self.post("extract")
        else:
            j = self.post(
                "extract",
                data={
                    "signature": survey.signature,
                    "symbol": survey.symbol,
                    "deposits": survey.deposits,
                    "expiration": survey.expiration.isoformat(),
                    "size": survey.size,
                },
            )
        self.update(j["data"])
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return Item(
            j["data"]["extraction"]["yield"]["symbol"],
            j["data"]["extraction"]["yield"]["units"],
            None,
        )

    def refuel(self, units=None):
        if units is None:
            j = self.post("refuel")
        else:
            j = self.post("refuel", data={
                "units": units
            })
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
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return [Item(i["tradeSymbol"], i["units"], None) for i in j["data"]["produced"]]

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
            surveys.append(Survey(s))
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return surveys

    def scan_systems(self) -> list[System]:
        j = self.post("scan/systems")
        systems = []
        for system in j["systems"]:
            s = System(system["symbol"], self.session, system)
            systems.append(s)
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return systems

    def scan_waypoints(self) -> list[Waypoint]:
        j = self.post("scan/waypoints")
        waypoints = []
        for waypoint in j["waypoints"]:
            w = Waypoint(waypoint["symbol"], self.session, waypoint)
            waypoints.append(w)
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return waypoints

    def scan_ships(self) -> list:
        j = self.post("scan/ships")
        ships = []
        for ship in j["data"]["ships"]:
            s = Ship(ship["symbol"], self.session, ship)
            ships.append(s)
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return ships

    def update_ship_cooldown(self):
        try:  # TODO: get more elegant solution
            j = self.get("cooldown")
            self.reactor.cooldown = parse_time(j["data"]["expiration"])
        except requests.exceptions.JSONDecodeError:
            self.reactor.cooldown = None

    def install_mount(self, mount_symbol: str):
        j = self.post("mounts/install", data={"symbol": mount_symbol})
        self.update(j["data"])
        return ShipyardTransaction(j["data"]["transaction"])

    def remove_mount(self, mount_symbol: str):
        j = self.post("mounts/remove", data={"symbol": mount_symbol})
        print(j)
        self.update(j["data"])
        return ShipyardTransaction(j["data"]["transaction"])

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get(
                session.base_url
                + "my/ships?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(j["error"], r.status_code)
            ships = []
            for ship in j["data"]:
                s = Ship(ship["symbol"], session, ship)
                ships.append(s)
            return ships, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)
