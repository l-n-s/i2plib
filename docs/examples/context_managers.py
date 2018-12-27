import asyncio
import logging

import i2plib

BUFFER_SIZE = 65536

PK_B64 = "5pJLIgm7KCqk-d0As66OdeMRj4moqtD97wOluQh5SXWCbeMfp7cr8cgHU~5rrcN6V~QcIJuqjDpYWojBdjYrc7fAA3iwWpN4fzI05yvE48oOOOLqBq7SvkpyzIhjc0hv81XQIu0LWzXXS~-B61wurJhte-LisF571BzefV5xoaRN8y3A0RidaJyuzVufPP4cKY5NeSsmTY36QRl54PG7iWJSXnLROROlg6qsjoeIV9lyNFY6ZsQKTQzEIInCZaARmNfoJP-MAsOMoj-CRDU2MXhYT~DKdI-rWH579A3wuoEjmlHtHyms7xvwUkb6kIx5UJHZmzF2Hyv3xVrpu0HSkZfUIbzz1lAc4IZ-8jnBjt2RIRpYMNnwZW09HjJXQDd7K-QvpxpK-cqNJcmWehGP7OxLt9Jj6h~8aUFHIJtFI77Zmp~YGf7cO9vCZexeLn7iByqDtfhzTP62IPu0~MJafA4efU83A-DXo8PJhOhl7rYRzH7bWRzB1rhBI~w~TsVOBQAEAAcAAL0me7gfS2H-OZ3FAsPtbUFCFpTcvfLAzBmNxxYU5TflB4KcxNe2isp2UjM7YLCuZg6OCaBSEnoag-ABpJPkY0WIjkqbFzOlowH2oVwevFHrZCFwvf1XVXsyWdupACHmmRHFCHKHMKzolO3Cye0RMH0wIEyMRyIszSThft~keXWyuEwBM4Vros-OKrKN-mBrHNbzQzTiGLS0dVMzdPvG6Pq4t1~wCWqAXrO8n7xU-xQECEpl053Ml5AJyUaCoVj3xqCd4nbrH2~kLmvd9r2nnd-Ig19BFHNALadSYbcH9JEdJZPY~7c505W1xhsrM2PcNnE4hm8DF4R~AddaILD7b2d1l~kehRZpUKdCL~THPTM20kTyN2PFqghIA4Ng-tVmXw=="
DEST_B32 = "bxwnysaa2nwykldz4ekz6u243x5ctqlcot5acmzj2huylvwr7eyq.b32.i2p"

async def server(sam_address, loop, ready):
    async with i2plib.Session("ppserver", sam_address=sam_address, loop=loop, destination=PK_B64):
        ready.release()
        async with i2plib.StreamAcceptor("ppserver", sam_address=sam_address, loop=loop) as s:
            incoming = await s.read(BUFFER_SIZE)
            dest, request = incoming.split(b"\n", 1)
            remote_destination = i2plib.Destination(dest.decode())
            if not request:
                request = await s.read(BUFFER_SIZE)
            assert request == b"PING"
            s.write(b"PONG")

async def ping_pong(sam_address, loop):
    ready = asyncio.Lock(loop=loop)
    await ready.acquire()
    asyncio.ensure_future(server(sam_address, loop, ready), loop=loop)
    await ready.acquire()

    async with i2plib.Session("ppclient", sam_address=sam_address, loop=loop):
        async with i2plib.StreamConnection("ppclient", DEST_B32, sam_address=sam_address, loop=loop) as c:
            c.write(b"PING")
            response = await c.read(BUFFER_SIZE)
            assert response == b"PONG"

    await asyncio.sleep(0.0001) # wait until all tasks are completed


if __name__ == "__main__":
    sam_address = i2plib.get_sam_address()

    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(ping_pong(sam_address, loop))
    loop.stop()
    loop.close()
