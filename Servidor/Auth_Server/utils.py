"""

Auxiliar file with calculations

"""

from hashlib import pbkdf2_hmac
from settings import JWT_SECRET_KEY

from flask.json import jsonify
import db_helper as helper
import os
import jwt
from dotenv import load_dotenv


def validate_user_input(input_type, **kwargs):
    """
    Checks if the user input (email and password) is legit
    :param input_type: must be authentication
    :param **kargs: user_email and user_password
    :return: True or False
    """
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and (len(kwargs["password"]) <= 255):
            return True
        else:
            return False


def generate_salt():
    """
    Generate a random value to be the salt
    :return: a random number with 128 bits
    """
    salt = os.urandom(16)  # 16 byte -> 128 bit
    return salt.hex()


def generate_hash(plain_password, password_salt):
    """
    Given a plain_password and a salt, returns the password hash
    :param plain_password: password in plain text
    :param password_salt: the salt
    :return: password hash
    """

    password_hash = pbkdf2_hmac(
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


def get_jwt_data(token):
    """
    Get the data in the jwt
    :param token: JWT
    :return: dictionary with the respective data or not
    """

    # empty dict
    data = {}

    if not token:
        return data

    # decode
    try:
        load_dotenv()
        data = jwt.decode(token, os.getenv(
            "JWT_SECRET_KEY"), algorithm="HS512")

        return data

    # signature has expired
    except jwt.ExpiredSignatureError as error:
        print(error)
        return data


def is_jwt_valid(jwt_token):
    """
    if the signature is invalid or the jwt isn't the most recent one
    :param token: JWT
    :return: message/data , valid
    """

    if not bool(jwt_token.split()):
        message = {"status": "NOK",
                   "message": "Invalid Token"}

        # 401 - UNAUTHORIZED - session token doesn't authorize the user anymore
        return jsonify(message), False

    # verify token
    jwt_data = get_jwt_data(jwt_token)

    # if the signature is invalid or the jwt isn't the most recent one
    if ((not jwt_data) or (not is_jwt_equals(jwt_token))):
        message = {"status": "NOK",
                   "message": "Invalid Token"}

        # 401 - UNAUTHORIZED - session token doesn't authorize the user anymore
        return jsonify(message), False
    else:
        return jwt_data, True


def is_jwt_equals(jwt):
    """
    Given one jwt verifies if it is equals to the last one created
    """

    data = get_jwt_data(jwt)
    username = data["user"]

    dbHelper = helper.DBHelper()

    jwt_db = dbHelper.get_jwt_from_user(username)

    dbHelper.close()

    # if they are equals and not the empty string
    return jwt == jwt_db and bool(jwt)

# endregion jwt
