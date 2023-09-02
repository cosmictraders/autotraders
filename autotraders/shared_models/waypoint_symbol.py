from autotraders.shared_models.map_symbol import MapSymbol


class WaypointSymbol(MapSymbol):
    def __init__(self, s):
        super().__init__(s)
        if self.system is None:
            raise ValueError("WaypointSymbol %s must have a system.", str(s))
        if self.waypoint is None:
            raise ValueError("WaypointSymbol %s must have a waypoint.", str(s))
