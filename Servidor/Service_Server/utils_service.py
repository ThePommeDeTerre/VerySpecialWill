"""

Auxiliar file with calculations

"""

from dotenv import load_dotenv

import jwt
import os

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
        load_dotenv()
        data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithm="HS512")

        return data

    # signature has expired
    except jwt.ExpiredSignatureError as error:
        print(error)
        return data