from autotraders.shared_models.item import Item
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.time import parse_time


class ShipyardTransaction:
    def __init__(self, data):
        if "price" in data:
            self.credits: int = data["price"]
        else:
            self.credits: int = data["totalPrice"]
        self.waypoint_symbol: MapSymbol = MapSymbol(data["waypointSymbol"])
        self.ship_symbol: str = data["shipSymbol"]
        if "agentSymbol" in data:
            self.agent_symbol: str = data["agentSymbol"]
        self.timestamp = parse_time(data["timestamp"])


class MarketTransaction:
    def __init__(self, data):
        self.waypoint_symbol: MapSymbol = MapSymbol(data["waypointSymbol"])
        self.ship_symbol: str = data["shipSymbol"]
        self.transaction_type = data["type"]
        self.item = Item(data["tradeSymbol"], data["units"], None)
        self.price_per_unit = data["pricePerUnit"]
        self.total_price = data["totalPrice"]
        self.timestamp = parse_time(data["timestamp"])
