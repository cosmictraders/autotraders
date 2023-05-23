from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol


class WaypointType(SpaceTradersEntity):
    def __init__(
        self, waypoint: str, trait: str, session: AutoTradersSession, update=True
    ):
        self.location = MapSymbol(waypoint)
        super().__init__(
            session,
            update,
            session.base_url
            + "systems/"
            + self.location.system
            + "/waypoints/"
            + self.location.waypoint
            + "/"
            + trait
            + "/",
        )
