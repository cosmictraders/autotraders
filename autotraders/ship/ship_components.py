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