from typing import Optional

from pydantic import Field

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.item import Item


class TradeGood(Item):
    trade_volume: int = Field(alias="tradeVolume")
    supply: str
    purchase_price: int = Field(alias="purchasePrice")
    sell_price: int = Field(alias="sellPrice")


class Marketplace(WaypointType):
    imports: list[str]
    exports: list[str]
    exchange: list[str]
    trade_goods: Optional[list[TradeGood]]

    def __init__(self, waypoint: str, session: AutoTradersSession, data=None):
        super().__init__(waypoint, "market", session, data)

    def update(self, data: dict = None):
        if data is None:
            data = self.get()["data"]
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
                self.trade_goods.append(TradeGood(**i))
