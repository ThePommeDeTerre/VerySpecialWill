"""

Service Server Blueprint

"""

from flask import (
    Blueprint,
    make_response,
    request
)

from flask.json import jsonify
from flask.wrappers import Response
from helpers.fa_encryption import encrypt_2fa, decrypt_2fa

import service_db_helper as helper_service

service_blueprint = Blueprint('service', __name__,)

# must be here to avoid circular imports
from utils_service import (
    get_jwt_data,
    is_jwt_equals,
    is_jwt_valid
)

@service_blueprint.route("/login2fa", methods=["POST"])
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

    #verifica se o jwt é valido
    jwt_data, jwt_valid = is_jwt_valid(jwt_token) 

    #caso não seja retorna uma mensagem de erro
    if not jwt_valid:
        return jwt_data
    del jwt_valid
    encrypt_2fa(secret_token,jwt_data['user'])

    return jsonify(jwt_data)

@service_blueprint.route("/create", methods=["POST"])
def create_will():

    """
    Method to create a will
    """

    # get jwt token
    jwt_token = get_from_json("jwt_token")

    # JWT can't be empty, if it is stop right now
    if not bool(jwt_token.split()):
        message = {"status": "NOK",
                   "message": "Invalid Token"}

        # 401 - UNAUTHORIZED - session token doesn't authorize the user anymore
        return jsonify(message)
    
    # verify token
    jwt_data = get_jwt_data(jwt_token)

    # connect to service db
    dbHelper = helper_service.DBHelper_service()
    
    #verifica se o jwt é valido
    jwt_data, jwt_valid = is_jwt_valid(jwt_token) 

    #caso não seja retorna uma mensagem de erro
    if not jwt_valid:
        return jwt_data
    del jwt_valid

    # update table user in service db with usernames from auth db
    if not dbHelper.populate_service_with_auth():
        message = {"status": "NOK",
                   "message": "Error in database"}

        # not created
        return jsonify(message)

    # in the end, close
    dbHelper.close()
    return jsonify({"message": "End"})

    # TODO : continue this - get the message, the people to give keys ...


def get_from_json(JSONKey):

    """
    Get the parameter from json 
    """
    return request.get_json()[JSONKey]