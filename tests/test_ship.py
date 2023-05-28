from datetime import datetime, timedelta, timezone

from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship import Ship, Nav
from test_init import session


def test_ship(session):
    Ship("TEST", session)


def test_ship_functions(session):
    s = Ship("TEST", session)
    s.update_ship_cooldown()
    s.dock()
    s.orbit()
    s.refuel()
    s.extract()


def test_ship_param_functions(session):
    s = Ship("TEST-1", session)
    s.navigate("X1-TEST-TEST")
    s.patch_navigation("DRIFT")
    s.jump(MapSymbol("X1-TEST-TEST"))
    s.warp("X1-TEST-TEST")
    s.sell("FUEL", 42)
    s.buy("FUEL", 42)
    s.refine("FUEL")
    s.transfer("TEST-2", "FUEL", 42)
    s.jettison("FUEL", 42)


def test_ship_nav(session):
    start = datetime.now(timezone.utc) - timedelta(seconds=5)
    end = datetime.now(timezone.utc) + timedelta(seconds=5)
    n = Nav(
        {
            "status": "IN_TRANSIT",
            "waypointSymbol": "X1-TEST-TEST2",
            "flightMode": "CRUISE",
            "route": {
                "destination": {"symbol": "X1-TEST-TEST2"},
                "departure": {"symbol": "X1-TEST-TEST"},
                "departureTime": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "arrival": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        }
    )
    assert n.status == "IN_TRANSIT"
    assert n.moving
    start2 = datetime.now(timezone.utc) - timedelta(seconds=10)
    end2 = datetime.now(timezone.utc) - timedelta(seconds=5)
    n2 = Nav(
        {
            "status": "ORBIT",
            "waypointSymbol": "X1-TEST-TEST2",
            "flightMode": "CRUISE",
            "route": {
                "destination": {"symbol": "X1-TEST-TEST2"},
                "departure": {"symbol": "X1-TEST-TEST"},
                "departureTime": start2.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "arrival": end2.strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
        }
    )
    assert n2.status == "ORBIT"
    assert not n2.moving
