from autotraders.session import AutoTradersSession


class JumpGate:
    def __init__(self, waypoint: str, session: AutoTradersSession, update=True):
        self.location = waypoint
        self.session = session
        self.faction_symbol = ""
        if update:
            self.update()

    def update(self, data: dict = None):
        if data is None:
            split = self.location.split("-")
            system_symbol = split[0] + "-" + split[1]
            waypoint_symbol = self.location
            data = self.session.get(
                self.session.base_url
                + "systems/"
                + system_symbol
                + "/waypoints/"
                + waypoint_symbol
                + "/jump-gate"
            ).json()["data"]
        self.jump_range = data["jumpRange"]
        if "factionSymbol" in data:
            self.faction_symbol = data["factionSymbol"]
