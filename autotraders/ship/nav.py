from datetime import datetime, timezone
from typing import Union

from autotraders import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship import Fuel, Cooldown
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
    symbol: str
    status: str
    location: MapSymbol
    flight_mode: str
    route: Route
    moving: bool

    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.symbol = symbol
        super().__init__(session, "my/ships/" + symbol, data)

    def update(self, data: dict = None) -> None:
        data = super()._update(data, "nav")

        self.status = NavState(data["status"])
        self.location = MapSymbol(data["waypointSymbol"])
        self.flight_mode = FlightMode(data["flightMode"])
        self.route = Route(data["route"])
        self.moving = self.route.moving

    def orbit(self):
        j = self.post("orbit")
        self.update(j["data"]["nav"])

    def dock(self):
        j = self.post("dock")
        self.update(j["data"]["nav"])

    def navigate(self, destination: Union[str, MapSymbol]):
        j = self.post(
            "warp",
            data={
                "waypointSymbol": str(destination),
            },
        )
        self.update(j["data"]["nav"])
        return Fuel(**j["data"]["fuel"])

    def jump(self, destination: Union[str, MapSymbol]):
        j = self.post(
            "jump",
            data={
                "systemSymbol": str(destination),
            },
        )
        self.update(j["data"]["nav"])
        return Cooldown(self.symbol, self.session, j["data"]["cooldown"])

    def warp(self, destination: Union[str, MapSymbol]):
        j = self.post(
            "warp",
            data={
                "waypointSymbol": str(destination),
            },
        )
        self.update(j["data"]["nav"])
        return Fuel(**j["data"]["fuel"])

    def patch_flight_mode(self, new_flight_mode: Union[str, FlightMode]):
        j = self.patch(
            "nav",
            data={
                "flightMode": str(new_flight_mode),
            },
        )
        self.update(j["data"])
