import asyncio


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


class Frame:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.name = data["name"]
        self.description = data["description"]
        self.module_slots = data["moduleSlots"]
        self.mounting_points = data["mountingPoints"]
        self.condition = data["condition"]


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
        if "frame" in data:
            self.frame = Frame(data["frame"])
        if "nav" in data:
            self.status = data["nav"]["status"]
            self.location = data["nav"]["waypointSymbol"]
        if "fuel" in data:
            self.fuel = Fuel(data["fuel"]["current"], data["fuel"]["capacity"])
        if "cargo" in data:
            self.cargo = Cargo(data["cargo"])

    async def move_async(self, waypoint):
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

    def move(self, waypoint):
        r = self.session.post(
            "https://api.spacetraders.io/v2/my/ships/" + self.symbol + "/navigate",
            data={"waypointSymbol": waypoint},
        )
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

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
