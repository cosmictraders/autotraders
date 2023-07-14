class ShipSymbol:
    def __init__(self, symbol):
        split = self.symbol.split("-")
        self.agent_name = split[0]
        self.number = split[1]

    def __str__(self):
        return self.agent_name + "-" + self.number

    def __hash__(self):
        return self.agent_name + "-" + str(self.number)

    def __eq__(self, other):
        return str(self) == str(other)
