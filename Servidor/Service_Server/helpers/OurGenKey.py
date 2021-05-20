from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA


class OurGenKey:

    @classmethod
    def gen_key_pair(cls):
        return RSA.generate(2048)

    @classmethod
    def extract_public(cls, pair) -> bytes:
        return pair.publickey().exportKey()

    @classmethod
    def sign_will(cls, pair, plaintext) -> bytes:
        oHASH = SHA256.new(plaintext)
        signature = pkcs1_15.new(pair).sign(oHASH)

        return signature

    @classmethod
    def verify_will(cls, publickey, plaintext, signature):

        if isinstance(publickey, bytes):
            publickey = RSA.importKey(publickey)

        oHASH = SHA256.new(plaintext)
        try:
            pkcs1_15.new(publickey).verify(oHASH, signature)
            print('VERIFIED OK')
            return True
        except ValueError:
            print('VERIFICATION FAILURE')
            return False
