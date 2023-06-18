from autotraders import AutoTradersSession
from autotraders.shared_models.item import Item
from autotraders.space_traders_entity import SpaceTradersEntity


class Cargo(SpaceTradersEntity):
    capacity: int
    current: int
    inventory: list[Item]

    def __init__(self, symbol, session: AutoTradersSession, data=None):
        super().__init__(session, "my/ships/" + symbol, data)

    def update(self, data: dict = None) -> None:
        if data is None:
            data = self.get("cargo")["data"]
        self.capacity = data["capacity"]
        inventory = data["inventory"]
        self.inventory = []
        self.current = 0
        for symbol in inventory:
            self.inventory.append(
                Item(symbol["symbol"], symbol["units"], symbol["description"])
            )
            self.current += symbol["units"]
