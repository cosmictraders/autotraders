from autotraders.faction.contract import Contract
from test_init import session

mock_contract = {
    "id": "test_contract_id",
    "factionSymbol": "COSMIC",
    "type": "PROCUREMENT",
    "terms": {
        "deadline": "2019-08-24T14:15:22Z",
        "payment": {
            "onAccepted": 100,
            "onFulfilled": 5000
        },
        "deliver": [{
            "tradeSymbol": "string",
            "destinationSymbol": "X1-TEST-TEST2",
            "unitsRequired": 0,
            "unitsFulfilled": 0
        }]
    },
    "accepted": False,
    "fulfilled": False,
    "expiration": "2019-08-24T14:15:22Z",
    "deadlineToAccept": "2019-08-24T14:15:22Z"
}


def test_contact(session):
    Contract("blah", session, data=mock_contract)


def test_contact_functions(session):
    c = Contract("blah", session, data=mock_contract)
    c.accept()
    c.fulfill()


def test_contact_param_functions(session):
    c = Contract.negotiate("TEST-1", session)
    c.deliver("TEST-1", "GOLD", 5)
