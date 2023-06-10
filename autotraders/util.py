from autotraders.ship.states import FlightMode


def travel_fuel(distance, mode):
    if mode == FlightMode.CRUISE:
        return distance
    elif mode == FlightMode.DRIFT:
        return 1
    elif mode == FlightMode.BURN:
        return 2 * distance
    elif mode == FlightMode.STEALTH:
        return distance


def travel_time(distance, ship_speed, mode):
    if mode == FlightMode.CRUISE:
        return 15 + 10 * distance / ship_speed
    elif mode == FlightMode.DRIFT:
        return 15 + 100 * distance / ship_speed
    elif mode == FlightMode.BURN:
        return 15 + 5 * distance / ship_speed
    elif mode == FlightMode.STEALTH:
        return 15 + 20 * distance / ship_speed
