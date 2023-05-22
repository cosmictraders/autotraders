from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession


class TradeGood:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.trade_volume = data["tradeVolume"]
        self.supply = data["supply"]
        self.purchase_price = data["purchasePrice"]
        self.sell_price = data["sellPrice"]


class Marketplace(WaypointType):
    def __init__(self, waypoint: str, session: AutoTradersSession, update=True):
        super().__init__(waypoint, "market", session, update)
        self.imports = None
        self.exports = None
        self.exchange = None
        self.trade_goods = None

    def update(self, data: dict = None):
        if data is None:
            data = self.session.get(
                self.session.base_url
                + "systems/"
                + self.location.system
                + "/waypoints/"
                + self.location.waypoint
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
