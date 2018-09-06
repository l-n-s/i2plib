import socket
from base64 import b64decode, b64encode, b32encode
from hashlib import sha256
import struct
import random
import string
import re

from .exceptions import SAM_EXCEPTIONS

I2P_B64_CHARS = "-~"

SAM_BUFSIZE = 4096
DEFAULT_ADDRESS = ("127.0.0.1", 7656)
DEFAULT_MIN_VER = "3.1"
DEFAULT_MAX_VER = "3.1"
TRANSIENT_DESTINATION = "TRANSIENT"

VALID_BASE32_ADDRESS = re.compile(r"^([a-zA-Z0-9]{52}).b32.i2p$")
VALID_BASE64_ADDRESS = re.compile(r"^([a-zA-Z0-9-~=]{516,528})$")

class Answer(object):
    """Parse answer from SAM bridge to an object"""
    def __init__(self, s):
        self.opts = {}
        if type(s) != str:
            self._reply_string = s.decode().strip()
        else:
            self._reply_string = s

        self.cmd, opts = self._reply_string.split(" ", 1)
        for v in opts.split(" ")[1:]:
            data = v.split("=", 1) if "=" in v else (v, True)
            self.opts[data[0]] = data[1]

    def __getitem__(self, key):
        return self.opts[key]

    @property
    def ok(self):
        return self["RESULT"] == "OK"

    def __repr__(self):
        return self._reply_string

def get_socket(sam_address=None):
    """Return new SAM socket"""
    sam_address = sam_address or DEFAULT_ADDRESS
    sam_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sam_socket.connect(sam_address)
    sam_socket.send(hello(DEFAULT_MIN_VER, DEFAULT_MAX_VER))
    a = get_response(sam_socket)
    if a.ok:
        return sam_socket
    else:
        raise SAM_EXCEPTIONS[a["RESULT"]]()

def lookup(sam_socket, name):
    """Lookup destination by name"""
    sam_socket.send(naming_lookup(name))
    a = get_response(sam_socket)
    if a.ok:
        return Destination(a["VALUE"])
    else:
        raise SAM_EXCEPTIONS[a["RESULT"]]()

def generate_session_id(length=6):
    """Generate random session id"""
    rand = random.SystemRandom()
    sid = [rand.choice(string.ascii_letters) for _ in range(length)]
    return "i2plib-" + "".join(sid)

def get_response(sam_socket):
    """Read answer from SAM API"""
    return Answer(sam_socket.recv(SAM_BUFSIZE))


# SAM request messages

def hello(min_version, max_version):
    return "HELLO VERSION MIN={} MAX={}\n".format(min_version, 
            max_version).encode()

def session_create(style, session_id, destination, options=""):
    return "SESSION CREATE STYLE={} ID={} DESTINATION={} {}\n".format(
            style, session_id, destination, options).encode()


def stream_connect(session_id, destination, silent="false"):
    return "STREAM CONNECT ID={} DESTINATION={} SILENT={}\n".format(
            session_id, destination, silent).encode()

def stream_accept(session_id, silent="false"):
    return "STREAM ACCEPT ID={} SILENT={}\n".format(session_id, silent).encode()

def stream_forward(session_id, port, options=""):
    return "STREAM FORWARD ID={} PORT={} {}\n".format(
            session_id, port, options).encode()



def naming_lookup(name):
    return "NAMING LOOKUP NAME={}\n".format(name).encode()

def dest_generate(signature_type):
    return "DEST GENERATE SIGNATURE_TYPE={}\n".format(signature_type).encode()

class Destination(object):
    """I2P destination

    https://geti2p.net/spec/common-structures#destination

    :param data: (optional) Base64 encoded data or binary data 
    """

    ECDSA_SHA256_P256 = 1
    ECDSA_SHA384_P384 = 2
    ECDSA_SHA512_P521 = 3
    EdDSA_SHA512_Ed25519 = 7

    default_sig_type = EdDSA_SHA512_Ed25519

    def __init__(self, data=None):
        #: Binary private key data
        self.data = bytes() 
        #: Base64 encoded private key data
        self.base64 = ""    
        
        if data:
            if type(data) == bytes:
                self.data = data
                self.base64 = b64encode(self.data, 
                        altchars=I2P_B64_CHARS.encode()).decode()
            elif type(data) == str:
                self.data = b64decode(data, altchars=I2P_B64_CHARS, validate=True)
                self.base64 = data

    def __repr__(self):
        return "<Destination: {}>".format(self.base32)

    @property
    def base32(self):
        """Base32 destination hash of this destination"""
        desthash = sha256(self.data).digest()
        return b32encode(desthash).decode()[:52].lower()
    
class PrivateKey(object):
    """I2P private key

    https://geti2p.net/spec/common-structures#keysandcert

    :param data: (optional) Base64 encoded data or binary data 
    :param path: (optional) Path to a file with binary private key data
    """
    _pubkey_size = 256
    _signkey_size = 128
    _min_cert_size = 3

    def __init__(self, data=None, path=None):
        #: Binary private key data
        self.data = bytes() 
        #: Base64 encoded private key data
        self.base64 = ""    
        #: i2plib.Destination object of the private key
        self.destination = None    

        if path:
            with open(path, "rb") as f: data = f.read()
        if data:
            if type(data) == bytes:
                self.data = data
                self.base64 = b64encode(self.data, 
                        altchars=I2P_B64_CHARS.encode()).decode()
            elif type(data) == str:
                self.data = b64decode(data, altchars=I2P_B64_CHARS, validate=True)
                self.base64 = data

            cert_len = struct.unpack("!H", self.data[385:387])[0]
            self.destination = Destination(data=self.data[:387+cert_len])

    def __repr__(self):
        return "<PrivateKey: {}>".format(self.destination.base32)



class StreamSession(object):

    def __init__(self, sam_address=DEFAULT_ADDRESS, \
            session_id=None, destination=TRANSIENT_DESTINATION, options="", \
            min_ver=DEFAULT_MIN_VER, max_ver=DEFAULT_MAX_VER):
        self.sam_address = sam_address
        self.min_ver = min_ver
        self.max_ver = max_ver
        self.session_id = session_id or generate_session_id()
        self._session_socket = get_socket(self.sam_address)
        self._session_socket.send(
            session_create("STREAM", self.session_id, destination, options))
        a = get_response(self._session_socket)

        if a.ok:
            self.destination = a["DESTINATION"]
        else:
            raise SAM_EXCEPTIONS[a["RESULT"]]()

    def _get_socket(self):
        """New socket for this session"""
        return get_socket(self.sam_address)

    def connect(self, dest):
        """Return new I2P stream to destination"""
        sam_socket = self._get_socket()
        sam_socket.send(stream_connect(self.session_id, dest, silent="false"))
        a = get_response(sam_socket)
        if a.ok:
            return sam_socket
        else:
            raise SAM_EXCEPTIONS[a["RESULT"]]()

    def accept(self):
        """Return new accepting socket"""
        sam_socket = self._get_socket()
        sam_socket.send(stream_accept(self.session_id, silent="false"))
        return sam_socket

    def forward(self, session_id, port, options=""):
        sam_socket = self._get_socket()
        sam_socket.send(stream_forward(self.session_id, port, options))
        return sam_socket

