class MapSymbol:
    """Generic Map symbol, could be a sector, system, or waypoint."""

    def __init__(self, s):
        """Your input must be a valid symbol for a sector, system, or waypoint. or a value error might be raised.
        :param s: The symbol
        """
        if type(s) is MapSymbol:
            s = str(s)
        split = s.split("-")
        self.sector = split[0]
        # TODO: Wait till stoplight is fixed
        # if len(self.sector) != 2:
        #     raise ValueError("Invalid map symbol")
        self.system = None
        self.waypoint = None
        if len(split) > 1:
            self.system = split[0] + "-" + split[1]
        if len(split) > 2:
            self.waypoint = split[0] + "-" + split[1] + "-" + split[2]
        if len(split) > 3:
            raise ValueError("Invalid map symbol")
        self.raw = s

    def __str__(self):
        """Returns the input that was passed as a string."""
        return self.raw

    def __hash__(self):
        return hash(self.raw)

    def __add__(self, other):
        return self / other

    def __truediv__(self, other):
        """Concatenates with a '-'"""
        assert isinstance(other, str)
        if other[0] == "-":
            other = other[1:]
        return MapSymbol(str(self) + "-" + other)

    def __eq__(self, other):
        return str(self) == str(other)
