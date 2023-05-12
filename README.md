# Autotraders
A spacetraders API focused on automation and ease of use
## Usage
First you need a client, which can be generated 
```python
import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

token = TOKEN_HERE
s = requests.Session()
s.auth = BearerAuth(token)
```
And now you're all set to use they actual API.

## Ships

```python
from autotraders.ship import Ship, get_all_ships

# create a session here
ship = Ship("SYMBOL-Here", session)  # This makes an API request
ships = get_all_ships(session)  # This also only makes one API request
ship.dock()
ship.refuel()
ship.orbit()  # All these functions make API calls (one each), but the line below doesn't
print(ship.fuel.current + "/" + ship.fuel.total)
```
## Contract
```python
from autotraders.contract import Contract, get_all_contracts
# create a session here
contract = Contract("id-here", session)
contracts = get_all_contracts(session)
contract.accept()
print(contract.accepted) # True
contract.deliver("SHIP_SYMBOL", "ALUMINUM_ORE", 30)
contract.fulfill()
print(contract.fulfilled) # True
```
