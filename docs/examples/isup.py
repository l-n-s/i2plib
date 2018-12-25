import os
import sys
import asyncio

import i2plib

async def check_peer(sam_address, loop, session_name, domain):
    try:
        r, w = await i2plib.stream_connect(session_name, domain, 
                                          sam_address=sam_address, loop=loop)
        w.close()
        return (domain, "up")
    except i2plib.CantReachPeer:
        return (domain, "down")


async def isup(sam_address, loop, domains):
    session_name = "checker"
    await i2plib.create_session(session_name, sam_address=sam_address, loop=loop)

    tasks = [check_peer(sam_address, loop, session_name, d) for d in domains]
    result = await asyncio.gather(*tasks, loop=loop)

    for r in result:
        print("{} is {}".format(*r))

if __name__ == "__main__":
    sam_address = i2plib.get_sam_address()


    if len(sys.argv) >= 2:
        if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
            with open(sys.argv[1], "r") as f: 
                domains = [d.strip() for d in f.readlines()]
        else:
            domains = sys.argv[1:] 

        loop = asyncio.get_event_loop()
        loop.run_until_complete(isup(sam_address, loop, domains))
        loop.stop()
        loop.close()

    else:
        print("""Check if I2P hosts are up. Usage: 
            python isup.py site.i2p site2.i2p site3.i2p
            python isup.py domain_list.txt""")
        exit()
