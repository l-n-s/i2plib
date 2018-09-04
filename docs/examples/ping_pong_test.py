import asyncio
import logging

import i2plib
import i2plib.utils

BUFFER_SIZE = 65536

PK_B64 = "5pJLIgm7KCqk-d0As66OdeMRj4moqtD97wOluQh5SXWCbeMfp7cr8cgHU~5rrcN6V~QcIJuqjDpYWojBdjYrc7fAA3iwWpN4fzI05yvE48oOOOLqBq7SvkpyzIhjc0hv81XQIu0LWzXXS~-B61wurJhte-LisF571BzefV5xoaRN8y3A0RidaJyuzVufPP4cKY5NeSsmTY36QRl54PG7iWJSXnLROROlg6qsjoeIV9lyNFY6ZsQKTQzEIInCZaARmNfoJP-MAsOMoj-CRDU2MXhYT~DKdI-rWH579A3wuoEjmlHtHyms7xvwUkb6kIx5UJHZmzF2Hyv3xVrpu0HSkZfUIbzz1lAc4IZ-8jnBjt2RIRpYMNnwZW09HjJXQDd7K-QvpxpK-cqNJcmWehGP7OxLt9Jj6h~8aUFHIJtFI77Zmp~YGf7cO9vCZexeLn7iByqDtfhzTP62IPu0~MJafA4efU83A-DXo8PJhOhl7rYRzH7bWRzB1rhBI~w~TsVOBQAEAAcAAL0me7gfS2H-OZ3FAsPtbUFCFpTcvfLAzBmNxxYU5TflB4KcxNe2isp2UjM7YLCuZg6OCaBSEnoag-ABpJPkY0WIjkqbFzOlowH2oVwevFHrZCFwvf1XVXsyWdupACHmmRHFCHKHMKzolO3Cye0RMH0wIEyMRyIszSThft~keXWyuEwBM4Vros-OKrKN-mBrHNbzQzTiGLS0dVMzdPvG6Pq4t1~wCWqAXrO8n7xU-xQECEpl053Ml5AJyUaCoVj3xqCd4nbrH2~kLmvd9r2nnd-Ig19BFHNALadSYbcH9JEdJZPY~7c505W1xhsrM2PcNnE4hm8DF4R~AddaILD7b2d1l~kehRZpUKdCL~THPTM20kTyN2PFqghIA4Ng-tVmXw=="
DEST_B32 = "bxwnysaa2nwykldz4ekz6u243x5ctqlcot5acmzj2huylvwr7eyq.b32.i2p"

async def ping_pong_client(loop, session_name, reader, writer):
    logging.debug("Connected, sending stuff")
    writer.write("PING".encode())
    data = await reader.read(BUFFER_SIZE)
    logging.debug(data.decode())
    writer.close()
    loop.stop()

async def ping_pong_server(loop, session_name, reader, writer):
    CLIENT_READY = asyncio.Event(loop=loop)
    asyncio.ensure_future(i2plib.create_session("ppclient",  
        sam_address=i2plib.utils.get_sam_address(), loop=loop,
        session_ready=CLIENT_READY), loop=loop)
    asyncio.ensure_future(i2plib.stream_connect("ppclient", DEST_B32, 
        sam_address=i2plib.utils.get_sam_address(), loop=loop, session_ready=CLIENT_READY, 
        stream_ready=ping_pong_client), loop=loop)


    incoming = await reader.read(BUFFER_SIZE)
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    logging.debug("Client connected: {}.b32.i2p".format(
        remote_destination.base32))

    if not data:
        logging.debug("Listening to data")
        data = await reader.read(BUFFER_SIZE)

    logging.debug(data.decode())
    writer.write(b"PONG")
    writer.close()

if __name__ == "__main__":
    sam_address = i2plib.utils.get_sam_address()

    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    READY = asyncio.Event(loop=loop)

    asyncio.ensure_future(i2plib.create_session("ppserver",
        sam_address=sam_address, loop=loop, private_key=PK_B64,
        session_ready=READY), loop=loop)
    asyncio.ensure_future(i2plib.stream_accept("ppserver", 
                          sam_address=sam_address, loop=loop, 
                          session_ready=READY, stream_ready=ping_pong_server),
                    loop=loop)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
