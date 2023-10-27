from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class SizeEnum(str, Enum):
    SMALL = "SMALL"
    MODERATE = "MODERATE"
    LARGE = "LARGE"


class Survey(BaseModel):
    signature: str
    symbol: str
    deposits: list[dict[str, str]]
    expiration: datetime
    size: SizeEnum
