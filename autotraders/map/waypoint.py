from typing import Optional, Union

from autotraders.error import SpaceTradersException
from autotraders.paginated_list import PaginatedList
from autotraders.session import AutoTradersSession
from autotraders.shared_models.trait import Trait

from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity


class Waypoint(SpaceTradersEntity):
    waypoint_type: str
    faction: Optional[str]
    traits: Optional[list[Trait]]
    marketplace: Optional[bool]
    shipyard: Optional[bool]
    symbol: MapSymbol
    x: int
    y: int

    def __init__(
        self, symbol: Union[str, MapSymbol], session: AutoTradersSession, data=None
    ):
        self.symbol = MapSymbol(symbol)
        super().__init__(
            session,
            "systems/" + self.symbol.system + "/waypoints/" + self.symbol.waypoint,
            data,
        )

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
        self.waypoint_type = data["type"]
        self.x = data["x"]
        self.y = data["y"]
        if "faction" in data:
            self.faction = data["faction"]["symbol"]
        else:
            self.faction = None
        self.traits = None
        if "traits" in data:
            self.traits = []
            for trait in data["traits"]:
                self.traits.append(Trait(trait))
        if self.traits is not None:
            self.marketplace = (
                len([trait for trait in self.traits if trait.symbol == "MARKETPLACE"])
                > 0
            )
            self.shipyard = (
                len([trait for trait in self.traits if trait.symbol == "SHIPYARD"]) > 0
            )
        else:
            self.marketplace = None
            self.shipyard = None

    def __str__(self):
        return str(self.symbol)

    @staticmethod
    def all(session, system_symbol, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get(
                session.base_url
                + "systems/"
                + system_symbol
                + "/waypoints?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(j["error"], r.status_code)
            waypoints = []
            for w in j["data"]:
                waypoint = Waypoint(w["symbol"], session, w)
                waypoints.append(waypoint)
            return waypoints, j["meta"]["total"]

        return PaginatedList(paginated_func, page)

    def __eq__(self, other):
        return self.symbol == other.symbol
