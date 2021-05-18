"""

Auxiliar file with calculations

"""

from dotenv import load_dotenv

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
        load_dotenv()
        data = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithm="HS512")

        return data

    # signature has expired
    except jwt.ExpiredSignatureError as error:
        print(error)
        return data


def is_jwt_equals(jwt):

    """
    Given one jwt verifies if it is equals to the last one created
    """

    data = get_jwt_data(jwt)
    username = data["user"]

    dbHelper = helper_auth.DBHelper_auth()

    jwt_db = dbHelper.get_jwt_from_user(username)

    dbHelper.close()

    # if they are equals and not the empty string
    return jwt == jwt_db and bool(jwt)