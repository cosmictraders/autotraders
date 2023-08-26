from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Requirements(BaseModel):
    power: Optional[int]
    crew: Optional[int]
    slots: Optional[int]


class ShipComponent(BaseModel):
    symbol: str
    name: str
    description: Optional[str]
    condition: int
    requirements: Requirements


class Frame(ShipComponent):
    module_slots: int = Field(alias="moduleSlots")
    mounting_points: int = Field(alias="mountingPoints")
    fuel_capacity: int = Field(alias="fuelCapacity")


class Reactor(ShipComponent):
    power_output: int = Field(alias="powerOutput")


class Engine(ShipComponent):
    speed: int


class Module(ShipComponent):
    capacity: Optional[int]
    range: Optional[int]


class Mount(ShipComponent):
    strength: Optional[int]
    deposits: Optional[list[str]]
