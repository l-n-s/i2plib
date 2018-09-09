import asyncio
import logging

import i2plib.sam
import i2plib.exceptions
import i2plib.utils

BUFFER_SIZE = 65536

def parse_reply(data):
    return i2plib.sam.Answer(data.decode().strip())

async def get_sam_socket(sam_address=i2plib.sam.DEFAULT_ADDRESS, loop=None):
    """A couroutine used to create a new SAM socket.

    :param sam_address: (optional) SAM API address
    :param loop: (optional) event loop instance
    :return: A (reader, writer) pair
    """
    reader, writer = await asyncio.open_connection(*sam_address, loop=loop)
    writer.write(i2plib.sam.hello("3.1", "3.1"))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def dest_lookup(domain, sam_address=i2plib.sam.DEFAULT_ADDRESS, 
                      loop=None):
    """A coroutine used to lookup a full I2P destination by .i2p domain or 
    .b32.i2p address.

    :param domain: Address to be resolved, can be a .i2p domain or a .b32.i2p 
                   address.
    :param sam_address: (optional) SAM API address
    :param loop: (optional) Event loop instance
    :return: An instance of i2plib.Destination
    """
    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.naming_lookup(domain))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        writer.close()
        return i2plib.sam.Destination(reply["VALUE"])
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def new_private_key(sam_address=i2plib.sam.DEFAULT_ADDRESS, loop=None,
                      sig_type=i2plib.sam.Destination.default_sig_type):
    """A coroutine used to generate a new private key of a chosen signature
    type.

    :param sam_address: (optional) SAM API address
    :param loop: (optional) Event loop instance
    :param sig_type: (optional) Signature type
    :return: An instance of i2plib.PrivateKey
    """
    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.dest_generate(sig_type))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    writer.close()
    return i2plib.sam.PrivateKey(reply["PRIV"])

async def create_session(session_name, sam_address=i2plib.sam.DEFAULT_ADDRESS, 
                         loop=None, session_ready=None, style="STREAM",
                         signature_type=i2plib.sam.Destination.default_sig_type,
                         private_key=None, options={}, session_created=None,
                         args=()):
    """A coroutine used to create a new SAM session.

    :param session_name: Session nick name
    :param sam_address: (optional) SAM API address
    :param loop: (optional) Event loop instance
    :param session_ready: (optional) asyncio.Event instance to notify when 
                        session is ready 
    :param style: (optional) Session style, can be STREAM, DATAGRAM, RAW
    :param signature_type: (optional) If the destination is TRANSIENT, this 
                        signature type is used
    :param private_key: (optional) Private key to use in this session. Can be 
                        a base64 encoded string, i2plib.sam.PrivateKey instance
                        or None. TRANSIENT destination is used when it is None.
    :param options: (optional) A dict object with i2cp options
    :param session_created: (optional) A coroutine to be executed after the 
                        session is created. Executed with arguments
                        (loop, reader, writer, private_key, \*args)
    :param args: (optional) Arguments for a session_created coroutine
    :return: A (reader, writer) pair
    """
    logging.debug("Creating session {}".format(session_name))
    if private_key:
        if type(private_key) == i2plib.sam.PrivateKey:
            private_key = private_key
        else:
            private_key = i2plib.sam.PrivateKey(private_key)
        destination = private_key.base64
    else:
        private_key = None
        destination = i2plib.sam.TRANSIENT_DESTINATION

    options = " ".join(["{}={}".format(k, v) for k, v in options.items()])

    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.session_create(
            style, session_name, destination, options))

    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        if not private_key:
            private_key = i2plib.sam.PrivateKey(reply["DESTINATION"]) 
        logging.debug(private_key.destination.base32)
        if session_ready:
            session_ready.set()
        logging.debug("Session created {}".format(session_name))
        if session_created:
            asyncio.ensure_future(session_created(loop, reader, writer, 
                private_key, *args), loop=loop)
        return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def stream_connect(session_name, destination, 
                         sam_address=i2plib.sam.DEFAULT_ADDRESS, loop=None, 
                         session_ready=None, stream_connected=None, args=()):
    """A coroutine used to connect to a remote I2P destination.

    :param session_name: Session nick name
    :param destination: I2P destination to connect to
    :param sam_address: (optional) SAM API address
    :param loop: (optional) Event loop instance
    :param session_ready: (optional) asyncio.Event instance to notify when 
                        session is ready 
    :param stream_connected: (optional) A coroutine to be executed after the 
                        connection has been established. Executed with arguments
                        (loop, session_name, reader, writer, \*args)
    :param args: (optional) Arguments for a stream_connected coroutine
    :return: A (reader, writer) pair
    """
    logging.debug("Connecting stream {}".format(session_name))
    if isinstance(destination, str) and not destination.endswith(".i2p"):
        destination = i2plib.sam.Destination(destination)
    elif isinstance(destination, str):
        destination = await dest_lookup(destination, sam_address, loop)

    if session_ready: await session_ready.wait()
    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.stream_connect(session_name, destination.base64,
                                           silent="false"))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        logging.debug("Stream connected {}".format(session_name))
        if stream_connected:
            asyncio.ensure_future(
              stream_connected(loop, session_name, reader, writer, *args),
              loop=loop)
        return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def stream_accept(session_name, sam_address=i2plib.sam.DEFAULT_ADDRESS,
                        loop=None, session_ready=None, stream_connected=None, 
                        args=()):
    """A coroutine used to accept a connection from the I2P network.

    :param session_name: Session nick name
    :param sam_address: (optional) SAM API address
    :param loop: (optional) Event loop instance
    :param session_ready: (optional) asyncio.Event instance to notify when 
                        session is ready 
    :param stream_connected: (optional) A coroutine to be executed after the 
                        connection has been established. Executed with arguments
                        (loop, session_name, reader, writer, \*args)
    :param args: (optional) Arguments for a stream_connected coroutine
    :return: A (reader, writer) pair
    """
    if session_ready: await session_ready.wait()
    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.stream_accept(session_name, silent="false"))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        if stream_connected:
            asyncio.ensure_future(
              stream_connected(loop, session_name, reader, writer, *args), 
              loop=loop)
        return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()
