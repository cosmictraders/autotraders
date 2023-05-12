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
from autotraders.ships import Ship
# create a session here
ship = Ship("SYMBOL-Here", session) # This makes an API request
ship.dock()
ship.refuel()
ship.orbit()
print(ship.fuel.current + "/" + ship.fuel.total)
```
