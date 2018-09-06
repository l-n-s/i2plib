import sys
import asyncio

import i2plib

async def resolve(sam_address, loop, domain):
    try:
        dest = await i2plib.dest_lookup(domain, sam_address, loop)
        print("Domain: \n{}\n".format(domain))
        print("Full destination: \n{}\n".format(dest.base64))
        print("B32 address: \n{}.b32.i2p\n".format(dest.base32))
    except i2plib.InvalidKey:
        print("Not found")

if __name__ == "__main__":
    sam_address = i2plib.get_sam_address()

    if len(sys.argv) == 2:
        domain = sys.argv[1] 

        loop = asyncio.get_event_loop()
        loop.run_until_complete(resolve(sam_address, loop, domain))
        loop.stop()
        loop.close()

    else:
        print("Usage: resolve.py [.i2p domain]")
        exit()

