from autotraders.session import AutoTradersSession
from autotraders.trait import Trait


class Faction:
    def __init__(self, symbol, session: AutoTradersSession, update=True):
        self.symbol = symbol
        self.session = session
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get(self.session.base_url + "factions/" + self.symbol)
            data = r.json()["data"]
        self.name = data["name"]
        self.description = data["description"]
        self.headquarters = data["headquarters"]
        self.traits = []
        for trait in data["traits"]:
            self.traits.append(Trait(trait))

    @staticmethod
    def all(session):
        r = session.get(session.base_url + "factions")
        j = r.json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        factions = []
        for f in j["data"]:
            faction = Faction(f["symbol"], session, False)
            faction.update(f)
            factions.append(faction)
        return factions


def get_all_factions(session):
    return Faction.all(session)
