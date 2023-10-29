from typing import Optional

from autotraders.error import SpaceTradersException
from autotraders.paginated_list import PaginatedList
from autotraders.session import AutoTradersSession
from autotraders.shared_models.trait import Trait
from autotraders.shared_models.system_symbol import SystemSymbol
from autotraders.space_traders_entity import SpaceTradersEntity


class Faction(SpaceTradersEntity):
    is_recruiting: bool
    traits: list[Trait]
    headquarters: Optional[SystemSymbol]
    description: str
    name: str
    symbol: str

    def __init__(
        self, symbol, session: AutoTradersSession, data: Optional[dict] = None
    ):
        self.symbol: str = symbol
        super().__init__(session, "factions/" + self.symbol, data)

    def update(self, data: Optional[dict] = None):
        data = super()._update(data)
        mappings = {
            "name": {},
            "description": {},
            "is_recruiting": {"alias": "isRecruiting"},
        }
        super().update_attr(mappings, data)
        if data["headquarters"] is None or data["headquarters"] == "":
            self.headquarters = None
        else:
            self.headquarters = SystemSymbol(data["headquarters"])
        self.traits = [Trait(**trait) for trait in data["traits"]]

    @staticmethod
    def all(session, page: int = 1) -> PaginatedList:
        def paginated_func(p, num_per_page):
            r = session.get("factions?limit=" + str(num_per_page) + "&page=" + str(p))
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(
                    j["error"], r.url, r.status_code, r.request.headers, r.headers
                )
            factions = []
            for f in j["data"]:
                faction = Faction(f["symbol"], session, f)
                factions.append(faction)
            return factions, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)


def get_all_factions(session):
    return Faction.all(session)
