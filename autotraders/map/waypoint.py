from typing import Optional, Union

from autotraders.paginated_list import PaginatedList
from autotraders.session import AutoTradersSession
from autotraders.shared_models.trait import Trait

from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.space_traders_entity import SpaceTradersEntity


class Waypoint(SpaceTradersEntity):
    def __init__(
        self, symbol: Union[str, MapSymbol], session: AutoTradersSession, data=None
    ):
        self.waypoint_type: Optional[str] = None
        self.faction: Optional[str] = None
        self.traits: Optional[list[Trait]] = []
        self.marketplace: Optional[bool] = None
        self.shipyard: Optional[bool] = None
        self.symbol = MapSymbol(symbol)
        self.x: Optional[int] = None
        self.y: Optional[int] = None
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
        self.traits = []
        if "traits" in data:
            for trait in data["traits"]:
                self.traits.append(Trait(trait))
        self.marketplace = (
            len([trait for trait in self.traits if trait.symbol == "MARKETPLACE"]) > 0
        )
        self.shipyard = (
            len([trait for trait in self.traits if trait.symbol == "SHIPYARD"]) > 0
        )

    @staticmethod
    def all(session, system_symbol, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get(
                session.base_url
                + "systems/" + system_symbol + "/waypoints?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            j = r.json()
            if "error" in j:
                raise IOError(j["error"]["message"])
            waypoints = []
            for w in j["data"]:
                waypoint = Waypoint(w["symbol"], session, w)
                waypoints.append(waypoint)
            return waypoints, j["meta"]["total"]

        return PaginatedList(paginated_func, page)

    def __eq__(self, other):
        return self.symbol == other.symbol
