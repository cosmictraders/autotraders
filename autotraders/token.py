import base64
import json
from enum import Enum

from pydantic import BaseModel


class AlgEnum(str, Enum):
    RS256 = "RS256"


class TypeEnum(str, Enum):
    JWT = "JWT"


class Header(BaseModel):
    alg: AlgEnum
    typ: TypeEnum


class Payload(BaseModel):
    identifier: str
    version: str
    reset_date: str
    iat: int
    sub: str


class JWT(BaseModel):
    header: Header
    payload: Payload
    signature: str


def parse_token(token):
    """Parses the given token as a JWT"""
    split = token.split(".")
    if len(split) != 3:
        raise ValueError("Invalid JWT")
    header = json.loads(base64.b64decode(split[0].encode("ascii")).decode("utf-8"))
    payload = json.loads(
        base64.b64decode(split[1].encode("ascii") + b"==").decode("utf-8")
    )  # TODO: Make API agnostic (don't add padding if already present)
    return JWT(header=header, payload=payload, signature=split[2])
