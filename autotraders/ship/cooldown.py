from autotraders import AutoTradersSession
from autotraders.space_traders_entity import SpaceTradersEntity
from autotraders.time import parse_time


class Cooldown(SpaceTradersEntity):
    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.symbol = symbol
        super().__init__(session, "my/ships/" + self.symbol + "/cooldown", data)

    def update(self, data: dict = None) -> None:
        if data is None:
            data = self.get()["data"]
        if "expiration" in data:
            self.expiration = parse_time(data["expiration"])
