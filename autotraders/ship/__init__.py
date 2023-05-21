import asyncio

from autotraders.contract import Contract
from autotraders.session import AutoTradersSession
from autotraders.ship.ship_components import Frame, Reactor, Engine, Module, Mount
from autotraders.ship.survey import Survey
from autotraders.util import parse_time
from autotraders.waypoint import Waypoint


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
        self.destination = data["destination"]
        self.departure = data["departure"]["symbol"]
        self.moving = self.destination == self.departure
        if self.moving:
            self.depature_time = parse_time(data["departure_time"])
            self.arrival = parse_time(data["arrival"])


class Nav:
    def __init__(self, data):
        self.status = data["status"]
        self.location = data["waypointSymbol"]
        self.flight_mode = data["flightMode"]
        self.route = Route(data["route"])


class Crew:
    def __init__(self, data):
        self.current = data["current"]
        self.required = data["required"]
        self.capacity = data["capacity"]
        self.morale = data["morale"]
        self.wages = data["wages"]


class Ship:
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.symbol = symbol
        self.session = session
        self.frame = None
        self.reactor = None
        self.engine = None
        self.modules = None
        self.mounts = None
        self.crew = None
        if update:
            self.update()

    def update(self, data: dict = None, hard=False):
        if data is None:
            r = self.session.get(self.session.base_url + "my/ships/" + self.symbol)
            if "error" in r.json():
                raise IOError(r.json()["error"]["message"])
            data = r.json()["data"]
        if self.crew is None and not hard:
            self.crew = Crew(data["crew"])
        if self.frame is None and not hard:
            self.frame = Frame(data["frame"])
        if self.reactor is None and not hard:
            self.reactor = Reactor(data["reactor"])
        if self.engine is None and not hard:
            self.engine = Engine(data["engine"])
        if self.modules is None and not hard:
            self.modules = [Module(d) for d in data["modules"]]
        if self.mounts is None and not hard:
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
        r = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/navigate",
            data={"waypointSymbol": waypoint},
        )
        j = r.json()
        if "error" in j:
            raise j["error"]["message"]
        await asyncio.sleep(5)
        self.update()
        while self.nav.status == "IN_TRANSIT":
            await asyncio.sleep(5)
            self.update()

    def navigate(self, waypoint):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function exits immediately, and does not wait the ship to arrive.
            :raise:
                IOError: if a server error occurs
        """
        r = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/navigate",
            data={"waypointSymbol": waypoint},
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def patch_navigation(self, new_flight_mode):
        r = self.session.patch(
            self.session.base_url + "my/ships/" + self.symbol + "/nav",
            data={  # TODO: Test
                "flightMode": new_flight_mode
            }
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update({"nav": j["data"]})

    def dock(self):
        r = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/dock"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def orbit(self):
        r = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/orbit"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def extract(self):
        r = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/extract"
        )
        j = r.json()
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
        r = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/refuel"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def sell(self, cargo_symbol, quantity):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/sell",
            data={"symbol": cargo_symbol, "units": quantity},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def buy(self, cargo_symbol, quantity):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/purchase",
            data={"symbol": cargo_symbol, "units": quantity},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def transfer(self, destination: str, cargo_symbol: str, quantity: int):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/transfer",
            data={
                "tradeSymbol": cargo_symbol,
                "units": quantity,
                "shipSymbol": destination,
            },
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def jump(self, destination: str):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/jump",
            data={
                "systemSymbol": destination,
            },
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])

    def warp(self, destination: str):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/warp",
            data={
                "waypointSymbol": destination,
            },
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def jettison(self, cargo_symbol: str, quantity: int):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/jettison",
            data={"symbol": cargo_symbol, "units": quantity},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def refine(self, output_symbol: str):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/refine",
            data={"produce": output_symbol},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def chart(self):
        """
        Charts the current waypoint
        :return: The info about the waypoint that has been charted
        """
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/chart"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        w = Waypoint(j["data"]["waypoint"]["symbol"], self.session, False)
        w.update(j["data"]["waypoint"])
        self.update()
        return w

    def survey(self):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/survey"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        surveys = []
        for s in j["data"]["surveys"]:
            surveys.append(Survey(s))
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return surveys

    def scan_systems(self):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/scan/systems"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        raise NotImplementedError

    def scan_waypoints(self):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/scan/waypoints"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        waypoints = []
        for waypoint in j["systems"]:
            s = Waypoint(waypoint["symbol"], self.session, False)
            s.update(waypoint)
            waypoints.append(s)
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return waypoints

    def scan_ships(self):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/scan/ships"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        ships = []
        for ship in j["data"]["ships"]:
            s = Ship(ship["data"], self.session, False)
            s.update(ship)
            ships.append(s)
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])
        return ships

    def update_ship_cooldown(self):
        j = self.session.post(
            self.session.base_url + "my/ships/" + self.symbol + "/cooldown"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
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
