i2plib
======

i2plib is a modern asynchronous library for building I2P applications. 

Installing
----------

::

    pip install i2plib

Requirements:

- Python version >= 3.5
- I2P router with SAM API enabled

Connecting to a remote I2P destination
--------------------------------------

::

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

::

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

::

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

::

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


Resources
---------

* `i2plib online documentation`_
* `Invisible Internet Project`_
* `SAM API documentation`_
* `Python asyncio documentation`_

.. _i2plib online documentation: https://i2plib.readthedocs.io/en/latest/
.. _Invisible Internet Project: https://geti2p.net/en/
.. _SAM API documentation: https://geti2p.net/en/docs/api/samv3
.. _Python asyncio documentation: https://docs.python.org/3/library/asyncio.html

Aknowledgments
--------------

* `i2p.socket, drop in python socket module that uses i2p`_
* `txi2p, I2P bindings for Twisted`_
* `leaflet, Dead simple I2P SAM library, written in Python 3`_

.. _i2p.socket, drop in python socket module that uses i2p: https://github.com/majestrate/i2p.socket
.. _txi2p, I2P bindings for Twisted: https://github.com/str4d/txi2p
.. _leaflet, Dead simple I2P SAM library, written in Python 3: https://github.com/MuxZeroNet/leaflet
