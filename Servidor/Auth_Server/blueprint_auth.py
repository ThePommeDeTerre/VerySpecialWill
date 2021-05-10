"""
Set up of Flask's Blueprint for the user's authentication
"""

import time

from flask import (Blueprint,
                  request, 
                  Response, 
                  jsonify,
                  make_response
)

from utils import (
    validate_user_input,
    generate_salt,
    generate_hash,
    generate_jwt_token
)
import db_helper as helper
dbHelper = helper.DBHelper()


auth_blueprint = Blueprint('auth', __name__,)
@auth_blueprint.route('/', methods=["GET"])
def this_main():
    return 'baaahh'


"""
Handle the user registration
"""
@auth_blueprint.route("/register", methods=["POST"])
def register_user():

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

            # get the query result, i.e verify the user existence
            is_2fa_enabled = dbHelper.user_has_2fa(username)

            # wrap into message to send it
            message = {"token_2fa": is_2fa_enabled}

            # 201: Success - Created 
            return make_response(jsonify(message), 201)
        else:

            # 409: Fail - Conflit between the current state of the target 
            return Response(status=409)
    else:

        # 400: Fail - Server can't process due to client error 
        return Response(status=400)

"""
Handle the user login
"""
@auth_blueprint.route("/login", methods=["POST"])
def login_user():

    # get parameters
    user_name = get_from_json("username")
    user_password = get_from_json("password")

    # check if the user has records in the database
    if dbHelper.verify_user(user_name, user_password):

        # expiration time - 15 minutes
        exp =  int(time.time())+900

        # data to incorporate the message
        dataToEncode = {'user': user_name, 'exp': exp}

        # check if the user has 2fa entry in the database and send the result
        token_2fa = dbHelper.user_has_2fa(user_name)

        # returns the session token with the status and the 2fa token
        return jsonify({"jwt_token": generate_jwt_token(dataToEncode), 
                        "status": "OK", 
                        "token_2fa": token_2fa})
    
    else:
        message = {"status": "NOK", 
                   "message":"Invalid credentials"}

        # 401 - UNAUTORIZED - credentials not valid
        return make_response(jsonify(message), 401)

# internal function
def get_from_json(JSONKey):
    return request.get_json()[JSONKey]