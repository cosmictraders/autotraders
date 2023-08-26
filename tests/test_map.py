from autotraders.map.system import System
from autotraders.map.waypoint import Waypoint
from autotraders.map.waypoint_types.jumpgate import JumpGate
from autotraders.map.waypoint_types.marketplace import Marketplace
from autotraders.map.waypoint_types.shipyard import Shipyard
from test_init import session


def test_system(session):
    System(
        "X1-AB12",
        session,
        {
            "symbol": "X1-AB12",
            "sectorSymbol": "X1",
            "type": "UNSTABLE",
            "x": 10,
            "y": 2,
            "factions": [{"symbol": "VOID"}],
            "waypoints": [
                {
                    "symbol": "X1-AB12-AB11",
                    "type": "JUMP_GATE",
                    "x": 10,
                    "y": 1,
                }
            ],
        },
    )


def test_waypoint(session):
    Waypoint("X1-FE16-FD15", session)


def test_waypoint_traits(session):
    JumpGate("X1-FE16-FD15", session)
    Marketplace("X1-FE16-FD15", session)
    Shipyard("X1-FE16-FD15", session)
