import sys

from i2plib.sam import lookup, get_socket
import i2plib.exceptions

if __name__ == "__main__":
    if len(sys.argv) == 2:
        domain = sys.argv[1] 
        try:
            r = lookup(get_socket(), domain)
            print("Domain: \n{}\n".format(domain))
            print("Full destination: \n{}\n".format(r.base64))
            print("B32 address: \n{}.b32.i2p\n".format(r.base32))
        except i2plib.exceptions.InvalidKey:
            print("Domain not found")
    else:
        print("Usage: resolve.py [.i2p domain]")
        exit()

