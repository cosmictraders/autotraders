# v2.3.4

- Fix issue with Contract deliver endpoint not able to return the right… by @Rsilnav in #14
- Fixed issue with nav.origin returning the wrong symbol

# v2.3.3

- UPDATED: Updated API version support to Dec. 2
- FIXED: minor marketplace error

# v2.3.2

- Bugfix

# v2.3.1

- FIXED: Bugs

# v2.3.0

- BREAKING: Route.origin and Route.destination are now Waypoints
- ADDED: Overloaders to many smaller classes
- FIXED: many bugs

# v2.2.8

- FIXED: Issue where h2 wasn't being installed
- FIXED: more api bugs

# v2.2.7

- More bug fixing

# v2.2.6

- FIXED: Issue with Activity being required

# v2.2.5

- BREAKING: API updated to support v2.1 (All previous API versions are now unsupported)
- ADDED: Some enums for market trade goods

# v2.2.4

- FIXED: More packaging issues

# v2.2.3

- FIXED: More packaging issues

# v2.2.2

- FIXED: GitHub python package publishing

# v2.2.1

- UPDATED: pyrate is now 3.0+
- FIXED: GitHub python package publishing

# v2.2.0

- ADDED: cooldown.active attribute
- UPDATED: Moved version stuff to version.py and added more version info
- UPDATED: Formatting

# v2.1.0

- BREAKING: The Update Ship Cooldown from the Ship class has been removed.
- ADDED: Method to get the cost effective refuel amount to the Fuel class.
- FIXED: Bug that limited retries to one less than what they should be
- FIXED: Bug that caused the wait_for_transit and the equivalent async version to error if there wasn't any transit happening.

# v2.0.4

- UPDATED: New server changes.

# v2.0.3

- Releasing Update

# v2.0.2

- FIXED: Rogue print statement
- FIXED: ship.nav warping instead of navigating

# v2.0.1

- FIXED: Various bugs

# v2.0.0

- BREAKING: Dropped requests as a dependency, switched to httpx
- BREAKING: Added and enabled http2
- BREAKING: Removed `navigate_async`, (it was deprecated)
- BREAKING: Removed `get_session`, you can instantiate the client for greater control.
- BREAKING: Renamed `Fuel.total` to `Fuel.capacity`
- BREAKING: `agent.ships` and `agent.contracts` have been removed.
- BREAKING: `status.leaderboards` is no longer a `list` it is now a `dict`
- BREAKING: `status.next_reset` and `status.reset_frequency` have been moved to `status.server_reset`
and renamed to `next` and `frequency`
- BREAKING: `ship.reactor.cooldown` has been completely removed
- UPDATED: Changed `attrs` to `pydantic`.

# v1.9.0

- ADDED: `Agent.create`
- ADDED: Email check for email fields
- ADDED: dependency on `attrs`
- ADDED: Missing fields in `get_status`

# v1.8.2

- FIXED: Agent creation

# v1.8.1

- FIXED: Create agent method

# v1.8.0

- ADDED: Automatic retrying on 429 ratelimit errors
- ADDED: Agent registration method
- ADDED: Navigation from a `Nav` object
- ADDED: Dictionary style `__getitem__` to `Cargo`
- ADDED: Stoplight Sidebar to function/class mapping
- UPDATED: Fuel and flight time calculations
- UPDATED: docs
- FIXED: `contract.deliver.trade_symbol` is now an item instead of a map symbol
- FIXED: `PaginatedList` docs

# v1.7.1

- FIXED: Agent init
- FIXED: hashes

# v1.7.0

- ADDED: Ability to view other agents
- ADDED: Partial refueling
- ADDED: `__hash__` to `MapSymbol` and `ShipSymbol`
- FIXED: `__eq__` for `MapSymbol`

# v1.6.4

- FIXED: `NavState` issue

# v1.6.3

- FIXED: `NavState` issue

# v1.6.2

- ADDED: Crew rotation
- ADDED: PYPI classifiers
- CHANGED: `ship.nav.flight_mode` and `ship.nav.status` to enums
- FIXED: Bug where `SpaceTradersException` was not being raised
- FIXED: PYPI links

# v1.6.1

- ADDED: `__version__`

# v1.6.0

- BREAKING: Exception class changed from `IOError` to `SpaceTradersException`
- FIXED: Marketplace not raising a proper error
- FIXED: Mount installation error

# v1.5.5

- FIXED: Waypoint bug

# v1.5.4

