from datetime import datetime, timezone

from autotraders import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship.states import NavState, FlightMode
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.time import parse_time


class Route:
    def __init__(self, data):
        self.destination = MapSymbol(data["destination"]["symbol"])
        self.departure = MapSymbol(data["departure"]["symbol"])
        self.departure_time = parse_time(data["departureTime"])
        self.arrival = parse_time(data["arrival"])
        self.moving = self.arrival > datetime.now(timezone.utc)


class Nav(SpaceTradersEntity):
    status: str
    location: MapSymbol
    flight_mode: str
    route: Route
    moving: bool

    def __init__(self, symbol, session: AutoTradersSession, data=None):
        super().__init__(session, "my/ships/" + symbol, data)

    def update(self, data: dict = None) -> None:
        if data is None:
            data = self.get("nav")["data"]
        self.status = NavState(data["status"])
        self.location = MapSymbol(data["waypointSymbol"])
        self.flight_mode = FlightMode(data["flightMode"])
        self.route = Route(data["route"])
        self.moving = self.route.moving
