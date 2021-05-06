from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA512, SHA256, MD5

class ourHMAC():
    """
    Abstraction from Crypto.Hash.HMAC and some of its functionalities
    
    Attributes
    ----------
    __key : bytes
        Key to be used in HMAC operations
    __mode : int (AES.MODE)
        Cryptographic hash function to be run in methods.
        
    Methods
    -------
    fazer_hmac() -> str
        Compute hmac
    verificar_hmac() -> str
        Verify hmac
    alterar_modo() -> None
        Change cryptographic hash function in HMAC object
    """
    
    def __init__(self, mode, key, **kwargs):
        """Constructor for HMAC object
        
        Parameters
        ----------
        __key : bytes
            Key to be used in encrypt or decrypt operations.
        __mode : int (AES.MODE)
             mode to be run in methods.  
        """
        
        super().__init__()
        self.__key = key
        
        # Eventually add more modes
        self.__mode_dict = {
            'MD5' : MD5,
            'SHA256' : SHA256,
            'SHA512' : SHA512
        }
        
        if mode in self.__mode_dict.keys():
            self.__mode = self.__mode_dict[mode]
        else:
            self.__mode = SHA512
        
    def fazer_hmac(self, pt, **kwargs) -> str:
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

    def verificar_hmac(self, hmac, pt, **kwargs) -> bool:
        """Verify HMAC
        
        Parameters
        ----------
        hmac : str
            Hex string representation of HMAC value
        pt : bytes
            Plaintext in bytes whose integrity needs verification
        """
        try:
            # Initialize HMAC object, give it the plaintext
            # Give it the plaintext
            h = HMAC.new(self.__key, digestmod=self.__mode)
            h.update(pt)
                
            # Verify Current HMAC with a given HMAC
            h.hexverify(hmac)
            print('VERIFIED OK\n')
            return True
        
        except Exception:
            print('VERIFIED FAILURE')
            return False
    
    def alterar_modo(self, mode, **kwargs) -> None:
        """Change cryptographic hash function for HMAC object
        
        Parameters
        ----------
        mode : bytes
            String representation of a valid cryptographic hash function
        """
        
        if mode in self.__mode_dict:
            self.__mode = self.__mode_dict[mode]
            
            print('Cryptographic hash function changed to {0}\n'.format(mode))
        else:
            print('Unrecognized cryptographic hash function')

class HMACVerificationError(Exception):
    def __init__ (self, message="Authentication error"):
        self.message = message
        super().__init__(self.message)