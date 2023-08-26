from typing import Optional

from pydantic import BaseModel, AliasChoices, Field


class Item(BaseModel):
    symbol: str = Field(validation_alias=AliasChoices("symbol", "tradeSymbol"))
    quantity: int = Field(
        validation_alias=AliasChoices("quantity", "units", "amount", "tradeVolume")
    )
    description: Optional[str] = None

    def __str__(self):
        return self.symbol

    def __eq__(self, other):
        return self.symbol == other.symbol and self.quantity == other.quantity

    def __hash__(self):
        return hash(self.symbol + "-" + str(self.quantity))
