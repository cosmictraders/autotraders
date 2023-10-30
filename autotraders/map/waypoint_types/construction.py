from typing import Optional

from autotraders.map.waypoint_types import WaypointType
from autotraders.session import AutoTradersSession
from autotraders.shared_models.item_progress import ItemProgress


class Construction(WaypointType):
    is_complete: bool
    materials: list[ItemProgress]

    def __init__(
        self, waypoint: str, session: AutoTradersSession, data: Optional[dict] = None
    ):
        super().__init__(waypoint, "construction", session, data)

    def update(self, data: Optional[dict] = None):
        if data is None:
            data = self.get()["data"]
        self.is_complete = data["isComplete"]
        self.materials = [
            ItemProgress(
                symbol=item["tradeSymbol"],
                required=item["required"],
                fulfilled=item["fulfilled"],
            )
            for item in data["materials"]
        ]

    def supply(self, ship_symbol: str, good: str, quantity: int):
        self.post(
            "supply",
            {"shipSymbol": ship_symbol, "tradeSymbol": good, "units": quantity},
        )
