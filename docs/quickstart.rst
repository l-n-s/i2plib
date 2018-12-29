Quick start
===========

Installing
----------

::

    pip install i2plib

Requirements:

- Python version >= 3.5
- I2P router with SAM API enabled

Connecting to a remote I2P destination
--------------------------------------

.. code-block:: python

    import asyncio
    import i2plib

    async def connect_test(destination):
        session_name = "test-connect"

        # create a SAM stream session
        await i2plib.create_session(session_name)

        # connect to a destination
        reader, writer = await i2plib.stream_connect(session_name, destination)

        # write data to a socket
        writer.write(b"PING")

        # asynchronously receive data
        data = await reader.read(4096)
        print(data.decode())

    # run event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_test("dummy.i2p"))
    loop.stop()

Accept connections in I2P
-------------------------

.. code-block:: python

    import asyncio
    import i2plib

    async def accept_test():
        session_name = "test-accept"

        # create a SAM stream session
        await i2plib.create_session(session_name)

        # accept a connection
        reader, writer = await i2plib.stream_accept(session_name)
        
        # first string on a client connection always contains clients I2P destination
        incoming = await reader.read(4096)
        dest, data = incoming.split(b"\n", 1)
        remote_destination = i2plib.Destination(dest.decode())

        # destination and data may come in one chunck, if not - we wait for the actual
        # incoming data
        if not data:
            data = await reader.read(4096)

        print(data.decode())

        # send data to the client
        writer.write(b"PONG")
        writer.close()

    # run event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(accept_test())
    loop.stop()

Server tunnel
-------------

Expose a local service to I2P like that:

.. code-block:: python

    import asyncio
    import i2plib

    loop = asyncio.get_event_loop()
    # making your local web server available in the I2P network
    tunnel = i2plib.ServerTunnel(("127.0.0.1", 80))
    asyncio.ensure_future(tunnel.run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

Client tunnel
-------------

Bind a remote I2P destination to a port on your local host:

.. code-block:: python

    import asyncio
    import i2plib

    loop = asyncio.get_event_loop()
    # bind irc.echelon.i2p to 127.0.0.1:6669
    tunnel = i2plib.ClientTunnel("irc.echelon.i2p", ("127.0.0.1", 6669))
    asyncio.ensure_future(tunnel.run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

More examples
-------------

You can see more demo applications in `docs/examples` directory of the source repository.

