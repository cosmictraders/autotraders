import requests

from autotraders.trait import Trait


class Faction:
    def __init__(self, symbol, session: requests.Session, update=True):
        self.symbol = symbol
        self.session = session
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get(
                "https://api.spacetraders.io/v2/factions/" + self.symbol
            )
            data = r.json()["data"]
        self.name = data["name"]
        self.description = data["description"]
        self.headquarters = data["headquarters"]
        self.traits = []
        for trait in data["traits"]:
            self.traits.append(Trait(trait))


def get_all_factions(session):
    r = session.get("https://api.spacetraders.io/v2/factions")
    j = r.json()
    if "error" in j:
        raise IOError(j["error"]["message"])
    factions = []
    for f in j["data"]:
        faction = Faction(f["symbol"], session, False)
        faction.update(f)
        factions.append(faction)
    return factions
