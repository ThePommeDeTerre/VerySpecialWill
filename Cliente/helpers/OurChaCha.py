from base64 import b64encode, b64decode

from Crypto.Cipher import ChaCha20


class OurChaCha:
    """Abstraction from Crypto.Cipher ChaCha20 and some of its utilities

    """

    def encrypt(self, pt, key, nonce, **kwargs):
        """Encrypt using ChaCha20 stream cipher

        """
        cifra = ChaCha20.new(key=key, nonce=nonce)
        bytes_ct = cifra.encrypt(pt)

        # Kwarg routines
        if 'show' in kwargs.keys() and kwargs['show']:
            # Ciphertext in printable format
            readable_ct = b64encode(bytes_ct).decode('utf-8')
            print('CIPHERTEXT:\n{0}\n'.format(readable_ct))

        return bytes_ct

    def decrypt(self, ct, key, nonce, **kwargs):
        """Decrypt using ChaCha20 stream cipher

        """
        cifra = ChaCha20.new(key=key, nonce=nonce)
        pt = cifra.decrypt(ct).decode('utf-8')

        # Kwarg routines
        if 'show' in kwargs.keys() and kwargs['show']:
            print('PLAINTEXT:\n{0}\n'.format(pt))

        return pt
