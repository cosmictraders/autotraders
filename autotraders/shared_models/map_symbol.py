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
        if len(split) == 2:
            self.system = split[0] + "-" + split[1]
        if len(split) == 3:
            self.waypoint = split[0] + "-" + split[1] + "-" + split[2]
        if len(split) > 3:
            raise ValueError("Invalid map symbol")
        self.raw = s

    def __str__(self):
        """Returns the input that was passed as a string."""
        return self.raw

    def __div__(self, other):
        """Concatenates with a "-", TODO: sanity checks"""
        return MapSymbol(str(self) + "-" + other)
