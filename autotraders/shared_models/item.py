class Item:
    def __init__(self, symbol, quantity, description):
        self.symbol: str = symbol
        self.quantity: int = quantity
        self.description: str = description

    def __eq__(self, other):
        return self.symbol == other.symbol and self.quantity == other.quantity

    def __hash__(self):
        return hash(self.symbol + "-" + str(self.quantity))
