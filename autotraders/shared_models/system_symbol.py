from autotraders.shared_models.map_symbol import MapSymbol


class SystemSymbol(MapSymbol):
    def __init__(self, s):
        super().__init__(s)
        if self.system is None:
            raise ValueError("SystemSymbol %s must have a system.", str(s))
        elif self.waypoint is not None:
            raise ValueError("SystemSymbol %s cannot have a waypoint.", str(s))
