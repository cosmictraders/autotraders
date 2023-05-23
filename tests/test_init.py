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
    s = Ship("TEST", session)
    s.dock()
    s.orbit()
    s.refuel()


def test_contact(session):
    c = Contract("blah", session)
    c.accept()
    c.fulfill()

def test_map_symbol():
    s = MapSymbol("X1-TEST")
    s1 = MapSymbol("X1-TEST2")
    s2 = MapSymbol("X1-TEST")
    assert s != s1
    assert s == s2
