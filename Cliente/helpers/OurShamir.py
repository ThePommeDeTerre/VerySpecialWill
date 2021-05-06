from Crypto.Protocol.SecretSharing import Shamir
from OurHMAC import OurHMAC, HMACVerificationError
from typing import List


class OurShamir:
    """
    Abstraction from Crypto.Protocol.SecretSharing.Shamir

    Static Methods
    --------------
    split_secret() -> List[bytes]
    combine() -> bytes
    """

    @classmethod
    def split_secret(cls, min_shares: int, n: int, key: bytes) -> List[(int, bytes)]:
        """
        Split a secret into n shares.
        The secret can be reconstructed later using just k shares out of the original n.
        Each share must be kept confidential to the person it was assigned to.
        Each share is associated to an index (starting from 1).
        A secret is split into n shares, and it is sufficient to collect k of them to reconstruct the secret.
        
        Parameters
        ----------
        min_shares : int
            The sufficient number of shares to reconstruct the secret
        n : int
            The number of shares that this method will create.
        key : bytes
             A byte string of 16 bytes.

        Raises
        ------
        ShamirCombineException : The number of shares is less than the number of required shares to recustruct secret.

        Returns
        -------
        List of n tuples. A tuple is meant for each participant and it contains two items:
            the unique index (an integer)
            the share (a byte string, 16 bytes)
        """

        if n < min_shares:
            raise ShamirSecretSplitException()
        return Shamir.split(min_shares, n, key)

    @classmethod
    def combine(cls, min_shares: int, shares: int, hmac: bytes, hmac_key: bytes, mode='SHA512') -> bytes:
        """
        Recombine and verify a secret, only if enough shares are presented.
        
        Parameters
        ----------
        min_shares : int
            The sufficient number of shares to reconstruct the secret
        shares : int
            The number of shares that this method will create.
        hmac : bytes
            HMAC of the secret before the split.
        hmac_key : bytes
            Key of the secret's HMAC. 
        mode : string
            HMAC cryptographic hash function. 

        Raises
        ------
        ShamirCombineException : The number of shares is less than the number of required shares to recustruct secret.

        Returns
        -------
        Reconstructed key.
        """

        if len(shares) < min_shares:
            raise ShamirCombineException(min_shares, len(shares))
        else:
            h = OurHMAC(mode, hmac_key)
            res = Shamir.combine(shares)

            if h.verify_hmac(hmac, res):
                return res
            else:
                raise HMACVerificationError()


class ShamirCombineException(Exception):
    def __init__(self, expected_n, received_n, message="Expected %d shares, received %d"):
        self.expected_n = expected_n
        self.received_n = received_n
        self.message = message
        super().__init__(self.message % (expected_n, received_n))


class ShamirSecretSplitException(Exception):
    def __init__(self):
        self.message = "Number of minimum required shares must be less then number of shares"
        super().__init__(self.message)
