from autotraders.util import parse_time


class ShipyardTransaction:
    def __init__(self, data):
        self.credits = data["price"]
        self.waypoint_symbol = data["waypointSymbol"]
        self.ship_symbol = data["shipSymbol"]
        self.agent_symbol = data["agent_symbol"]
        self.timestamp = parse_time(data["timestamp"])
