"""

Auxiliar file with calculations

"""

from hashlib import pbkdf2_hmac
from settings import JWT_SECRET_KEY

import os
import jwt


def validate_user_input(input_type, **kwargs):

    """
    Checks if the user input (email and password) is legit
    :param input_type: must be authentication
    :param **kargs: user_email and user_password
    :return: True or False
    """
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and ( len(kwargs["password"]) <= 255 ):
            return True
        else:
            return False


def generate_salt():

    """
    Generate a random value to be the salt
    :return: a random number with 128 bits
    """
    salt = os.urandom(16) # 16 byte -> 128 bit
    return salt.hex()


def generate_hash(plain_password, password_salt):

    """
    Given a plain_password and a salt, returns the password hash
    :param plain_password: password in plain text
    :param password_salt: the salt
    :return: password hash
    """
    
    password_hash = pbkdf2_hmac (
        "sha512",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()


def generate_jwt_token(message):

    """
    Generate a JWT to send to the user with Hash512 and the secret key
    :param message: the message to encode
    :return: JWT 
    """

    # enconde data
    encoded_content = jwt.encode(message, JWT_SECRET_KEY, algorithm="HS512")
    token = str(encoded_content).split("'")[1]
    return token