import hashlib

from bitutils import to_bytes


def sha256(value):
    value = to_bytes(value, 'utf8')
    return bytes(hashlib.sha256(value).digest())

