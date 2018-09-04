"""
Example HTTP server tunnel
""" 
from multiprocessing import Process
import os
import logging
import http.server
import argparse
import asyncio

import i2plib
import i2plib.utils

def serve_directory(server_address, path):
    os.chdir(path)
    http.server.SimpleHTTPRequestHandler.protocol_version = "HTTP/1.0"
    with http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()

def main(args):
    sam_address = i2plib.utils.get_sam_address()
    server_address = ('127.0.0.1', i2plib.utils.get_free_port())

    if not os.path.isdir(args.web_directory):
        raise OSError("No such directory {}".format(args.web_directory))

    if args.key:
        priv = i2plib.PrivateKey(path=args.key)
    else:
        priv = i2plib.utils.get_new_private_key(sam_address=sam_address)

    logging.info("Listening: {}.b32.i2p".format(priv.destination.base32))
    logging.info("Server: {}:{}".format(server_address[0], server_address[1]))

    # run HTTP server
    http_server_thread = Process(target=serve_directory, 
                args=(server_address, args.web_directory))
    http_server_thread.daemon = True
    http_server_thread.start()

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(i2plib.server_tunnel(server_address, 
        loop=loop, private_key=priv.base64, sam_address=sam_address), loop=loop)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('web_directory', metavar="WEBROOT", 
            help="Directory with files")
    parser.add_argument('--debug', '-d', action='store_true',
                       help='Debugging')
    parser.add_argument('--key', '-k', default='', metavar='PRIVATE_KEY',
                        help='Path to private key')
    args = parser.parse_args()

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)

    main(args)

