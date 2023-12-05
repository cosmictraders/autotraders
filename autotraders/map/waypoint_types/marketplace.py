from enum import Enum
from typing import Optional

from pydantic import Field

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.item import Item
from autotraders.shared_models.transaction import MarketTransaction


class GoodType(str, Enum):
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    EXCHANGE = "EXCHANGE"


class Supply(str, Enum):
    SCARCE = "SCARCE"
    LIMITED = "LIMITED"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    ABUNDANT = "ABUNDANT"


class Activity(str, Enum):
    WEAK = "WEAK"
    GROWING = "GROWING"
    STRONG = "STRONG"
    RESTRICTED = "RESTRICTED"

class TradeGood(Item):
    good_type: GoodType = Field(alias="type")
    trade_volume: int = Field(alias="tradeVolume")
    supply: Supply
    purchase_price: int = Field(alias="purchasePrice")
    sell_price: int = Field(alias="sellPrice")
    activity: Optional[Activity] = None


class Marketplace(WaypointType):
    imports: list[str]
    exports: list[str]
    exchange: list[str]
    trade_goods: Optional[list[TradeGood]]

    def __init__(
        self, waypoint: str, session: AutoTradersSession, data: Optional[dict] = None
    ):
        super().__init__(waypoint, "market", session, data)

    def update(self, data: Optional[dict] = None):
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
        self.transactions = None
        if "transactions" in data:
            self.transactions = []
            for i in data["transactions"]:
                self.transactions.append(MarketTransaction(i))
