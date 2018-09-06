import socket
import os
import i2plib.sam

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 0))
    free_port = s.getsockname()[1]
    s.close()
    return free_port


def address_from_string(address_string):
    """Address tuple from host:port string"""
    address = address_string.split(":")
    return (address[0], int(address[1]))

def get_sam_address():
    """Get SAM address from environment variable SAM_ADDRESS, or use a default 
       value"""
    if os.getenv("SAM_ADDRESS"):
        return address_from_string(os.getenv("SAM_ADDRESS"))
    else:
        return i2plib.sam.DEFAULT_ADDRESS

def get_new_private_key(sam_address=i2plib.sam.DEFAULT_ADDRESS, 
                        sig_type=i2plib.sam.Destination.default_sig_type):
    """Generates new I2P destination of a chosen signature type"""
    sam_socket = i2plib.sam.get_socket(sam_address)
    sam_socket.send(i2plib.sam.dest_generate(sig_type))
    a = i2plib.sam.get_response(sam_socket)
    sam_socket.close()
    return i2plib.sam.PrivateKey(a['PRIV'])

