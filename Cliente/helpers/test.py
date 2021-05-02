import os
from Crypto.Random import get_random_bytes
from ourAES import ourAES as AES
from ourHMAC import ourHMAC as HMAC

# TODO : Abstract so it accepts files
with open('text.txt', 'r') as file:
    plaintext = bytes(file.read(), 'utf-8')

key = get_random_bytes(16)

oAES = AES('ECB', key)
oAES.alterar_modo('CBC')

oHMAC = HMAC('SHA256', key)
oHMAC.alterar_modo('SHA512')

# Cipher and HMAC
ct_bytes = oAES.cifrar(plaintext, show=True)
hmac = oHMAC.fazer_hmac(plaintext)

# Verificar e decifrar
if oHMAC.verificar_hmac(hmac, plaintext):
    pt = oAES.decifrar(ct_bytes, show=True)
