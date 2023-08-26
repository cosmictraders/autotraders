from datetime import datetime
from enum import Enum

from autotraders.time import parse_time


class SizeEnum(str, Enum):
    SMALL = "SMALL"
    MODERATE = "MODERATE"
    LARGE = "LARGE"


class Survey:
    signature: str
    symbol: str
    deposits: list[dict[str, str]]
    expiration: datetime
    size: SizeEnum
