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
import auth_db_helper as helper_auth
import service_db_helper as helper_service
import pyotp
import helpers.DecideMethod

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

    db_auth = helper_auth.DBHelper_auth()
    fa_token = db_auth.user_has_2fa(jwt_data['user'])
    
    if not bool(fa_token):
        totp = pyotp.TOTP(secret_token)

        if not totp.verify(fa_code):
            return jsonify({"status": "NOK", "message": "Wrong 2FA code"})

        crypt = encrypt_2fa(secret_token,jwt_data['user'])

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
            
@service_blueprint.route("/create", methods=["POST"])
def create_will():

    """
    Method to create a will
    """

    # get jwt token
    jwt_token = get_from_json("jwt_token")

    #verifica se o jwt é valido
    jwt_data, jwt_valid = is_jwt_valid(jwt_token)

    #caso não seja retorna uma mensagem de erro
    if not jwt_valid:
        message = {"status": "NOK","message": "Invalid Token"}
        # 401 - UNAUTHORIZED - session token doesn't authorize the user anymore
        return jsonify(message)

    del jwt_valid

    #verificar se os emails existem
    db_auth = helper_auth.DBHelper_auth()
    username_list = db_auth.verify_emails(get_from_json("emailList"))

    if not username_list:
        message = {"status": "NOK","message": "One or more emails don\'t exist"}
        return jsonify(message)


    # # update table user in service db with usernames from auth db
    # if not dbHelper.populate_service_with_auth():
    #     message = {"status": "NOK",
    #                "message": "Error in database"}

    #     # not created
    #     return jsonify(message)

    # in the end, close
    # TODO : continue this - get the message, the people to give keys ...
    
    params = request.get_json()
    cripto = params['cypher']
    will = params['special_will']
    hash = params['hash']

    (cypher, hmac) = randomness_galore(will, cripto, hash)


    insert_will(jwt_token['username'], cypher)

    db_auth.close()
    return jsonify({"message": "End"})



def get_from_json(JSONKey):

    """
    Get the parameter from json
    """
    return request.get_json()[JSONKey]