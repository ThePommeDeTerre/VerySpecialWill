"""

Auxiliar file with calculations

"""

from json import load

import jwt
import os
import auth_db_helper as helper_auth

def get_jwt_data(token):

    """
    Get the data in the jwt
    :param token: JWT
    :return: dictionary with the respective data or not
    """

    # empty dict
    data = {}

    # decode
    try:
        load.dotenv()
        data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithm="HS512")

        return data

    # signature has expired
    except jwt.ExpiredSignatureError as error:
        print(error)
        return data

# TODO: get usernames from the authentication database, acho
