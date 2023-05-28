from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.util import parse_time


class ShipyardTransaction:
    def __init__(self, data):
        self.credits = data["price"]
        self.waypoint_symbol = MapSymbol(data["waypointSymbol"])
        self.ship_symbol = data["shipSymbol"]
        self.agent_symbol = data["agent_symbol"]
        self.timestamp = parse_time(data["timestamp"])


class MarketTransaction:
    def __init__(self, data):
        self.waypoint_symbol = MapSymbol(data["waypointSymbol"])
        self.ship_symbol = data["shipSymbol"]

        self.trade_symbol = data["tradeSymbol"]
        self.transaction_type = data["type"]
        self.units = data["units"]
        self.price_per_unit = data["pricePerUnit"]
        self.total_price = data["totalPrice"]
        self.timestamp = parse_time(data["timestamp"])
