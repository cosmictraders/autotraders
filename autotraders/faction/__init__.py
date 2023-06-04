from typing import Optional

from autotraders.paginated_list import PaginatedList
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.shared_models.trait import Trait


class Faction(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.is_recruiting: Optional[bool] = None
        self.traits: Optional[list[Trait]] = None
        self.headquarters: Optional[MapSymbol] = None
        self.description: Optional[str] = None
        self.name: Optional[str] = None
        self.symbol: str = symbol
        super().__init__(session, "factions/" + self.symbol, data)

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
        self.name = data["name"]
        self.description = data["description"]
        self.headquarters = MapSymbol(data["headquarters"])
        self.traits = []
        for trait in data["traits"]:
            self.traits.append(Trait(trait))
        self.is_recruiting = data["isRecruiting"]

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get(
                session.base_url
                + "my/contracts?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            r = session.get(
                session.base_url
                + "factions?limit="
                + str(num_per_page)
                + "&page="
                + str(p)
            )
            j = r.json()
            if "error" in j:
                raise IOError(j["error"]["message"])
            factions = []
            for f in j["data"]:
                faction = Faction(f["symbol"], session, f)
                factions.append(faction)
            return factions, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)


def get_all_factions(session):
    return Faction.all(session)
