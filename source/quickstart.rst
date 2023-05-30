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
    print(my_agent.credits)


Minimal API Request Model
---------------------------
Once an object is initialized, no api requests are made until a function is called.
The general update function to refresh the client state is called ``.update()``.

You can use ``.all()`` to get all of your objects of that type ``Ships.all()`` returns all your ships for example,
``.all()`` is paginated, so it returns the list and the page number.


Writing a Program
---------------------
Now lets write a program to extract resources from an astroid field and sell it at the market which is at the astroid field.

To start off, lets initialize the session.

.. code:: python

    from autotraders import session
    s = session.get_session("YOUR_TOKEN_HERE")


Now we can create a ship object to control the ship.

.. code:: python

    from autotraders import session
    from autotraders.ship import Ship
    s = session.get_session("YOUR_TOKEN_HERE")
    ship = Ship("STARSTAR-1")  # Note that this is the ship symbol, it varies for different people

First we have to extract the resources, which can be done via the ``.extract()`` method, but it only works when the ship is in orbit,
so we must use the ``.orbit()`` method first.

.. code:: python

    from autotraders import session
    from autotraders.ship import Ship
    s = session.get_session("YOUR_TOKEN_HERE")
    ship = Ship("STARSTAR-1")  # Note that this is the ship symbol, it varies for different people
    ship.orbit()
    ship.extract()

Next the ship needs to dock in order to sell its cargo:

.. code:: python

    from autotraders import session
    from autotraders.ship import Ship
    s = session.get_session("YOUR_TOKEN_HERE")
    ship = Ship("STARSTAR-1")  # Note that this is the ship symbol, it varies for different people
    ship.orbit()
    ship.extract()
    ship.dock()

The ships cargo is stored as a dictionary in ``ship.cargo.inventory``.
Let's sell all of it via ``.sell("SYMBOL", ship.cargo.inventory["SYMBOL"])`` where symbol is the item to sell.

.. code:: python

    from autotraders import session
    from autotraders.ship import Ship
    s = session.get_session("YOUR_TOKEN_HERE")
    ship = Ship("STARSTAR-1")  # Note that this is the ship symbol, it varies for different people
    ship.orbit()
    ship.extract()
    ship.dock()
    for item in ship.cargo.inventory:
        ship.sell(item, ship.cargo.inventory[item])

And now we're done! You can wrap it in a while loop so it loops if you wish.

.. code:: python

    from autotraders import session
    from autotraders.ship import Ship
    import time
    s = session.get_session("YOUR_TOKEN_HERE")
    ship = Ship("STARSTAR-1")  # Note that this is the ship symbol, it varies for different people
    while True:
        ship.orbit()
        ship.extract()
        ship.dock()
        for item in ship.cargo.inventory:
            ship.sell(item, ship.cargo.inventory[item])
        time.sleep(60)  # make sure that the cooldown doesn't cause an extraction error

