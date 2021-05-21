from helpers.OurAES import OurAES as AES
from helpers.OurHMAC import OurHMAC as HMAC
from helpers.OurChaCha import OurChaCha
from helpers.OurShamir import OurShamir
from Crypto.Random import get_random_bytes
from typing import Tuple, List, Union
from Crypto.Hash import SHA256
from helpers.OurGenKey import OurGenKey as RSA
from base64 import b64encode, b64decode



def randomness_galore(plaintext: Union[bytes, str], crypto_type: str, hash_type: str,date :str) -> Tuple[bytes, str, bytes]:
    """randomness_galore decides cryptographic and hash functionalities based on their string representations.
    The chosen cryptographic and hash methods are then performed on the plaintext.
    Returns the ciphertext , plaintext's HMAC and key used.

    Arguments
    ---------
    plaintext : Union[bytes, str]
        String or bytes representation of the written will.
    crypto_type : str
        A number in string representation of the encryption method used.
    hash_type : str
        A number in string representation of hash type used.

    Returns
    -------
    A tuple consisting of the ciphertext, plaintext's HMAC and key used
    """

    c = {
        '1': 'CBC',
        '2': 'ECB',
        '3': 'CTR',
        # Storing ChaCha20 association is not necessary
    }

    h = {
        '1': 'MD5',
        '2': 'SHA256',
        '3': 'SHA512'
        # Storing MD5 association is not necessary
    }

    if type(plaintext) is str:
        plaintext = plaintext.encode('utf-8')

    # We use the chosen date as part of the key
    # this allow us to only be able to decypher on that day
    date_hash = SHA256.new(date.encode()).digest()
    key = get_random_bytes(16)
    nonce = date_hash[0:24]

    ctype = int(crypto_type)
    htype = int(hash_type)

    # the last 16 bytes of the hash of the date are part of the key
    key = key[:16] + date_hash[-16:]

    # Treat cipher and encryption type
    if 0 < ctype <= 3:

        cmode = c[crypto_type]
        # the first 16 are used as the iv depending on the cypher
        nonce = nonce[0:16]
        oAES = AES(cmode)

        # TODO : ECB, CBC, CTR may have different arguments
        if cmode == 'CBC':
            bytes_ct = oAES.encrypt(plaintext, key, nonce)
        elif cmode == 'ECB':
            bytes_ct = oAES.encrypt(plaintext, key)
            pass
        elif cmode == 'CTR':
            pass

    elif ctype == 4:
        # the first 24 are used as the nonce
        oCHACHA = OurChaCha()
        bytes_ct = oCHACHA.encrypt(plaintext, key, nonce)

    # Treat hash type
    if 1 < htype <= 3:
        hmode = h[hash_type]
        oHMAC = HMAC(hmode, key)

    elif htype == 1:
        oHMAC = HMAC('MD5', key)

    # Compute HMAC
    hmac = oHMAC.compute_hmac(plaintext)

    # Compute pub key
    pair = RSA.gen_key_pair()
    public = RSA.extract_public(pair)

    signature = RSA.sign_will(pair, plaintext)

    bytes_ct = b64encode(bytes_ct).decode('utf-8')
    public = b64encode(public).decode('utf-8')
    signature = b64encode(signature).decode('utf-8')
    nonce = b64encode(nonce).decode('utf-8')

    return bytes_ct, hmac, key[0:16], public, signature, nonce,date_hash


def share_secrets(min_shares: int, shares: int, key: bytes) -> List[Tuple[int, bytes]]:
    shamir = OurShamir.split_secret(min_shares, shares, key)
    return shamir

def decrypt_will(will_message, will_hmac, will_sign,will_pub, cypher_id, hash_id,current_date,secrets):
    c = {
        1: 'CBC',
        2: 'ECB',
        3: 'CTR',
        # Storing ChaCha20 association is not necessary
    }

    h = {
        1: 'MD5',
        2: 'SHA256',
        3: 'SHA512'
        # Storing MD5 association is not necessary
    }

    date_hash = SHA256.new(current_date.encode()).digest()
    date_hash[-16:]

    ctype = int(cypher_id)
    htype = int(hash_id)

    nonce = date_hash[0:24]

    key_pt1 = OurShamir.simple_combine(secrets)
    key_total = key_pt1 + date_hash[-16:]

    will_message = b64decode(will_message)
    will_sign = b64decode(will_sign)
    will_pub = b64decode(will_pub)

    
    # Treat cipher and encryption type
    if 0 < ctype <= 3:
        cmode = c[cypher_id]
        # the first 16 are used as the iv depending on the cypher
        nonce = nonce[0:16]
        oAES = AES(cmode)
        
        # TODO : ECB, CBC, CTR may have different arguments
        if cmode == 'CBC':
            str_pt = oAES.decrypt(will_message, key_total, nonce)
        elif cmode == 'ECB':
            str_pt = oAES.decrypt(will_message, key_total)
            pass
        elif cmode == 'CTR':
            pass

    elif ctype == 4:
        # the first 24 are used as the nonce
        oCHACHA = OurChaCha()
        str_pt = oCHACHA.encrypt(will_message, key_total, nonce)

    # Treat hash type
    if 1 < htype <= 3:
        hmode = h[hash_id]
        oHMAC = HMAC(hmode, key_total)

    elif htype == 1:
        oHMAC = HMAC('MD5', key_total)
    
    valid = oHMAC.verify_hmac(will_hmac,str_pt)
    valid = valid and RSA.verify_will(will_pub,str_pt,will_sign)

    return str_pt,valid
