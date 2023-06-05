from datetime import datetime, timezone
from typing import Optional

from autotraders import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.util import parse_time


class Route:
    def __init__(self, data):
        self.destination = MapSymbol(data["destination"]["symbol"])
        self.departure = MapSymbol(data["departure"]["symbol"])
        self.departure_time = parse_time(data["departureTime"])
        self.arrival = parse_time(data["arrival"])
        self.moving = self.arrival > datetime.now(timezone.utc)


class Nav(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.status: Optional[str] = None
        self.location: Optional[MapSymbol] = None
        self.flight_mode: Optional[str] = None
        self.route: Optional[Route] = None
        self.moving: Optional[bool] = None
        super().__init__(session, "my/ships/" + symbol, data)

    def update(self, data: dict = None) -> None:
        if data is None:
            data = self.get("nav")["data"]
        self.status = data["status"]
        self.location = MapSymbol(data["waypointSymbol"])
        self.flight_mode = data["flightMode"]
        self.route = Route(data["route"])
        self.moving = self.route.moving
