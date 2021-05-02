from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA512
from Crypto.Random import get_random_bytes

"""
Cifrar:
Pretende-se que se cifre um ficheiro com uma cifra AES-128-CBC
Do criptograma resultante é se autenticado com HMAC-SHA512

Decifrar:
Valida-se um MAC em conjunto com a mensagem
Decifrar a mensagem com AES-128-CBC com uma chave supostamente partilhada de forma segura
"""

def CipherAndMac(plaintext, key, iv):
    
    # Preparing the cipher and HMAC object
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    h = HMAC.new(key, digestmod=SHA512)

    # Pad message and encrypt it. Result is given in bytes
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    
    # Digest plaintext and store it in hex format
    hmac = h.update(plaintext).hexdigest()
    
    # Encode it in readable format
    readable_ct = b64encode(ct_bytes).decode('utf-8')
    print('Ciphertext:\n{0}\n'.format(readable_ct))
    print(hmac)
    
    return (hmac, ct_bytes)


def VerifyAndDecipher(mac, plaintext_, ct_bytes, key, iv):
    
    # Verify integrity
    def verify():
        try:
            # Initialize HMAC object, give it the plaintext
            # Give it the plaintext
            h = HMAC.new(key, digestmod=SHA512)
            h.update(plaintext_)
            
            # Verify Current HMAC with a given HMAC
            h.hexverify(mac)
            
            print(h.hexdigest())
            print('VERIFIED OK\n')
            
            return True
        except Exception:
            print('VERIFIED FAILURE\n')
            return False
        
    # Deciphering
    def decipher():
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(ct_bytes), AES.block_size).decode('utf-8')
            print('MESSAGE:\n{0}'.format(plaintext))
        except Exception:
            print('Something went wrong on deciphering')

    if verify():
        decipher()
    
def main():
    
    # Read contents into a bytes object
    with open("text.txt", 'r') as file:
        plaintext = bytes(file.read(), 'utf-8')
    
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    (mac, ct_bytes) = CipherAndMac(plaintext, key, iv)
    
    # Window to change something in file
    input()
    
    with open("text.txt", 'r') as file:
        plaintext = bytes(file.read(), 'utf-8')
    
    VerifyAndDecipher(mac, plaintext, ct_bytes, key, iv)
    

if __name__ == '__main__':
    main()