from Crypto.Hash import SHA512
from helpers import OurAES
from auth_db_helper import DBHelper_auth
from base64 import b64decode


def hash(s):
    h = SHA512.new()
    h.update(bytes(s.encode()))
    return h.hexdigest()


def xor_str(a, b):
    return ''.join([hex(ord(a[i % len(a)]) ^ ord(b[i % (len(b))]))[2:] for i in range(max(len(a), len(b)))])


def hash_of_2fa(username, curr_time, salt):
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
    pt1 += salt

    for i in range(0, len(username)):
        pt1 = hash(pt1)

    return pt1


def encrypt_2fa(token, username):
    h , h2 = get_2fa_necessities(username)
    # cyphers the token using AES
    aes = OurAES.OurAES('CBC')
    cypher = aes.encrypt(token.encode(), h[-32:], h2[0:16])
    return cypher


def decrypt_2fa(cypher, username):
    aes = OurAES.OurAES('CBC')
    h, h2 = get_2fa_necessities(username)
    decypher = aes.decrypt(b64decode(cypher), h[-32:], h2[0:16])
    return decypher
    
def get_2fa_necessities(username):
    dbHelper = DBHelper_auth()
    # creates two hashes one for key other for iv
    created_at, salt, fa2_token = dbHelper.get_user_info_for_2fa(username)
    h = hash_of_2fa(username, created_at.strftime("%m/%d/%Y"), salt)
    h2 = hash_of_2fa(salt, created_at.strftime("%m/%d/%Y"), username)
    return h,h2
