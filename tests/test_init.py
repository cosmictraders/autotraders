import pytest

from autotraders.agent import Agent
from autotraders.session import get_session
from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.ship import Ship
from autotraders.faction.contract import Contract


@pytest.fixture
def session():
    s = get_session("BLANK")
    s.base_url = "https://stoplight.io/mocks/spacetraders/spacetraders/96627693/"
    return s


def test_invalid_api_key():
    s = get_session("TEST")
    try:
        Agent(s)
        assert False  # shouldn't complete successfully
    except Exception as e:
        assert type(e) is IOError


def test_agent(session):
    a = Agent(session)
    assert a.credits == 0
    assert a.symbol == "string"


def test_ship(session):
    Ship("TEST", session)


def test_ship_functions(session):
    s = Ship("TEST", session)
    s.dock()
    s.orbit()
    s.refuel()
    s.extract()


def test_ship_param_functions(session):
    s = Ship("TEST-1", session)
    s.navigate("X1-TEST-TEST")
    s.jump(MapSymbol("X1-TEST-TEST"))
    s.warp("X1-TEST-TEST")
    s.sell("FUEL", 42)
    s.buy("FUEL", 42)
    s.refine("FUEL")
    s.transfer("TEST-2", "FUEL", 42)


def test_contact(session):
    Contract("blah", session)


def test_contact_functions(session):
    c = Contract("blah", session)
    c.accept()
    c.fulfill()
    c.deliver("TEST-1", "GOLD", 5)
