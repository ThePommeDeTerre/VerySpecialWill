from Crypto.Hash import SHA512
from helpers import OurAES
from auth_db_helper import DBHelper_auth


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
    dbHelper = DBHelper_auth()
    # creates two hashes one for key other for iv
    created_at, salt = dbHelper.get_user_info_for_2fa(username)
    h = hash_of_2fa(username, created_at.strftime("%m/%d/%Y"), salt)
    h2 = hash_of_2fa(salt, created_at.strftime("%m/%d/%Y"), username)

    # cyphers the token using AES
    aes = OurAES.OurAES('CBC')
    print(token, h, h2)
    aes.encrypt(token, h[-32:], h2[0:16])


def decrypt_2fa():
    h = hash_of_2fa('pedro', '12-05-2021', 'adfadfadfagadfgadgfsdg', 'in4cio')
    aes = OurAES('CTR')
    aes.encrypt('es toda boa', h, 'asdsadasda')
