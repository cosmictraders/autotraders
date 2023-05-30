from typing import Optional

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.item import Item


class TradeGood(Item):
    def __init__(self, data):
        super().__init__(data["symbol"], data["supply"], data["description"])
        self.trade_volume: int = data["tradeVolume"]
        self.supply: str = data["supply"]
        self.purchase_price: int = data["purchasePrice"]
        self.sell_price: int = data["sellPrice"]


class Marketplace(WaypointType):
    def __init__(self, waypoint: str, session: AutoTradersSession, update=True):
        self.imports: Optional[list[str]] = None
        self.exports: Optional[list[str]] = None
        self.exchange: Optional[list[str]] = None
        self.trade_goods: Optional[list[TradeGood]] = None
        super().__init__(waypoint, "market", session, update)

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
