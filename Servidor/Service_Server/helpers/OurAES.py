import os.path as osp
from base64 import b64encode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES


class OurAES:
    """Abstraction from Crypto.Cipher.AES and some of its utilities
    
    Attributes
    ----------
    __mode : str
        AES mode to be run in methods.
    
    Methods
    -------
    encrypt(bytes, bytes, bytes) -> bytes
        Encrypt a message
    decrypt(bytes, bytes, bytes) -> str
        Decrypt a message
    change_mode(str) -> None
        Change operation mode of the AES object
    """

    def __init__(self, mode):
        """Constructor for ourAES object.
        
        Parameters
        ----------
        mode : str
            String representation of AES mode to be used in consequent methods
        """

        super().__init__()

        # Eventually add more modes
        self.__mode_dict = {
            'CBC': AES.MODE_CBC,
            'ECB': AES.MODE_ECB,
            'CTR': AES.MODE_CTR
        }

        if mode in self.__mode_dict.keys():
            self.__mode = self.__mode_dict[mode]
        else:
            self.__mode = AES.MODE_CBC

    def encrypt(self, pt, key, iv, **kwargs) -> bytes:
        """Encrypt a stream of bytes using current AES configuration.
        
        Parameters
        ----------
        pt : bytes
            String representation of the AES mode to be used in consequent methods

        iv : bytes
            A stream of bytes indicative of initialization vector.

        Returns
        -------
        ct : bytes
            Ciphertext byte representation
        """

        # TODO : try catch
        # TODO : Different encryption modes may require more or less arguments
        # Pad message and encrypt it. Result is given in bytes
        cifra = AES.new(key, self.__mode, iv)
        bytes_ct = cifra.encrypt(pad(pt, AES.block_size))

        # Kwarg routines
        if 'show' in kwargs.keys() and kwargs['show']:
            # Ciphertext in printable format
            readable_ct = b64encode(bytes_ct).decode('utf-8')
            print('CIPHERTEXT:\n{0}\n'.format(readable_ct))

        if 'save' in kwargs.keys() and kwargs['save']:
            # Finding string representation of mode
            for k, v in self.__mode_dict.items():
                if self.__mode is v:
                    s_mode = k

            # Filename to be saved
            fname = 'ct.aes-128-{0}'.format(s_mode.lower())
            with open(fname, "wb") as f:
                f.write(bytes_ct)
                print('File was saved in\n{0}'.format(osp.relpath(fname)))

        return bytes_ct

    def decrypt(self, ct, key, iv, **kwargs) -> str:
        """Decrypt a stream of bytes using current AES configuration.
        
        Parameters
        ----------
        ct : bytes
            Ciphertext or input message/file.
        key : bytes
            Bytes representation of key used in this decryption instance.
        iv : bytes
            A stream of bytes indicative of initialization vector

        Returns
        -------
        pt : string
            Plaintext as a string
        """

        # TODO : try catch
        # TODO : Different encryption modes may require more or less arguments
        # Decipher message with the same key and iv, unpad result
        cifra = AES.new(key, self.__mode, iv)
        pt = unpad(cifra.decrypt(ct), AES.block_size).decode('utf-8')

        if 'show' in kwargs.keys() and kwargs['show']:
            print('PLAINTEXT:\n{0}\n'.format(pt))

        if 'save' in kwargs.keys() and kwargs['save']:
            fname = 'pt.txt'
            with open(fname, "w") as f:
                f.write(pt)
                print('File was saved in\n{0}'.format(osp.relpath(fname)))

        return pt
