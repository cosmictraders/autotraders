import time

import pytest

from autotraders import get_status
from autotraders.agent import Agent
from autotraders.faction import Faction
from autotraders.session import get_session
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship import Ship
from autotraders.faction.contract import Contract


@pytest.fixture
def session():
    s = get_session(None)
    s.base_url = "https://stoplight.io/mocks/spacetraders/spacetraders/96627693/"
    return s


def test_invalid_api_key():
    s = get_session("TEST")
    try:
        Agent(s)
        assert False  # shouldn't complete successfully
    except Exception as e:
        assert type(e) is IOError


def test_get_status():
    status = get_status()
    assert status.version == "v2"


def test_rate_limiter(session):
    t1 = time.time()
    for i in range(20):
        get_status(session)
    t2 = time.time()
    assert t2-t1 < 100


def test_agent(session):
    Agent(session)


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


def test_contact(session):
    Contract("blah", session)


def test_contact_functions(session):
    c = Contract("blah", session)
    c.accept()
    c.fulfill()


def test_contact_param_functions(session):
    c = Contract.negotiate("TEST-1", session)
    c.deliver("TEST-1", "GOLD", 5)


def test_faction(session):
    Faction.all(session)
