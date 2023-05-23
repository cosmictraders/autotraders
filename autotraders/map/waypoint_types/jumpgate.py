from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession


class JumpGate(WaypointType):
    def __init__(self, waypoint: str, session: AutoTradersSession, update=True):
        self.faction_symbol = ""
        self.jump_range = None
        super().__init__(waypoint, "jump-gate", session, update)

    def update(self, data: dict = None):
        if data is None:
            data = self.get()["data"]
        self.jump_range = data["jumpRange"]
        if "factionSymbol" in data:
            self.faction_symbol = data["factionSymbol"]
