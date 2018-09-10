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

The *reader* returned is an asyncio.StreamReader instance; the *writer* is 
an asyncio.StreamWriter instance.


.. autofunction:: create_session
.. autofunction:: stream_connect
.. autofunction:: stream_accept
.. autofunction:: get_sam_socket

Utilities
---------

.. autofunction:: dest_lookup
.. autofunction:: new_private_key
.. autofunction:: get_sam_address

Tunnel API
----------

Tunnel API is the quickest way to use regular programms inside I2P.
Client tunnel binds a remote I2P destination to a port on your local machine.
Server tunnel exposes a port on your local machine to the I2P network.

.. autofunction:: client_tunnel
.. autofunction:: server_tunnel
.. autoclass:: i2plib.tunnel.I2PTunnel
   :members:

Data structures
---------------

.. autoclass:: i2plib.Destination
   :members:

.. autoattribute:: i2plib.sam.Destination.data
.. autoattribute:: i2plib.sam.Destination.base64

.. autoclass:: i2plib.PrivateKey
   :members:

.. autoattribute:: i2plib.sam.PrivateKey.data
.. autoattribute:: i2plib.sam.PrivateKey.base64
.. autoattribute:: i2plib.sam.PrivateKey.destination

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
