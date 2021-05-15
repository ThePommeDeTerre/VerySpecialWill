"""

Validation of user inputs

"""

from hashlib import pbkdf2_hmac
from settings import JWT_SECRET_KEY

import os
import jwt


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and ( len(kwargs["password"]) <= 255 ):
            return True
        else:
            return False

def generate_salt():
    salt = os.urandom(16) # 16 byte -> 128 bit
    return salt.hex()

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac (
        "sha512",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()

def generate_jwt_token(message):
    """
    Generate a JWT to respond to the user
    """
    # enconde data
    encoded_content = jwt.encode(message, JWT_SECRET_KEY, algorithm="HS512")
    token = str(encoded_content).split("'")[1]
    return token