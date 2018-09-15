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
   :inherited-members:
.. autoclass:: i2plib.ServerTunnel
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
