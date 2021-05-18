from Crypto.Hash import SHA512
from cliente.helpers import OurAES


def hash(s):
    h = SHA512.new()
    h.update(bytes(s.encode()))
    return h.hexdigest()

def xor_str(a,b):
    return ''.join([hex(ord(a[i%len(a)]) ^ ord(b[i%(len(b))]))[2:] for i in range(max(len(a), len(b)))])

def hash_of_fuck_off(username, curr_time, salt, password):
    """
    Create user's cypher key

    Parameters
    ----------
    username : string
    curr_time : string
    salt : string
    password : string


    Returns
    -------
    byte string containing user's cypher key
    """
    
    pt1 = hash(curr_time)
    pt1 += salt + password

    for i in range(0,len(username)):
        pt1 = hash(pt1)
    
    return pt1

def test():
    h = hash_of_fuck_off('pedro', '12-05-2021', 'adfadfadfagadfgadgfsdg', 'in4cio')
    aes = OurAES('CTR')
    aes.encrypt('es toda boa', h, 'asdsadasda')

test()