- BREAKING: Removed jumpgate (shouldn't affect anyone seeing I added it 2 hours ago)

# v1.5.3

- FIXED: get ship cooldown and cooldown

# v1.5.2

Not a minor release because there aren't no real server side change.

- ADDED: extracting with survey
- ADDED: Jump gate attribute to system (its a boolean)
- CHANGED: Waypoint traits is now an optional attribute
- FIXED: Removed excessive `Optional` on typing
- FIXED: flight mode patching
- FIXED: Shipyard transaction ship return

# v1.5.1

- FIXED: Adding and removing mounts
- FIXED: Market transaction using empty string as item description
- FIXED: Removed `Optional` from more fields

# v1.5.0

- ADDED: ship capabilities class
- ADDED: Typed ship states (mostly unused)
- FIXED: Typing

# v1.4.3

- FIXED: Waypoint list all bug fix

# v1.4.2

- FIXED: Waypoint list all bug fix

# v1.4.1

- FIXED: Agent pagination bug fix

# v1.4.0

- ADDED: Proper Pagination via pagination list class
- CHANGED: Refining now returns the refined product as a `Item`

# v1.3.3

- FIXED: Market waypoint type initialization bug

# v1.3.2

- FIXED: Bug that causes Waypoint types to fail on initialization

# v1.3.1

- FIXED: Bug involving agent ships and contracts being accidentally paginated (temp fix).

# v1.3.0

- BREAKING: Updating now is forced (`update` is no longer an initialization parameter for any request class, `data` is the replacement and requires the actual data to be provided)
- BREAKING: Deprecated the `hard` parameter for `Ship.update()` (it does nothing now)
- BREAKING `get_all*` and `list_systems` have been removed use `Ship.all()` or `Contract.all()` or `System.all()` or `Waypoint.all()`
- ADDED: 6/3/2023 Server Features Support
- ADDED: Fuel Cost and Time formulas in `util.py`
- ADDED: Market Transaction
- UPDATED: Polling time for `navigate_async` has changed to 1 second and is configurable
- UPDATED: Refueling, Buying, Updating mounts, and Selling now return `MarketTransaction`
- FIXED: Removed Print Statements

# v1.2.4

- ADDED: More static types
- FIXED: Bug that caused time parsing errors on older python versions (<3.11)

# v1.2.3

- FIXED: Moving parameter in nav
- FIXED: Agent Typing
- FIXED: Made Agent Headquarters a map symbol

# v1.2.2

- FIXED: Excessively cautious rate limiter
- FIXED: Made token attribute truly optional

# v1.2.1

- FIXED: GitHub Actions python package publishing issue

# v1.2.0

- ADDED: Rate Limiter
- ADDED: `pyproject.toml` dependency section
- CHANGED: `token` is now optional for `get_session`
- FIXED: `marketplace` and `shipyard` having null values
- FIXED: `status.next_reset` and `status.reset_date` are now datetime objects
- FIXED: `list_systems` now actually returns the systems
- FIXED: `scan_ships` now does not fail
- FIXED: Fulfilling a contract now triggers a state update
- FIXED: Negotiating a contract is now contract independent
- FIXED: `WaypointSymbol.__div__` has been renamed to `__truediv__`

# v1.1.5

- FIXED: JSON POST issue that originated from `requests`
- FIXED: Automatic `WaypointSymbol` to `str` conversion for jumping, nav, or warping
- FIXED: Abstracted `Waypoint` from base entity class
- FIXED: Made extraction work
- FIXED: Typed some parameters that were marked as `None` by IDEs

# v1.1.4

- ADDED: equality tests for `MapSymbol`, `Waypoint`, and `System`
- CHANGED: Switched to timezone aware datetime parser
- FIXED: Bugs with `MapSymbol`
- FIXED: Bugs with navigation status (the `moving` attribute was the inverse of what it should have been)

# v1.1.3

- CHANGED: `None` is used instead of `math.nan`

# v1.1.2

- ADDED: System Scanning
- UPDATED: More detailed server status
- UPDATED: sanity checks to map symbol concatenation by division
- BUGFIX: map symbol bug fix

# v1.1.1

- Fixed print statements
- Fixed waypoint symbol bug

# v1.1.0

- Updated to support the new features from the May 20nd updates
- Internal refactoring
- The OOP model has been enhanced
- Tests

# v1.0.5

- Added `.all()` helper method
- Mocked some data with math.nan

# v1.0.4

- Added star type to system

# v1.0.3

- A bunch of bug fixes

# v1.0.2

- Made all requirement attributes optional

# v1.0.1

- Bugfix: make slots optional in requirements

# v1.0.0

- BREAKING: renamed move and move_async to navigate and navigate_async
- BREAKING: Moved many files around
- BREAKING: nav info, like `status` is in ship.nav rather than ship.
- added: purchase functionality
- added: datetime parsing
- added: ability to jettison cargo
- added: jumpgate support
- adding: refining capability
- added: charting
- added: ship nav patching
- added: more shipyard info if ship is at waypoint and improved ship info.
- added: nav route
- added: more market info
- added: support for cooldown
- added: surveying capability
- contract deadline is now a datetime
- added: contract type
- added: scanning
- statically type all requests.Session parameters
- added: tests and fixed time parser
- added: session

# v0.3.1

- Fixed build bug

# v0.3.0

- Docs have arrived on GitHub pages
- BREAKING: `ships.py` has been renamed to `ship.py`
- Added: Ability to purchase ships from shipyards
- Added: Faction APIs
- Added: Ability to jettison cargo
- Bugfix: Updating marketplace no longer fails

# v0.2.0

- Added basic shipyard read
- Added basic marketplace read
- Added shipyard and marketplace flags to the `Waypoint` class

# v0.1.5

- Another bugfix

# v0.1.4

- Fixed circular imports issue

# v0.1.3

- Fixed critical bugs (again)

# v0.1.2

- FIXED: errors

# v0.1.1

- Switched to GitHub actions for PYPI deployment
- reformatted code
- ADDED: requirements.txt
