from datetime import datetime
from typing import Optional

from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.session import AutoTradersSession
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.util import parse_time


class Deliver:
    def __init__(self, data):
        self.trade_symbol = MapSymbol(data["tradeSymbol"])
        self.destination_symbol = MapSymbol(data["destinationSymbol"])
        self.units_required = data["unitsRequired"]
        self.units_fulfilled = data["unitsFulfilled"]


class Contract(SpaceTradersEntity):
    def __init__(self, contract_id: str, session: AutoTradersSession, data=None):
        self.contract_data = None
        self.accepted: Optional[bool] = None
        self.fulfilled: Optional[bool] = None
        self.deadline: Optional[datetime] = None
        self.accept_deadline: Optional[datetime] = None
        self.contract_type = None
        self.on_fulfilled: Optional[str] = None
        self.on_accepted: Optional[str] = None
        self.contract_id: str = contract_id
        super().__init__(session, "my/contracts/" + self.contract_id, data)

    def update(self, data=None):
        if data is None:
            data = self.get()["data"]
        self.on_accepted = data["terms"]["payment"]["onAccepted"]
        self.on_fulfilled = data["terms"]["payment"]["onFulfilled"]
        self.accepted = data["accepted"]
        self.fulfilled = data["fulfilled"]
        self.deadline = parse_time(data["terms"]["deadline"])
        self.accept_deadline = parse_time(data["deadlineToAccept"])
        self.contract_type = data["type"]
        if "deliver" in data["terms"]:
            self.contract_data = [Deliver(d) for d in data["terms"]["deliver"]]

    def accept(self):
        j = self.post("accept")
        self.update(j["data"]["contract"])

    def deliver(self, symbol, cargo_symbol, amount):
        j = self.post(
            "deliver",
            data={"shipSymbol": symbol, "tradeSymbol": cargo_symbol, "units": amount},
        )
        self.update(j["data"]["contract"])

    @staticmethod
    def negotiate(ship_symbol, session):
        j = session.post(
            session.base_url + "my/ships/" + ship_symbol + "/negotiate/contract"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        c = Contract(j["data"]["contract"]["id"], session, j["data"]["contract"])
        return c

    def fulfill(self):
        j = self.post("fulfill")
        self.update(j["data"]["contract"])

    @staticmethod
    def all(session, page: int = 1):
        r = session.get(session.base_url + "my/contracts?limit=20&page=" + str(page))
        j = r.json()
        contracts = []
        for contract in j["data"]:
            c = Contract(contract["id"], session, contract)
            contracts.append(c)
        return contracts, r.json()["meta"]["total"]
