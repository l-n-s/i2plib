import sys
import asyncio
from urllib.parse import urlparse

import i2plib

async def http_get(sam_address, loop, session_name, url):
    url = urlparse(url)
    r, w = await i2plib.stream_connect(session_name, url.netloc, 
                                       sam_address=sam_address, loop=loop)

    w.write("GET {} HTTP/1.0\nHost: {}\r\n\r\n".format(
        url.path, url.netloc).encode())

    buflen, resp = 4096, b""
    while 1:
        data = await r.read(buflen)
        if len(data) > 0:
            resp += data
        else:
            break

    w.close()
    try:
        return resp.split(b"\r\n\r\n", 1)[1].decode()
    except IndexError:
        return resp.decode()

async def wget(sam_address, loop, url):
    session_name = "wget"
    await i2plib.create_session(session_name, sam_address=sam_address, loop=loop)

    res = await http_get(sam_address, loop, session_name, url)
    print(res)

if __name__ == "__main__":
    sam_address = i2plib.get_sam_address()

    if len(sys.argv) == 2:
        url = sys.argv[1] 
        if not url.startswith("http://"):
            url = "http://" + url

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wget(sam_address, loop, url))
        loop.stop()
        loop.close()
    else:
        print("""Fetch I2P URL. Usage: 
            python wget.py http://site.i2p/""")
