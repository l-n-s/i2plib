import asyncio
import logging

import i2plib.sam
import i2plib.exceptions
import i2plib.utils

BUFFER_SIZE = 65536

def parse_reply(data):
    return i2plib.sam.Answer(data.decode().strip())

async def get_sam_socket(sam_address, loop):
    reader, writer = await asyncio.open_connection(*sam_address, loop=loop)
    writer.write(i2plib.sam.hello("3.1", "3.1"))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def dest_lookup(destination, sam_address=i2plib.sam.DEFAULT_ADDRESS, loop=None):
    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.naming_lookup(destination))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        writer.close()
        return i2plib.sam.Destination(reply["VALUE"])
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def create_session(session_name, sam_address=i2plib.sam.DEFAULT_ADDRESS, 
                         loop=None, session_ready=None, style="STREAM",
                         signature_type=i2plib.sam.Destination.default_sig_type,
                         private_key=None, session_created=None, *args, **kwargs):
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
    options = ""

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
                private_key, *args, **kwargs), loop=loop)
        else:
            return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def stream_connect(session_name, destination, sam_address=i2plib.sam.DEFAULT_ADDRESS, loop=None, 
                         session_ready=None, stream_ready=None, *args, **kwargs):
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
        if stream_ready:
            asyncio.ensure_future(
              stream_ready(loop, session_name, reader, writer, *args, **kwargs),
              loop=loop)
        else:
            return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()

async def stream_accept(session_name, sam_address=i2plib.sam.DEFAULT_ADDRESS,
                        loop=None, session_ready=None, stream_ready=None, 
                        *args, **kwargs):
    if session_ready: await session_ready.wait()
    reader, writer = await get_sam_socket(sam_address, loop)
    writer.write(i2plib.sam.stream_accept(session_name, silent="false"))
    reply = parse_reply(await reader.read(BUFFER_SIZE))
    if reply.ok:
        if stream_ready:
            asyncio.ensure_future(
              stream_ready(loop, session_name, reader, writer, *args, **kwargs), 
              loop=loop)
        else:
            return (reader, writer)
    else:
        raise i2plib.exceptions.SAM_EXCEPTIONS[reply["RESULT"]]()
