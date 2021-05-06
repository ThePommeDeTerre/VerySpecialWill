from Crypto.Protocol.SecretSharing import Shamir
from ourHMAC import ourHMAC, HMACVerificationError

class ourShamir():
    # TODO:
    # Adicionar tipagem
    # Documentaçãob

    @staticmethod
    def split_secret(self, min_shares, shares, key):
        return Shamir.split(min_shares, shares, key)

    @staticmethod
    def combine(self, min_shares, shares, hmac, hmac_key, mode='SHA512'):
        if len(shares) < min_shares:
            raise ShamirSharingException(min_shares, len(shares))
        else:
            h = ourHMAC(mode, hmac_key)
            res = Shamir.combine(shares)

            if h.verificar_hmac(hmac, res):
                return res
            else:
                raise HMACVerificationError()

class ShamirSharingException(Exception):
    def __init__(self, expected_n, received_n, message="Expected %d shares, received %d"):
        self.expected_n = expected_n
        self.received_n = received_n
        self.message = message
        super().__init__(self.message % (expected_n, received_n))