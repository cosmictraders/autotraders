import requests


class TradeGood:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.trade_volume = data["tradeVolume"]
        self.supply = data["supply"]
        self.purchase_price = data["purchasePrice"]
        self.sell_price = data["sellPrice"]


class Marketplace:
    def __init__(self, waypoint: str, session: requests.Session, update=True):
        self.location = waypoint
        self.session = session
        if update:
            self.update()

    def update(self, data: dict = None):
        if data is None:
            split = self.location.split("-")
            system_symbol = split[0] + "-" + split[1]
            waypoint_symbol = self.location
            data = self.session.get(
                "https://api.spacetraders.io/v2/systems/"
                + system_symbol
                + "/waypoints/"
                + waypoint_symbol
                + "/market"
            ).json()["data"]
        self.imports = []
        for i in data["imports"]:
            self.imports.append(i["symbol"])
        self.exports = []
        for i in data["exports"]:
            self.exports.append(i["symbol"])
        self.exchange = []
        for i in data["exchange"]:
            self.exchange.append(i["symbol"])

        self.trade_goods = None
        if "tradeGoods" in data:
            self.trade_goods = []
            for i in data["tradeGoods"]:
                self.trade_goods.append(TradeGood(i))
