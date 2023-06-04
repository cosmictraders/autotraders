import asyncio
from datetime import datetime, timezone
from typing import Union, Optional

from autotraders.shared_models.item import Item
from autotraders.shared_models.transaction import MarketTransaction
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.map.system import System
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship.ship_components import Frame, Reactor, Engine, Module, Mount
from autotraders.ship.survey import Survey
from autotraders.util import parse_time
from autotraders.map.waypoint import Waypoint


class Fuel:
    def __init__(self, current, total):
        self.current = current
        self.total = total

    def __str__(self):
        return str(self.current) + "/" + str(self.total)


class Cargo:
    def __init__(self, j):
        self.capacity = j["capacity"]
        inventory = j["inventory"]
        self.inventory = []
        self.current = 0
        for symbol in inventory:
            self.inventory.append(
                Item(symbol["symbol"], symbol["units"], symbol["description"])
            )
            self.current += symbol["units"]


class Route:
    def __init__(self, data):
        self.destination = MapSymbol(data["destination"]["symbol"])
        self.departure = MapSymbol(data["departure"]["symbol"])
        self.departure_time = parse_time(data["departureTime"])
        self.arrival = parse_time(data["arrival"])
        self.moving = self.arrival > datetime.now(timezone.utc)


class Nav:
    def __init__(self, data):
        self.status = data["status"]
        self.location = MapSymbol(data["waypointSymbol"])
        self.flight_mode = data["flightMode"]
        self.route = Route(data["route"])
        self.moving = self.route.moving


class Crew:
    def __init__(self, data):
        self.current = data["current"]
        self.required = data["required"]
        self.capacity = data["capacity"]
        self.morale = data["morale"]
        self.wages = data["wages"]


class Ship(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.cargo: Optional[Cargo] = None
        self.fuel: Optional[Fuel] = None
        self.nav: Optional[Nav] = None
        self.symbol: str = symbol
        self.frame: Optional[Frame] = None
        self.reactor: Optional[Reactor] = None
        self.engine: Optional[Engine] = None
        self.modules: Optional[list[Module]] = None
        self.mounts: Optional[list[Mount]] = None
        self.crew: Optional[Crew] = None
        super().__init__(session, "my/ships/" + self.symbol, data)

    def update(self, data: dict = None, hard=False) -> None:  # TODO: Hard is deprecated
        """
        :param hard: deprecated does not do anything
        """
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
            self.nav = Nav(data["nav"])
        if "fuel" in data:
            self.fuel = Fuel(data["fuel"]["current"], data["fuel"]["capacity"])
        if "cargo" in data:
            self.cargo = Cargo(data["cargo"])

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
            data={"flightMode": new_flight_mode},
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update({"nav": j["data"]})

    def dock(self):
        j = self.post("dock")
        self.update(j["data"])

    def orbit(self):
        j = self.post("orbit")
        self.update(j["data"])

    def extract(self):
        j = self.post("extract")
        self.update(j["data"])
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])
        return Item(
            j["data"]["extraction"]["yield"]["symbol"],
            j["data"]["extraction"]["yield"]["units"],
            "",
        )

    def refuel(self):
        j = self.post("refuel")
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
        j = self.get("cooldown")
        self.reactor.cooldown = parse_time(j["data"]["expiration"])

    def install_mount(self):
        j = self.post("mounts/install")
        self.update(j["data"])
        return MarketTransaction(j["data"]["transaction"])

    def remove_mount(self):
        j = self.post("mounts/remove")
        self.update(j["data"])
        return MarketTransaction(j["data"]["transaction"])

    @staticmethod
    def all(session, page: int = 1) -> (str, int):
        r = session.get(session.base_url + "my/ships?limit=20&page=" + str(page))
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        ships = []
        for ship in j["data"]:
            s = Ship(ship["symbol"], session, ship)
            ships.append(s)
        return ships, r.json()["meta"]["total"]
