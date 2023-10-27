from typing import Optional

from autotraders.session import AutoTradersSession
from autotraders.shared_models.waypoint_symbol import WaypointSymbol
from autotraders.space_traders_entity import SpaceTradersEntity


class WaypointType(SpaceTradersEntity):
    def __init__(
        self,
        waypoint: str,
        trait: str,
        session: AutoTradersSession,
        data: Optional[dict] = None,
    ):
        self.location: WaypointSymbol = WaypointSymbol(waypoint)
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
