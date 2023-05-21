import pytest

from autotraders.agent import Agent
from autotraders.session import get_session


@pytest.fixture
def session():
    s = get_session("BLANK")
    s.base_url = "https://stoplight.io/mocks/spacetraders/spacetraders/96627693"
    return s


def test_invalid_api_key():
    s = get_session("TEST")
    try:
        Agent(s)
        assert False  # shouldn't complete successfully
    except Exception as e:
        assert type(e) is IOError
