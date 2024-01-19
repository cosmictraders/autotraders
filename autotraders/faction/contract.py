from datetime import datetime

from autotraders.agent import Agent
from autotraders.error import SpaceTradersException
from autotraders.paginated_list import PaginatedList
from autotraders.session import AutoTradersSession
from autotraders.shared_models.item import Item
from autotraders.shared_models.item_progress import ItemProgress
from autotraders.shared_models.waypoint_symbol import WaypointSymbol
from autotraders.ship import Cargo
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.time import parse_time


class Deliver:
    def __init__(self, data):
        self.item = ItemProgress(
            symbol=data["tradeSymbol"],
            required=data["unitsRequired"],
            fulfilled=data["unitsFulfilled"],
        )
        self.destination_symbol = WaypointSymbol(data["destinationSymbol"])


class Contract(SpaceTradersEntity):
    accepted: bool
    fulfilled: bool
    deadline: datetime
    accept_deadline: datetime
    on_fulfilled: str
    on_accepted: str
    contract_id: str

    def __init__(self, contract_id: str, session: AutoTradersSession, data=None):
        self.contract_data = None
        self.contract_type = None
        self.contract_id: str = contract_id
        super().__init__(session, "my/contracts/" + self.contract_id, data)

    def update(self, data=None):
        data = super()._update(data)
        mappings = {"accepted": {}, "fulfilled": {}, "contract_type": {"alias": "type"}}
        super().update_attr(mappings, data)
        self.on_accepted = data["terms"]["payment"]["onAccepted"]
        self.on_fulfilled = data["terms"]["payment"]["onFulfilled"]
        self.deadline = parse_time(data["terms"]["deadline"])
        self.accept_deadline = parse_time(data["deadlineToAccept"])
        if "deliver" in data["terms"]:
            self.contract_data = [Deliver(d) for d in data["terms"]["deliver"]]

    def accept(self):
        j = self.post("accept")
        self.update(j["data"]["contract"])
        return Agent(self.session, data=j["data"]["agent"])

    def deliver(self, symbol, cargo_symbol, amount):
        j = self.post(
            "deliver",
            data={"shipSymbol": symbol, "tradeSymbol": cargo_symbol, "units": amount},
        )
        self.update(j["data"]["contract"])
        return Cargo(symbol, self.session, j["data"]["cargo"])

    @staticmethod
    def negotiate(ship_symbol, session):
        r = session.post("my/ships/" + ship_symbol + "/negotiate/contract")
        j = r.json()
        if "error" in j:
            raise SpaceTradersException(
                j["error"], r.url, r.status_code, r.request.headers, r.headers
            )
        c = Contract(j["data"]["contract"]["id"], session, j["data"]["contract"])
        return c

    def fulfill(self):
        j = self.post("fulfill")
        self.update(j["data"]["contract"])
        return Agent(self.session, data=j["data"]["agent"])

    @staticmethod
    def all(session, page: int = 1):
        def paginated_func(p, num_per_page):
            r = session.get(
                "my/contracts?limit=" + str(num_per_page) + "&page=" + str(p)
            )
            j = r.json()
            if "error" in j:
                raise SpaceTradersException(
                    j["error"], r.url, r.status_code, r.request.headers, r.headers
                )
            contracts = []
            for contract in j["data"]:
                c = Contract(contract["id"], session, contract)
                contracts.append(c)
            return contracts, r.json()["meta"]["total"]

        return PaginatedList(paginated_func, page)
