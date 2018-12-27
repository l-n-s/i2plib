.. _api:

Developer Interface
===================

.. module:: i2plib

This part of the documentation covers all the interfaces of i2plib.

Network connections 
-------------------

These 4 *coroutines* provide everything you need for making connections inside 
I2P network. All of them return a tuple of transports *(reader, writer)* to 
deal with.

The *reader* returned is an :class:`asyncio.StreamReader` instance; the *writer* is 
an :class:`asyncio.StreamWriter` instance.


.. autofunction:: create_session
.. autofunction:: stream_connect
.. autofunction:: stream_accept
.. autofunction:: get_sam_socket

Context managers 
----------------

The following are asynchronous context managers for making I2P connections.

You can use them like that:

::
    
    import asyncio
    import i2plib

    async def connect_test(destination):
        session_name = "test"

        async with i2plib.Session(session_name):
            async with i2plib.StreamConnection(session_name, destination) as c:
                c.write(b"PING")
                resp = await c.read(4096)

        print(resp)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect_test("dummy.i2p"))
    loop.stop()

.. autoclass:: i2plib.Session
   :members:
.. autoclass:: i2plib.StreamConnection
   :members:
.. autoclass:: i2plib.StreamAcceptor
   :members:

Utilities
---------

.. autofunction:: dest_lookup
.. autofunction:: new_destination
.. autofunction:: get_sam_address

Tunnel API
----------

Tunnel API is the quickest way to use regular software inside I2P.
Client tunnel binds a remote I2P destination to a local address.
Server tunnel exposes a local address to the I2P network.

.. autoclass:: i2plib.tunnel.I2PTunnel
   :members:
.. autoclass:: i2plib.ClientTunnel
   :members:
   :inherited-members:
.. autoclass:: i2plib.ServerTunnel
   :members:
   :inherited-members:

Data structures
---------------

.. autoclass:: i2plib.Destination
   :members:

.. autoattribute:: i2plib.sam.Destination.data
.. autoattribute:: i2plib.sam.Destination.base64
.. autoattribute:: i2plib.sam.Destination.private_key

.. autoclass:: i2plib.PrivateKey
   :members:

.. autoattribute:: i2plib.sam.PrivateKey.data
.. autoattribute:: i2plib.sam.PrivateKey.base64

Exceptions
---------------

.. autoexception:: CantReachPeer
.. autoexception:: DuplicatedDest
.. autoexception:: DuplicatedId
.. autoexception:: I2PError
.. autoexception:: InvalidId
.. autoexception:: InvalidKey
.. autoexception:: KeyNotFound
.. autoexception:: PeerNotFound
.. autoexception:: Timeout
