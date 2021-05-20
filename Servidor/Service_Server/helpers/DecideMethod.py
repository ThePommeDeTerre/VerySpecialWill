from OurAES import OurAES as AES
from OurHMAC import OurHMAC as HMAC
from OurChaCha import OurChaCha
from OurShamir import OurShamir
from Crypto.Random import get_random_bytes
from typing import Tuple, List, Union


def randomness_galore(plaintext: Union[bytes, str], crypto_type: str, hash_type: str) -> Tuple[bytes, str, bytes]:
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
        '2': 'SHA256',
        '3': 'SHA512'
        # Storing MD5 association is not necessary
    }

    if type(plaintext) is str:
        plaintext = plaintext.encode('utf-8')

    key = get_random_bytes(32)
    nonce = get_random_bytes(24)

    ctype = int(crypto_type)
    htype = int(hash_type)

    # Treat cipher and encryption type
    if 0 < ctype <= 3:

        cmode = c[crypto_type]
        key = key[:16]
        iv = nonce[:16]
        oAES = AES(cmode)

        # TODO : ECB, CBC, CTR may have different arguments
        if cmode == 'CBC':
            bytes_ct = oAES.encrypt(plaintext, key, iv)
        elif cmode == 'ECB':
            bytes_ct = oAES.encrypt(plaintext, key)
            pass
        elif cmode == 'CTR':
            pass

    elif ctype is 4:
        oCHACHA = OurChaCha()
        bytes_ct = oCHACHA.encrypt(plaintext, key, nonce)

    # Treat hash type
    if 1 < htype <= 3:
        hmode = h[hash_type]
        oHMAC = HMAC(hmode, key)

    elif htype is 1:
        oHMAC = HMAC('MD5', key)

    # Compute HMAC
    hmac = oHMAC.compute_hmac(plaintext)

    return bytes_ct, hmac, key


def share_secrets(min_shares: int, shares: int, key: bytes) -> List[Tuple[int, bytes]]:
    shamir = OurShamir.split_secret(min_shares, shares, key)
    return shamir
