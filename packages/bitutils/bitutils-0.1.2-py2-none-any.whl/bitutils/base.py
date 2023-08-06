def to_bytes(value, encoding='utf8'):
    """
    cast string to bytes() like object, but for python2 support it's bytearray copy
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, str):
        return value.encode(encoding)
    elif isinstance(value, bytearray):
        return bytes(value)
    else:
        raise TypeError("Not a string or bytes like object")


__b43chars = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ$*+-./:'


def base43(v):
    """ encode v, which is a string of bytes, to base58."""
    long_value = 0

    for (i, c) in enumerate(v[::-1]):
        long_value += (256 ** i) * c

    result = bytearray()

    while long_value >= 43:
        div, mod = divmod(long_value, 43)
        result.append(__b43chars[mod])
        long_value = div

    result.append(__b43chars[long_value])

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    n_pad = 0
    for c in v:
        if c == 0x00:
            n_pad += 1
        else:
            break
    result.extend([__b43chars[0]] * n_pad)
    result.reverse()

    return result.decode('ascii')


__b58chars = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58(v):
    """ encode v, which is a string of bytes, to base58."""
    long_value = 0

    for (i, c) in enumerate(v[::-1]):
        long_value += (256 ** i) * c

    result = bytearray()

    while long_value >= 58:
        div, mod = divmod(long_value, 58)
        result.append(__b58chars[mod])
        long_value = div

    result.append(__b58chars[long_value])

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    n_pad = 0
    for c in v:
        if c == 0x00:
            n_pad += 1
        else:
            break
    result.extend([__b58chars[0]] * n_pad)
    result.reverse()

    return result.decode('ascii')
