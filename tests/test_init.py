import time

import pytest

from autotraders import get_status
from autotraders.agent import Agent
from autotraders.faction import Faction
from autotraders.session import get_session


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
    assert t2 - t1 < 100


def test_agent(session):
    Agent(session)


def test_faction(session):
    Faction.all(session)
