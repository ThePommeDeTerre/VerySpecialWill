from Crypto.Hash import HMAC, MD5, SHA256, SHA512


class OurHMAC:
    """Abstraction from Crypto.Hash.HMAC and some of its functionalities
    
    Attributes
    ----------
    __key : bytes
        Key to be used in HMAC operations
    __mode : str
        Cryptographic hash function to be run in methods.
        
    Methods
    -------
    compute_hmac(bytes) -> str
        Compute hmac
    verify_hmac(str, bytes) -> bool
        Verify hmac
    """

    def __init__(self, mode, key, dgst_size=512, **kwargs):
        """Constructor for HMAC object
        
        Parameters
        ----------
        __key : bytes
            Key to be used in encrypt or decrypt operations.
        __mode : str
             mode to be run in methods.  
        """

        super().__init__()
        self.__key = key
        self.__digest_size = dgst_size

        # Eventually add more modes
        self.__mode_dict = {
            'MD5': MD5,
            'SHA256': SHA256,
            'SHA512': SHA512,
        }

        if mode in self.__mode_dict.keys():
            self.__mode = self.__mode_dict[mode]
        else:
            self.__mode = SHA512

    def compute_hmac(self, pt, **kwargs) -> str:
        """Compute HMAC
        
        Parameters
        ----------
        pt : bytes
            Plaintext in bytes whose integrity needs verification
        
        Returns
        -------
        hmac : str
            Hex string representation of HMAC value
        """
        # Initialize HMAC object
        # Feed plaintext and get hex string representation
        h = HMAC.new(self.__key, digestmod=self.__mode)
        hmac = h.update(pt).hexdigest()

        if 'show' in kwargs.keys() and kwargs['show']:
            # Printing HMAC
            print('HMAC:\n{0}\n'.format(hmac))

        return hmac

    def verify_hmac(self, hmac, pt, **kwargs) -> bool:
        """Verify HMAC
        
        Parameters
        ----------
        hmac : str
            Hex string representation of HMAC value
        pt : bytes
            Plaintext in bytes whose integrity needs verification
        """
        try:
            if isinstance(pt, str):
                pt = pt.encode()

            # Initialize HMAC object, give it the plaintext
            # Give it the plaintext
            h = HMAC.new(self.__key, digestmod=self.__mode)
            h.update(pt)


            # Verify Current HMAC with a given HMAC
            h.hexverify(hmac)
            print('VERIFIED OK\n')
            return True

        except Exception as e:
            print(e)
            print('VERIFIED FAILURE')
            return False


class HMACVerificationError(Exception):
    def __init__(self, message="Authentication error"):
        self.message = message
        super().__init__(self.message)
