from enum import Enum

from autotraders.shared_models.item import Item
from autotraders.shared_models.waypoint_symbol import WaypointSymbol
from autotraders.time import parse_time


class ShipyardTransaction:
    def __init__(self, data):
        if "price" in data:
            self.credits: int = data["price"]
        else:
            self.credits: int = data["totalPrice"]
        self.waypoint_symbol: WaypointSymbol = WaypointSymbol(data["waypointSymbol"])
        self.ship_symbol: str = data["shipSymbol"]
        if "agentSymbol" in data:
            self.agent_symbol: str = data["agentSymbol"]
        self.timestamp = parse_time(data["timestamp"])


class TransactionType(str, Enum):
    PURCHASE = "PURCHASE"
    SELL = "SELL"


class MarketTransaction:
    def __init__(self, data: dict):
        self.waypoint_symbol: WaypointSymbol = WaypointSymbol(data["waypointSymbol"])
        self.ship_symbol: str = data["shipSymbol"]
        self.transaction_type: TransactionType = TransactionType(data["type"])
        self.item = Item(symbol=data["tradeSymbol"], quantity=data["units"])
        self.price_per_unit: int = data["pricePerUnit"]
        self.total_price: int = data["totalPrice"]
        self.timestamp = parse_time(data["timestamp"])
