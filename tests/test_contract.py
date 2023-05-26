from autotraders.faction.contract import Contract
from test_init import session


def test_contact(session):
    Contract("blah", session)


def test_contact_functions(session):
    c = Contract("blah", session)
    c.accept()
    c.fulfill()


def test_contact_param_functions(session):
    c = Contract.negotiate("TEST-1", session)
    c.deliver("TEST-1", "GOLD", 5)
