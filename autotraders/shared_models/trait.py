from pydantic import BaseModel


class Trait(BaseModel):
    symbol: str
    name: str
    description: str

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == str(other)

    def __hash__(self):
        return hash(self.symbol)
