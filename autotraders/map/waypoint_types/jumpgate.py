from typing import Optional

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.system_symbol import SystemSymbol


class JumpGate(WaypointType):
    connections: list[SystemSymbol]

    def __init__(
        self, waypoint: str, session: AutoTradersSession, data: Optional[dict] = None
    ):
        super().__init__(waypoint, "jump-gate", session, data)

    def update(self, data: Optional[dict] = None):
        if data is None:
            data = self.get()["data"]
        self.connections = [
            SystemSymbol(connection) for connection in data["connections"]
        ]
