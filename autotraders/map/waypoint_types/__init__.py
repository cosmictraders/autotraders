from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol


class WaypointType(SpaceTradersEntity):
    def __init__(
        self, waypoint: str, trait: str, session: AutoTradersSession, data=None
    ):
        self.location: MapSymbol = MapSymbol(waypoint)
        super().__init__(
            session,
            "systems/"
            + self.location.system
            + "/waypoints/"
            + self.location.waypoint
            + "/"
            + trait
            + "/",
            data,
        )
