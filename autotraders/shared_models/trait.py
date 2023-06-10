class Trait:
    def __init__(self, data):
        self.symbol: str = data["symbol"]
        self.name: str = data["name"]
        self.description: str = data["description"]

    def __str__(self):
        return self.name
