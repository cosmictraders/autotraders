from datetime import datetime, timezone
from typing import Optional

from autotraders import AutoTradersSession
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.time import parse_time


class Cooldown(SpaceTradersEntity):
    expiration: Optional[datetime]
    active: bool

    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.symbol = symbol
        super().__init__(session, "my/ships/" + self.symbol + "/cooldown", data)

    def update(self, data: Optional[dict] = None) -> None:
        data = super()._update(data)
        if "expiration" in data:
            self.expiration = parse_time(data["expiration"])
            self.active = self.expiration > datetime.now(timezone.utc)
        else:
            self.expiration = None
            self.active = False
