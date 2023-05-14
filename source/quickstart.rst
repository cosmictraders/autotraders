Quickstart
==================

To make any API requests, your client must first have a token, to get one, check out the official docs at
https://docs.spacetraders.io/quickstart/new-game

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
The general update function to refresh the client state is called `update()`.

