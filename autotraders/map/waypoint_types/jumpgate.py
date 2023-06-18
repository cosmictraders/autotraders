from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession


class JumpGate(WaypointType):
    faction_symbol: str
    jump_range: int

    def __init__(self, waypoint: str, session: AutoTradersSession, data=None):
        super().__init__(waypoint, "jump-gate", session, data)

    def update(self, data: dict = None):
        if data is None:
            data = self.get()["data"]
        self.jump_range = data["jumpRange"]
        if "factionSymbol" in data:
            self.faction_symbol = data["factionSymbol"]
