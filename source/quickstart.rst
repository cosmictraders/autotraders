Quickstart
==================

To make any API requests, your client must first have a token, to get one, check out the official docs at
https://docs.spacetraders.io/quickstart/new-game#register-as-a-new-agent

Once you have your token, you can quickly create a session with `autotraders.session`

.. code:: python

    from autotraders import session
    s = session.get_session("YOUR_TOKEN_HERE")

To make sure your token works, try to check how many credits you have:

.. code:: python

    from autotraders import agent, session
    s = session.get_session("YOUR_TOKEN_HERE")
    my_agent = agent.Agent(s)
    print(my_agent.credits, my_agent.headquarters)


Minimal API Request Model
---------------------------
Once an object is initialized, no api requests are made until a function is called.
The general update function to refresh the client state is called ``.update()``.

You can use ``.all()`` to get all of your objects of that type for example ``Ships.all()`` returns all your ships,
``.all()`` is paginated, so it returns a ``PaginatedList``.


Writing a Program
---------------------
Now lets write a program to extract resources from an astroid field and sell it at the market which is at the astroid field.

To start off, lets initialize the session.

.. code:: python

    from autotraders import session
    s = session.AutoTradersSession("YOUR_TOKEN_HERE")


Now we can create a ship object to control the ship.

.. code:: python

    ship = Ship("STARSTAR-1", s)  # Note that this is the ship symbol, it varies for different people

First we have to extract the resources, which can be done via the ``.extract()`` method, but it only works when the ship is in orbit,
so we must use the ``.orbit()`` method first. `extracted_resources` simply represents what has been extracted.

.. code:: python

    ship.orbit()
    extracted_resources = ship.extract()

Next the ship needs to dock in order to sell its cargo:

.. code:: python

    ship.dock()

The ships cargo is stored as a dictionary in ``ship.cargo.inventory``.
Let's sell the resource of it via ``.sell("SYMBOL", ship.cargo.inventory["SYMBOL"])`` where symbol is the item to sell.

.. code:: python

    ship.sell(extracted_resources.symbol, extracted_resources.units)

And now we're done! You can wrap it in a while loop so it loops if you wish: ``ship.wait_cooldown()`` will use a
``time.sleep`` to wait until the cooldown has finished.

.. code:: python

    from autotraders import session
    from autotraders.ship import Ship
    import time
    s = session.AutoTradersSession("YOUR_TOKEN_HERE")
    ship = Ship("STARSTAR-1", s)  # Note that this is the ship symbol, it varies for different people
    while True:
        ship.orbit()
        extracted_resources = ship.extract()
        ship.dock()
        ship.sell(extracted_resources.symbol, extracted_resources.units)
        ship.wait_cooldown()  # make sure that the cooldown doesn't cause an extraction error (ship.await_cooldown is the async equivalent)

