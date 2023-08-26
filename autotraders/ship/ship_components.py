from typing import Optional

from pydantic import BaseModel, Field


class Requirements(BaseModel):
    power: Optional[int] = None
    crew: Optional[int] = None
    slots: Optional[int] = None


class ShipComponent(BaseModel):
    symbol: str
    name: str
    description: Optional[str] = None
    condition: Optional[int] = None
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
    capacity: Optional[int] = None
    range: Optional[int] = None


class Mount(ShipComponent):
    strength: Optional[int] = None
    deposits: Optional[list[str]] = None
