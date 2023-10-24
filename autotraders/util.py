import math

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
        return 15 + 15 * distance / ship_speed
    elif mode == FlightMode.DRIFT:
        return 15 + 150 * distance / ship_speed
    elif mode == FlightMode.BURN:
        return 15 + 7.5 * distance / ship_speed
    elif mode == FlightMode.STEALTH:
        return 15 + 30 * distance / ship_speed


def distance(*args):
    """
    If there is one arg, then the arg should be a iterable of length 2 or 4.
    It will be expanded and used as a 2 or 4 arg.
    If there are 2 args, then they should both have x and y attributes
    if there are 4 args they should be in the format x_1, y_1, x_2, y_2

    :return: The euclidian distance between the two objects.
    """
    if len(args) == 1:
        return distance(*args)
    elif len(args) == 2:
        return distance(
            getattr(args[0], "x"),
            getattr(args[0], "y"),
            getattr(args[1], "x"),
            getattr(args[1], "y"),
        )
    else:
        return math.sqrt((args[0] - args[2]) ** 2 + (args[1] - args[3]) ** 2)
