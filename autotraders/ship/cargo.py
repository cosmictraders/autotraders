from autotraders import AutoTradersSession
from autotraders.shared_models.item import Item
from autotraders.space_traders_entity import SpaceTradersEntity


class Cargo(SpaceTradersEntity):
    capacity: int
    current: int
    inventory: list[Item]

    def __init__(self, symbol, session: AutoTradersSession, data=None):
        self.symbol = symbol
        super().__init__(session, "my/ships/" + symbol + "/cargo/", data)

    def update(self, data: dict = None) -> None:
        data = super()._update(data)
        self.capacity = data["capacity"]
        inventory = data["inventory"]
        self.inventory = []
        self.current = 0
        for item in inventory:
            self.inventory.append(
                Item(
                    symbol=item["symbol"],
                    quantity=item["units"],
                    description=item["description"],
                )
            )
            self.current += item["units"]

    def __getitem__(self, item):
        results = [i for i in self.inventory if i.symbol == item]
        if not any(results):
            raise Exception("No such item found.")
        else:
            return results[0]

    def __iter__(self):
        return iter(self.inventory)
