# SAM exceptions

class SAMException(Exception):
    pass

class CantReachPeer(SAMException):
    pass

class DuplicatedDest(SAMException):
    pass

class DuplicatedId(SAMException):
    pass

class I2PError(SAMException):
    pass

class InvalidId(SAMException):
    pass

class InvalidKey(SAMException):
    pass

class KeyNotFound(SAMException):
    pass

class PeerNotFound(SAMException):
    pass

class Timeout(SAMException):
    pass

SAM_EXCEPTIONS = {
    "CANT_REACH_PEER": CantReachPeer,
    "DUPLICATED_DEST": DuplicatedDest,
    "DUPLICATED_ID": DuplicatedId,
    "I2P_ERROR": I2PError,
    "INVALID_ID": InvalidId,
    "INVALID_KEY": InvalidKey,
    "KEY_NOT_FOUND": KeyNotFound,
    "PEER_NOT_FOUND": PeerNotFound,
    "TIMEOUT": Timeout,
}

