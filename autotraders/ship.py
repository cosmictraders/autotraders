import asyncio

from autotraders.util import parse_time
from autotraders.waypoint import Waypoint


class Fuel:
    def __init__(self, current, total):
        self.current = current
        self.total = total

    def __str__(self):
        print(str(self.current) + "/" + str(self.total))


class Cargo:
    def __init__(self, j):
        self.capacity = j["capacity"]
        inventory = j["inventory"]
        self.inventory = {}
        for symbol in inventory:
            self.inventory[symbol["symbol"]] = symbol["units"]


class Requirements:
    def __init__(self, data):
        self.power = data["power"]
        self.crew = data["crew"]
        self.slots = data["slots"]


class ShipComponent:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.name = data["name"]
        self.description = data["description"]
        if "condition" in data:
            self.condition = data["condition"]
        else:
            self.condition = 100
        self.requirements = Requirements(data["requirements"])


class Frame(ShipComponent):
    def __init__(self, data):
        super().__init__(data)
        self.module_slots = data["moduleSlots"]
        self.mounting_points = data["mountingPoints"]
        self.fuel_capacity = data["fuelCapacity"]


class Reactor(ShipComponent):
    def __init__(self, data):
        super().__init__(data)
        self.power_output = data["powerOutput"]
        self.cooldown = 0


class Engine(ShipComponent):
    def __init__(self, data):
        super().__init__(data)
        self.speed = data["speed"]


class Module(ShipComponent):
    def __init__(self, data):
        super().__init__(data)
        if "capacity" in data:
            self.capacity = data["capacity"]
        if "range" in data:
            self.range = data["range"]


class Mount(ShipComponent):
    def __init__(self, data):
        super().__init__(data)
        if "strength" in data:
            self.strength = data["strength"]
        if "deposits" in data:
            self.deposits = data["deposits"]


class Route:
    def __init__(self, data):
        self.destination = data["destination"]
        self.departure = data["departure"]["symbol"]
        self.moving = self.destination == self.departure
        self.depature_time = parse_time(data["departure_time"])
        self.arrival = parse_time(data["arrival"])


class Nav:
    def __init__(self, data):
        self.status = data["status"]
        self.location = data["waypointSymbol"]
        self.flight_mode = data["flightMode"]
        self.route = Route(data["route"])


class Ship:
    def __init__(self, symbol, session, update=True):
        self.symbol = symbol
        self.session = session
        if update:
            self.update()

    def update(self, data: dict = None):
        if data is None:
            r = self.session.get(
                "https://api.spacetraders.io/v2/my/ships/" + self.symbol
            )
            if "error" in r.json():
                raise IOError(r.json()["error"]["message"])
            data = r.json()["data"]
        self.frame = Frame(data["frame"])
        self.reactor = Reactor(data["reactor"])
        self.engine = Engine(data["engine"])
        self.modules = [Module(d) for d in data["modules"]]
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
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/navigate",
            data={"waypointSymbol": waypoint},
        )
        j = r.json()
        if "error" in j:
            raise j["error"]["message"]
        await asyncio.sleep(5)
        self.update()
        while self.status == "IN_TRANSIT":
            await asyncio.sleep(5)
            self.update()

    def navigate(self, waypoint):
        """Attempts to move ship to the provided waypoint.
        If the request succeeds, this function exits immediately, and does not wait the ship to arrive.
            :raise:
                IOError: if a server error occurs
        """
        r = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/navigate",
            data={"waypointSymbol": waypoint},
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j["data"])

    def patch_navigation(self, new_flight_mode):
        r = self.session.patch(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/nav"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update({"nav": j["data"]})

    def dock(self):
        r = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/dock"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j)

    def orbit(self):
        r = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/orbit"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j)

    def extract(self):
        r = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/extract"
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
        self.update(j)
        self.reactor.cooldown = parse_time(j["cooldown"]["expiration"])

    def refuel(self):
        r = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/refuel"
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update(j)

    def sell(self, cargo_symbol, quantity):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/sell",
            data={"symbol": cargo_symbol, "units": quantity},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def buy(self, cargo_symbol, quantity):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/purchase",
            data={"symbol": cargo_symbol, "units": quantity},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def transfer(self, destination: str, cargo_symbol: str, quantity: int):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/transfer",
            data={
                "tradeSymbol": cargo_symbol,
                "units": quantity,
                "shipSymbol": destination,
            },
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def jump(self, destination: str):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/jump",
            data={
                "systemSymbol": destination,
            },
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def warp(self, destination: str):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/warp",
            data={
                "waypointSymbol": destination,
            },
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def jettison(self, cargo_symbol: str, quantity: int):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/jettison",
            data={"symbol": cargo_symbol, "units": quantity},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def refine(self, output_symbol: str):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/refine",
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
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/chart"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        w = Waypoint(j["data"]["waypoint"]["symbol"], self.session, False)
        w.update(j["data"]["waypoint"])
        self.update()
        return w


def get_all_ships(session):
    r = session.get("https://api.spacetraders.io/v2/my/ships")
    j = r.json()
    if "error" in j:
        raise IOError(j["error"]["message"])
    ships = []
    for ship in j["data"]:
        s = Ship(ship["symbol"], session, False)
        s.update(ship)
        ships.append(s)
    return ships
