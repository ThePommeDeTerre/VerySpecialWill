from OurAES import OurAES as AES
from OurHMAC import OurHMAC as HMAC
from OurChaCha import OurChaCha
from OurShamir import OurShamir
from Crypto.Random import get_random_bytes
from typing import Tuple, List, Union


def randomness_galore(plaintext: Union[bytes, str], crypto_type: str, hash_type: str) -> Tuple[bytes, str]:
    """randomness_galore decides cryptographic and hash functionalities based on their string representations.
    The chosen cryptographic and hash methods are then performed on the plaintext.
    Returns the ciphertext and hmac value of plaintext.

    Arguments
    ---------
    plaintext : Union[bytes, str]
        String or bytes representation of the written will.
    crypto_type : str
        String representation of the encryption method used.
    hash_type : str
        String representation of hash type used.

    Returns
    -------
    A tuple of the ciphertext and hmac of plaintext using the encryption key.
    """

    if type(plaintext) is str:
        plaintext = plaintext.encode('utf-8')

    key = get_random_bytes(32)
    nonce = get_random_bytes(24)

    # Treat cipher and encryption type
    if crypto_type.startswith('AES'):
        cmode = hash_type.split('-', maxsplit=2)[2]
        key = key[:16]
        iv = nonce[:16]
        oAES = AES(cmode)

        # TODO : ECB, CBC, CTR may have different arguments
        if cmode == 'CBC':
            bytes_ct = oAES.encrypt(plaintext, key, iv)
        elif cmode == 'ECB':
            pass
        elif cmode == 'CTR':
            pass

    elif crypto_type == 'ChaCha20':
        oCHACHA = OurChaCha()
        bytes_ct = oCHACHA.encrypt(plaintext, key, nonce)

    # Treat hash type
    if hash_type.startswith('SHA'):
        hmode = 'SHA{0}'.format(hash_type.split('-')[1])
        oHMAC = HMAC(hmode, key)

    elif hash_type == 'MD5':
        oHMAC = HMAC('MD5', key)

    # Compute HMAC
    hmac = oHMAC.compute_hmac(plaintext)

    return (bytes_ct, hmac)


def share_secrets(min_shares: int, shares: int, key: bytes) -> List[Tuple[int, bytes]]:
    shamir = OurShamir.split_secret(min_shares, shares, key)
    return shamir
