#!/usr/bin/env python3

import os
from base64 import b64encode, b64decode
from binascii import hexlify
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from OurAES import OurAES as AES
from OurChaCha import OurChaCha
from OurHMAC import OurHMAC as HMAC
from DecideMethod import randomness_galore, share_secrets


def main():
    # TODO : Abstract so it accepts files
    with open('text.txt', 'r') as file:
        plaintext = bytes(file.read(), 'utf-8')

    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    oAES = AES('CBC')
    oHMAC = HMAC('SHA512', key)

    # Cipher and HMAC
    ct_bytes = oAES.encrypt(plaintext, key, iv, show=True)
    hmac = oHMAC.compute_hmac(plaintext)

    # Criar segredo de shamir para 3 pessoas de forma a precisar
    # de 3 pessoas para reconstruir a chave
    shares = Shamir.split(3, 3, key)
    print("key: %s" % hexlify(key))

    for idx, share in shares:
        print("Index #%d: %s" % (idx, hexlify(share)))

    # Delete objects to make sure everything can reunite perfectly
    del key
    del oAES
    del oHMAC

    # Recombine shares
    key2 = Shamir.combine(shares)

    oAES = AES('CBC')
    oHMAC = HMAC('SHA512', key2)

    print("key: %s" % hexlify(key2))

    if oHMAC.verify_hmac(hmac, plaintext):
        pt = oAES.decrypt(ct_bytes, key2, iv, show=True)


def main2():
    # Using other encryption methods, such as chacha20 and blowfish
    # Using other cryptographic hash functions such as SHA3

    with open('text.txt', 'r') as file:
        plaintext = bytes(file.read(), 'utf-8')

    key = get_random_bytes(32)
    nonce = get_random_bytes(24)

    oCHACHA = OurChaCha()
    oHMAC = HMAC('MD5', key)
    hmac = oHMAC.compute_hmac(plaintext)
    ciphertext = oCHACHA.encrypt(plaintext, key, nonce, show=True)

    del oHMAC
    del oCHACHA

    oCHACHA = OurChaCha()
    oHMAC = HMAC('MD5', key)

    if oHMAC.verify_hmac(hmac, plaintext):
        plaintext = oCHACHA.decrypt(ciphertext, key, nonce, show=True)


def main3():
    with open('text.txt', 'r') as file:
        plaintext = bytes(file.read(), 'utf-8')

    (bytes_ct, hmac, key) = randomness_galore(plaintext, '1', '1')

    readable_ct = b64encode(bytes_ct).decode('utf-8')
    print(readable_ct)
    print(hmac)
    print(key)


if __name__ == '__main__':
    main3()
