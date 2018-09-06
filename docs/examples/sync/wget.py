import sys
from urllib.parse import urlparse

from i2plib.sam import generate_session_id, lookup, get_socket, StreamSession

def http_get(url, sam_address):
    url = urlparse(url)
    s_id = generate_session_id()
    ss = StreamSession(session_id=s_id, sam_address=sam_address)

    dest = lookup(get_socket(sam_address=sam_address), url.netloc)

    # connect to remote server, returns socket to use
    client_sock = ss.connect(dest.base64)
    client_sock.send("GET {} HTTP/1.0\nHost: {}\r\n\r\n".format(
        url.path, url.netloc).encode())

    buflen, resp = 4096, b""
    while 1:
        data = client_sock.recv(buflen)
        if len(data) > 0:
            resp += data
        else:
            break

    resp = resp.decode()
    try:
        return resp.split("\r\n\r\n", 1)[1]
    except IndexError:
        return resp

if __name__ == "__main__":
    if len(sys.argv) == 2:
        url = sys.argv[1] if sys.argv[1].startswith("http://") else "//"+sys.argv[1]
    else:
        url = "http://irkvgdnlc6tidoqomre4qr7q4w4qcjfyvbovatgyolk6d4uvcyha.b32.i2p/uploads/BSD"

    r = http_get(url, i2plib.get_sam_address())

    print(r)
