from enum import Enum


class FlightMode(str, Enum):
    CRUISE = "CRUISE"
    DRIFT = "DRIFT"
    BURN = "BURN"
    STEALTH = "STEALTH"


class NavState(str, Enum):
    DOCK = "DOCK"
    ORBIT = "ORBIT"
    IN_TRANSIT = "IN_TRANSIT"
