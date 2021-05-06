#!/usr/bin/env python3

import os
from binascii import hexlify
from Crypto.Random import get_random_bytes
from Crypto.Protocol.SecretSharing import Shamir
from ourAES import ourAES as AES
from ourHMAC import ourHMAC as HMAC


# TODO : Abstract so it accepts files
with open('text.txt', 'r') as file:
    plaintext = bytes(file.read(), 'utf-8')

key = get_random_bytes(16)

oAES = AES('CBC', key)
oHMAC = HMAC('SHA512', key)

# Cipher and HMAC
ct_bytes = oAES.cifrar(plaintext, show=True)
hmac = oHMAC.fazer_hmac(plaintext)

# Criar segredo de shamir para 3 pessoas de forma a precisar
# de 3 pessoas para reconstruir a chave
shares = Shamir.split(3, 3, key)
print("key: %s" % hexlify(key))

for idx, share in shares:
    print("Index #%d: %s" % (idx, hexlify(share)))

s = shares[0:1] 


key = Shamir.combine(s)
print("key: %s" %  hexlify(key))
# dividir em métodos
# Verificar e decifrar
#if oHMAC.verificar_hmac(hmac, plaintext):
#    pt = oAES.decifrar(ct_bytes, show=True)
