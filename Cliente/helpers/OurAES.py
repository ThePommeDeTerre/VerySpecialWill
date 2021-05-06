import os.path as osp
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class ourAES():    
    """Abstraction from Crypto.Cipher.AES and some of its utilities
    
    Attributes
    ----------
    __key : bytes
        Key to be used in encrypt or decrypt operations.
    __mode : int (AES.MODE)
        AES mode to be run in methods.
    iv : bytes
        Initialization vector for certain cipher modes.
    
    Methods
    -------
    cifrar() -> bytes
        Encrypt a message
    decifrar() -> str
        Decypher a message
    alterar_modo() -> None
        Change operation mode of the AES object
    """
    
    def __init__(self, mode, key=get_random_bytes(16), iv=get_random_bytes(16)):
        """Constructor for ourAES object.
        
        Parameters
        ----------
        mode : str
            String representation of AES mode to be used in consequent methods
        key : bytes (optional)
            Bytes representation of key used for this objects' methods.
        iv : bytes (optional)
            A stream of bytes indicative of initialization vector        
        """
        
        super().__init__()
        self.__key = key
        self.iv = iv
        
        # Eventually add more modes
        self.__mode_dict = {
            'CBC' : AES.MODE_CBC,
            'ECB' : AES.MODE_ECB,
            'CTR' : AES.MODE_CTR
        }
        
        if mode in self.__mode_dict.keys():
            self.__mode = self.__mode_dict[mode]
        else:
            self.__mode = AES.MODE_CBC
        
    def cifrar(self, pt, **kwargs) -> bytes:
        """Encrypt a stream of bytes using current AES configuration.
        
        Parameters
        ----------
        pt : bytes
            String representation of the AES mode to be used in consequent methods
            
        Returns
        -------
        ct : bytes
            Ciphertext byte representation
        """
        
        # TODO : try catch
        # Pad message and encrypt it. Result is given in bytes
        cifra = AES.new(self.__key, self.__mode, self.iv)
        bytes_ct = cifra.encrypt(pad(pt, AES.block_size))
        
        # Kwarg routines
        if 'show' in kwargs.keys() and kwargs['show']:
            # Ciphertext in printable format
            readable_ct = b64encode(bytes_ct).decode('utf-8')
            print('CIPHERTEXT:\n{0}\n'.format(readable_ct))
            
        if 'save' in kwargs.keys() and kwargs['save']:
            # Finding string representation of mode
            for k,v in self.__mode_dict.items():
                if self.__mode is v:
                    s_mode = k
            
            # Filename to be saved
            fname = 'ct.aes-128-{0}'.format(s_mode.lower())
            with open(fname, "wb") as f:
                f.write(bytes_ct)
                print('File was saved in\n{0}'.format(osp.relpath(fname)))
        
        return bytes_ct
    
    def decifrar(self, ct, **kwargs) -> str:
        """Decrypt a stream of bytes using current AES configuration.
        
        Parameters
        ----------
        ct : bytes
            Ciphertext or input message/file
            
        Returns
        -------
        pt : string
            Plaintext as a string
        """
        
        # TODO : try catch
        # Decipher message with the same key and iv, unpad result
        cifra = AES.new(self.__key, self.__mode, self.iv)
        pt = unpad(cifra.decrypt(ct), AES.block_size).decode('utf-8')
        
        if 'show' in kwargs.keys() and kwargs['show']:
            print('PLAINTEXT:\n{0}\n'.format(pt))
        
        if 'save' in kwargs.keys() and kwargs['save']:
            fname = 'pt.txt'
            with open(fname, "w") as f:
                f.write(pt)
                print('File was saved in\n{0}'.format(osp.relpath(fname)))
            
        return pt
    
    def alterar_modo(self, mode, **kwargs) -> None:
        """Change cipher mode for AES object
        
        Parameters
        ----------
        mode : bytes
            String of a valid AES mode of operation
        """
        
        valid_kwargs = [
            'iv',
        ]
        
        if mode in self.__mode_dict:
            self.__mode = self.__mode_dict[mode]
            
            # Different modes may have more or less arguments
            for key in valid_kwargs:
                if key in kwargs.keys():
                    setattr(self, key, kwargs[key])
            
            
            print('Cipher mode changed to {0}\n'.format(mode))
        else:
            print('Unrecognized AES mode')
        