Usage Notes
=============
Just some FAQs and notes about pitfalls etc.

- Errors are always thrown then the API request fails (usually an ``SpaceTradersException``)
- If an object attribute has a value of ``None`` (or doesn't exist) is it likely the object hasn't synced that part of its state from the server
- Python 3.9 or higher necessary for usage.
- ``Survey.asdict()`` (equivalent to `dict(survey)`) exists for any surveys you might want to convert into json ``json.dumps(dict(survey))``.

Finding Methods
_________________
Since having documentation for methods that simply make a request to the server is exessive, I will provide a mapping from
`Stoplight <https://spacetraders.stoplight.io/docs/spacetraders/11f2735b75b02-space-traders-api>`_.
Things might not have a one to one correspondence however.

- Get Status -> :meth:`autotraders.status.get_status` (or autotraders.get_status)
- Register New Agent -> :meth:`autotraders.register_agent`

Agents
####################
- Get Agent -> :meth:`autotraders.agent.Agent`
- List Agents -> :meth:`autotraders.agent.Agent.all`
- Get Public Agent ->  :meth:`autotraders.agent.Agent`

Contracts
####################

- List Contracts -> :meth:`autotraders.faction.contract.Contract.all`
- Get Contract -> :meth:`autotraders.faction.contract.Contract`
- Accept Contract -> :meth:`autotraders.faction.contract.Contract.accept`
- Deliver Cargo to Contract -> :meth:`autotraders.faction.contract.Contract.deliver`
- Fulfill Contract -> :meth:`autotraders.faction.contract.Contract.fulfill`

Factions
####################

- List Factions -> :meth:`autotraders.faction.Faction.all`
- Get Faction -> :meth:`autotraders.faction.Faction`

Fleet
####################

- List Ships -> :meth:`autotraders.ship.Ship.all`
- Purchase Ship -> :meth:`autotraders.map.waypoint_types.shipyard.Shipyard.purchase`
- Get Ship -> :meth:`autotraders.ship.Ship`
- Get Ship Cargo -> :meth:`autotraders.ship.Ship.cargo`
- Orbit Ship -> :meth:`autotraders.ship.Ship.orbit`
- Ship Refine -> :meth:`autotraders.ship.Ship.refine`
- Create Chart -> :meth:`autotraders.ship.Ship.chart`
- Get Ship Cooldown -> :meth:`autotraders.ship.Ship.cooldown` (update via :meth:`autotraders.ship.Ship.update_ship_cooldown`)
- Dock Ship -> :meth:`autotraders.ship.Ship.dock`
- Create Survey -> :meth:`autotraders.ship.Ship.survey`
- Extract Resources -> :meth:`autotraders.ship.Ship.extract`
- Jettison Cargo -> :meth:`autotraders.ship.Ship.jettison`
- Jump Ship -> :meth:`autotraders.ship.Ship.jump`
- Navigate Ship -> :meth:`autotraders.ship.Ship.navigate`
- Patch Ship Nav -> :meth:`autotraders.ship.Ship.patch_navigation`
- Get Ship Nav -> :meth:`autotraders.ship.Ship.nav`
- Sell Cargo -> :meth:`autotraders.ship.Ship.sell`
- Scan Systems -> :meth:`autotraders.ship.Ship.scan_systems`
- Scan Waypoints -> :meth:`autotraders.ship.Ship.scan_waypoints`
- Scan Ships -> :meth:`autotraders.ship.Ship.scan_ships`
- Refuel Ship -> :meth:`autotraders.ship.Ship.refuel`
- Purchase Cargo -> :meth:`autotraders.ship.Ship.buy`
- Transfer Cargo -> :meth:`autotraders.ship.Ship.transfer`
- Negotiate Contract -> :meth:`autotraders.faction.contract.Contract.negotiate`
- Get Mounts -> :meth:`autotraders.ship.Ship.mounts`
- Install Mount -> :meth:`autotraders.ship.Ship.install_mount`
- Remove Mount -> :meth:`autotraders.ship.Ship.remove_mount`


Systems
####################

- List Systems -> :meth:`autotraders.map.system.System.all`
- Get System -> :meth:`autotraders.map.system.System`
- List Waypoints in System -> :meth:`autotraders.map.waypoint.Waypoint.all`
- Get Waypoint -> :meth:`autotraders.map.waypoint.Waypoint`
- Get Market -> :meth:`autotraders.map.waypoint_types.marketplace.Marketplace`
- Get Shipyard -> :meth:`autotraders.map.waypoint_types.shipyard.Shipyard`
- Get Jump Gate -> :meth:`autotraders.map.waypoint_types.jumpgate.JumpGate`

Versioning
_______________
As the game is in alpha the versioning system is not exactly semantic.

- Major releases happen when the code structure changes or there is a breaking matter that involves the codebase
- Minor releases usually occur when major game changes happen, or a new feature has been added.
- Patch releases could be bug fixes or updates to keep up with game changes.
