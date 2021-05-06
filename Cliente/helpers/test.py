#!/usr/bin/env python3

import os
from binascii import hexlify
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from OurAES import OurAES as AES
from OurHMAC import OurHMAC as HMAC

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
