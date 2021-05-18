"""
Set up of Flask's Blueprint for the user's authentication
"""

from flask import (
    Blueprint,
    request,
    Response,
    jsonify,
    make_response
)

from helpers.fa_encryption import encrypt_2fa, decrypt_2fa

from utils import (
    validate_user_input,
    generate_salt,
    generate_hash,
    generate_jwt_token,
    get_jwt_data,
    is_jwt_equals,
    is_jwt_valid
)

import time
import db_helper as helper
import pyotp


auth_blueprint = Blueprint('auth', __name__,)


@auth_blueprint.route("/register", methods=["POST"])
def register_user():
    """
    Method to regist a new user

    :param: None
    :return: 201 and the 2fa token if it has success
             409 if the username is already in use
             400 if it is not possible to process due to client error
    """

    dbHelper = helper.DBHelper()

    # get parameters
    username = get_from_json("username")
    user_email = get_from_json("email")
    user_password = get_from_json("password")

    if validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)

        # actually write to DB
        if dbHelper.insert_user(username, user_email, password_salt, password_hash):

            # expiration time - 15 minutes
            exp = int(time.time())+900

            # data to incorporate the message
            dataToEncode = {'user': username, 'exp': exp}

            # get the query result, i.e verify the user existence
            is_2fa_enabled = dbHelper.user_has_2fa(username)

            # get the query result, i.e verify the user existence
            jwt_token = generate_jwt_token(dataToEncode)
            dbHelper.store_jwt(jwt_token, username)

            # wrap into message to send it
            message = {"status": "OK", "token_2fa": is_2fa_enabled,
                       "jwt_token": jwt_token, "username": username}

            # 201: Success - Created
            dbHelper.close()
            return jsonify(message)
        else:
            dbHelper.close()
            # 409: Fail - Conflit between the current state of the target
            return Response(status=409)
    else:
        dbHelper.close()
        # 400: Fail - Server can't process due to client error
        return Response(status=400)


@auth_blueprint.route("/login", methods=["POST"])
def login_user():
    """
    Method to login an user

    :param: None
    :return: jwt, status, 2fa token and username if the credentials are valid
             401 if the credentials are invalid             
    """

    dbHelper = helper.DBHelper()

    # get parameters
    user_name = get_from_json("username")
    user_password = get_from_json("password")

    # check if the user has records in the database
    if dbHelper.verify_user(user_name, user_password):

        # expiration time - 15 minutes
        exp = int(time.time())+900

        # data to incorporate the message
        dataToEncode = {'user': user_name, 'exp': exp}

        # check if the user has 2fa entry in the database and send the result
        token_2fa = dbHelper.user_has_2fa(user_name)
        print(token_2fa)
        print(dataToEncode)

        jwt_token = generate_jwt_token(dataToEncode)
        dbHelper.store_jwt(jwt_token, user_name)

        dbHelper.close()

        # returns the session token with the status and the 2fa token
        return jsonify({"jwt_token": jwt_token,
                        "status": "OK",
                        "token_2fa": token_2fa,
                        "username": user_name})

    else:
        message = {"status": "NOK",
                   "message": "Invalid credentials"}

        dbHelper.close()

        # 401 - UNAUTORIZED - credentials not valid
        return make_response(jsonify(message), 401)


@auth_blueprint.route("/login2fa", methods=["POST"])
def login_user2fa():
    """
    Method to verify 2fa after login

    :param: 2fa_token,code
    :return: jwt, status, 2fa token and username if the credentials are valid
             401 if the credentials are invalid
    """

    # get parameters
    jwt_token = get_from_json("jwt_token")
    secret_token = get_from_json("secret")
    fa_code = get_from_json("otp")

    # verifica se o jwt é valido
    jwt_data, jwt_valid = is_jwt_valid(jwt_token)

    # caso não seja retorna uma mensagem de erro
    if not jwt_valid:
        return jwt_data
    del jwt_valid

    db_auth = helper.DBHelper()
    fa_token = db_auth.user_has_2fa(jwt_data['user'])

    if not bool(fa_token) or fa_token == 'NOK':
        totp = pyotp.TOTP(secret_token)

        if not totp.verify(fa_code):
            return jsonify({"status": "NOK", "message": "Wrong 2FA code"})

        crypt = encrypt_2fa(secret_token, jwt_data['user'])

        result = db_auth.insert_user_info_for_2fa(crypt, jwt_data['user'])

        db_auth.commit()
        db_auth.close()

        if result:
            return jsonify({"status": "OK"})
        else:
            return jsonify({"status": "NOK", "message": "You are contacting support"})

    else:
        secret_token = decrypt_2fa(fa_token, jwt_data['user'])
        totp = pyotp.TOTP(secret_token)

        if not totp.verify(fa_code):
            return jsonify({"status": "NOK", "message": "Wrong 2FA code"})
        else:
            return jsonify({"status": "OK"})


def get_from_json(JSONKey):
    """
    Get the parameter from json 
    """
    return request.get_json()[JSONKey]
