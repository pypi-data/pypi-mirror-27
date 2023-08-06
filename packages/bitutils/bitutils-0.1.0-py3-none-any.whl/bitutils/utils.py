import hashlib





def hex2bytes(x):
    """
    py2-py3 aware wrapper to "bytes.fromhex()" func
    :param x: str
    :rtype: bytes
    """
    if isinstance(x, str):
        return bytes.fromhex(x)
    elif isinstance(x, (list, tuple, map)):
        return [hex2bytes(sub) for sub in x]
    else:
        raise TypeError('Unexpected type: ' + str(type(x)))





ADDR_TYPE_P2PKH = 0




def hash160(value):
    hash = hashlib.new('ripemd160')
    hash.update(sha256(value))
    return hash.digest()


def Hash(x):
    return bytes(sha256(sha256(to_bytes(x, 'utf8'))))


def hash160_to_b58(h160, addrtype):
    s = bytes([addrtype])
    s += h160
    return base58(s + Hash(s)[0:4])


def hash160_to_p2pkh(h160):
    return hash160_to_b58(h160, ADDR_TYPE_P2PKH)


def public_key_to_p2pkh(public_key):
    return hash160_to_p2pkh(hash160(public_key))


def pubkey_to_address(type, pubkey):
    if type == 'p2pkh':
        return public_key_to_p2pkh(hex2bytes(pubkey))
    elif type == 'p2wpkh':
        return hash_to_segwit_addr(hash_160(bfh(pubkey)))
    elif type == 'p2wpkh-p2sh':
        scriptSig = p2wpkh_nested_script(pubkey)
        return hash160_to_p2sh(hash_160(bfh(scriptSig)))
    else:
        raise NotImplementedError(type)


print(pubkey_to_address('p2pkh', '121212'))
