import asyncio

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
        self.inventory = {}
        self.current = 0
        for symbol in inventory:
            self.inventory[symbol["symbol"]] = symbol["units"]
            self.current += symbol["units"]


class Route:
    def __init__(self, data):
        self.destination = MapSymbol(data["destination"]["symbol"])
        self.departure = MapSymbol(data["departure"]["symbol"])
        self.moving = self.destination != self.departure
        if self.moving:
            self.departure_time = parse_time(data["departureTime"])
            self.arrival = parse_time(data["arrival"])


class Nav:
    def __init__(self, data):
        self.status = data["status"]
        self.location = MapSymbol(data["waypointSymbol"])
        self.flight_mode = data["flightMode"]
        self.route = Route(data["route"])


class Crew:
    def __init__(self, data):
        self.current = data["current"]
        self.required = data["required"]
        self.capacity = data["capacity"]
        self.morale = data["morale"]
        self.wages = data["wages"]


class Ship(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.cargo = None
        self.fuel = None
        self.nav = None
        self.symbol = symbol
        self.frame = None
        self.reactor = None
        self.engine = None
        self.modules = None
        self.mounts = None
        self.crew = None
        super().__init__(
            session, update, session.base_url + "my/ships/" + self.symbol + "/"
        )

    def update(self, data: dict = None, hard=False):
        if data is None:
            data = self.get()["data"]

        def go_for_update(d, s):
            return s in data and (d is None or hard)

        if go_for_update(self.crew, "crew"):
            self.crew = Crew(data["crew"])
        if go_for_update(self.frame, "frame"):
            self.frame = Frame(data["frame"])
        if go_for_update(self.reactor, "reactor"):
            self.reactor = Reactor(data["reactor"])
        if go_for_update(self.engine, "engine"):
            self.engine = Engine(data["engine"])
        if go_for_update(self.modules, "modules"):
            self.modules = [Module(d) for d in data["modules"]]
        if go_for_update(self.mounts, "mounts"):
            self.mounts = [Mount(d) for d in data["mounts"]]
        if "nav" in data:
            self.nav = Nav(data["nav"])
        if "fuel" in data:
            self.fuel = Fuel(data["fuel"]["current"], data["fuel"]["capacity"])
        if "cargo" in data:
            self.cargo = Cargo(data["cargo"])

    async def navigate_async(self, waypoint):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function waits for the ship to arrive.
            :raise:
                IOError: if a server error occurs
        """
        j = self.post("navigate", data={"waypointSymbol": waypoint})
        self.update(j["data"])
        while self.nav.status == "IN_TRANSIT":
            await asyncio.sleep(5)
            self.update()

    def navigate(self, waypoint):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function exits immediately, and does not wait the ship to arrive.
            :raise:
                IOError: if a server error occurs
        """
        j = self.post("navigate", data={"waypointSymbol": waypoint})
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
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/extract"
        ).json()
        if "error" in j:
            if j["error"]["code"] == 4000:
                raise IOError(
                    "Ship is still in cooldown, "
                    + str(j["error"]["data"]["cooldown"]["remainingSeconds"])
                    + " seconds out of "
                    + str(j["error"]["data"]["cooldown"]["totalSeconds"])
                    + " seconds remaining"
                )
            else:
                raise IOError(j["error"]["message"])
        self.update(j["data"])
        self.reactor.cooldown = parse_time(j["data"]["cooldown"]["expiration"])

    def refuel(self):
        j = self.post("refuel")
        self.update(j["data"])

    def sell(self, cargo_symbol, quantity):
        j = self.post("sell", data={"symbol": cargo_symbol, "units": quantity})
        self.update(j["data"])

    def buy(self, cargo_symbol, quantity):
        j = self.post("purchase", data={"symbol": cargo_symbol, "units": quantity})
        self.update(j["data"])

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

    def jump(self, destination: str):
        j = self.post(
            "jump",
            data={
                "systemSymbol": destination,
            },
        )
        self.update(j["data"])
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])

    def warp(self, destination: str):
        j = self.post(
            "warp",
            data={
                "waypointSymbol": destination,
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
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])

    def chart(self) -> Waypoint:
        """
        Charts the current waypoint
        :return: The info about the waypoint that has been charted
        """
        j = self.post("chart")
        w = Waypoint(j["data"]["waypoint"]["symbol"], self.session, False)
        w.update(j["data"]["waypoint"])
        return w

    def survey(self) -> list[Survey]:
        j = self.post("survey")
        surveys = []
        for s in j["data"]["surveys"]:
            surveys.append(Survey(s))
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return surveys

    def scan_systems(self):
        j = self.post("scan/systems")
        systems = []
        for system in j["systems"]:
            s = System(system["symbol"], self.session, False)
            s.update(system)
            systems.append(s)
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return systems

    def scan_waypoints(self):
        j = self.post("scan/waypoints")
        waypoints = []
        for waypoint in j["waypoints"]:
            s = Waypoint(waypoint["symbol"], self.session, False)
            s.update(waypoint)
            waypoints.append(s)
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return waypoints

    def scan_ships(self):
        j = self.post("scan/ships")
        ships = []
        for ship in j["data"]["ships"]:
            s = Ship(ship["data"], self.session, False)
            s.update(ship)
            ships.append(s)
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return ships

    def update_ship_cooldown(self):
        j = self.get("cooldown")
        self.reactor.cooldown = parse_time(j["data"]["expiration"])

    @staticmethod
    def all(session, page: int = 1):
        r = session.get(session.base_url + "my/ships?page=" + str(page))
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        ships = []
        for ship in j["data"]:
            s = Ship(ship["symbol"], session, False)
            s.update(ship)
            ships.append(s)
        return ships, r.json()["meta"]["total"]


def get_all_ships(session):
    return Ship.all(session)[0]
