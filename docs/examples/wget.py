import sys
import asyncio
from urllib.parse import urlparse

import i2plib

async def wget(sam_address, loop, url):
    session_name = "wget"
    url = urlparse(url)
    buflen, resp = 4096, b""

    async with i2plib.Session(session_name, sam_address=sam_address, loop=loop):
        async with i2plib.StreamConnection(session_name, url.netloc, loop=loop, 
                                           sam_address=sam_address) as c:
            c.write("GET {} HTTP/1.0\nHost: {}\r\n\r\n".format(
                url.path, url.netloc).encode())

            while 1:
                data = await c.read(buflen)
                if len(data) > 0:
                    resp += data
                else:
                    break
    try:
        print(resp.split(b"\r\n\r\n", 1)[1].decode())
    except IndexError:
        print(resp.decode())

if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1] 
        if not url.startswith("http://"):
            url = "http://" + url

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wget(i2plib.get_sam_address(), loop, url))
        loop.stop()
        loop.close()
    else:
        print("""Fetch I2P URL. Usage: 
            python wget.py http://site.i2p/""")
