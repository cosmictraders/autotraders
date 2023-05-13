import requests

from autotraders.util import parse_time


class Deliver:
    def __init__(self, data):
        self.trade_symbol = data["tradeSymbol"]
        self.destination_symbol = data["destinationSymbol"]
        self.units_required = data["unitsRequired"]
        self.units_fulfilled = data["unitsFulfilled"]


class Contract:
    def __init__(self, contract_id, session: requests.Session, update=True):
        self.contract_id = contract_id
        self.session = session
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get(
                "https://api.spacetraders.io/v2/my/contracts/" + self.contract_id
            )
            data = r.json()["data"]
        self.on_accepted = data["terms"]["payment"]["onAccepted"]
        self.on_fulfilled = data["terms"]["payment"]["onFulfilled"]
        self.accepted = data["accepted"]
        self.fulfilled = data["fulfilled"]
        self.deadline = parse_time(data["terms"]["deadline"])
        if "deliver" in data:
            self.contract_type = "deliver"
            self.contract_data = [Deliver(d) for d in data["deliver"]]

    def accept(self):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/contracts/"
            + self.contract_id
            + "/accept"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])

    def deliver(self, symbol, cargo_symbol, amount):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/contracts/"
            + self.contract_id
            + "/deliver",
            data={"shipSymbol": symbol, "tradeSymbol": cargo_symbol, "units": amount},
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])
        self.update()

    def fulfill(self):
        j = self.session.post(
            "https://api.spacetraders.io/v2/my/contracts/"
            + self.contract_id
            + "/fulfill"
        ).json()
        if "error" in j:
            raise IOError(j["error"]["message"])


def get_all_contracts(session):
    r = session.get("https://api.spacetraders.io/v2/my/contracts")
    j = r.json()
    contracts = []
    for contract in j["data"]:
        c = Contract(contract["id"], session, False)
        c.update(contract)
        contracts.append(c)
    return contracts
