class Trait:
    def __init__(self, data):
        self.symbol: str = data["symbol"]
        self.name: str = data["name"]
        self.description: str = data["description"]

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == str(other)

    def __hash__(self):
        return self.symbol
