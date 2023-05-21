class Trait:
    def __init__(self, data):
        self.symbol = data["symbol"]
        self.name = data["name"]
        self.description = data["description"]

    def __str__(self):
        return self.name
