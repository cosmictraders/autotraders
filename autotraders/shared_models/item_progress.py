from pydantic import BaseModel, AliasChoices, Field


class ItemProgress(BaseModel):
    symbol: str = Field(validation_alias=AliasChoices("symbol", "tradeSymbol"))
    required: int
    fulfilled: int
