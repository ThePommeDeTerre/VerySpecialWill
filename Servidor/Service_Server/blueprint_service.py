"""

Service Server Blueprint

"""
import traceback
from utils_service import (
    get_jwt_data,
    is_jwt_equals,
    is_jwt_valid
)
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
from helpers.DecideMethod import randomness_galore

service_blueprint = Blueprint('service', __name__,)


@service_blueprint.route("/create", methods=["POST"])
def create_will():
    try:
        """
        Method to create a will
        """

        # get jwt token
        jwt_token = get_from_json("jwt_token")

        # verifica se o jwt é valido
        jwt_data, jwt_valid = is_jwt_valid(jwt_token)

        # caso não seja retorna uma mensagem de erro
        if not jwt_valid:
            return jwt_data

        del jwt_valid

        # verificar se os emails existem
        db_auth = helper_auth.DBHelper_auth()
        username_list = db_auth.verify_emails(get_from_json("emailList"))

        if not username_list:
            message = {"status": "NOK",
                       "message": "One or more emails don\'t exist"}
            return jsonify(message)

        db_service = helper_service.DBHelper_service()

        # # update table user in service db with usernames from auth db
        if not db_service.populate_service_with_auth():
            message = {"status": "NOK",
                       "message": "Error in database"}

        params = request.get_json()
        cripto_f = params['cypher']
        will_txt = params['special_will']
        hash_f = params['hash']
        date = params['date']
        min_shares = params['min_shares']
        n_shares = params['n_shares']
        print(date)

        (cypher, hmac, key, pub, sign, nonce,date_hash) = randomness_galore(will_txt, cripto_f, hash_f, date)
        # Insere o testamento
        will_id = db_service.insert_will(jwt_data['user'], cypher, hmac, sign, pub, min_shares,cripto_f,hash_f)

        # Insere os segredos do testamento
        db_service.insert_users_of_will(will_id, key, username_list, min_shares, n_shares, date_hash)

        db_service.commit()
        db_auth.commit()

        db_auth.close()
        db_service.close()
        return jsonify({"status": "OK"})
    except Exception as e:
        print(traceback.format_exc())
        if db_auth:
            db_auth.rollback()
        if db_service:
            db_service.rollback()
        return jsonify({"status": "NOK", "message": "An error has occurred"})


@service_blueprint.route("/inheritpage", methods=["POST"])
def inherit_will_fill_page():
    """
    Method to try and inherit a will
    """

    # get jwt token
    jwt_token = get_from_json("jwt_token")

    # verifica se o jwt é valido
    jwt_data, jwt_valid = is_jwt_valid(jwt_token)

    # caso não seja retorna uma mensagem de erro
    if not jwt_valid:
        return jwt_data
    del jwt_valid

    username = jwt_data['user']
    db_service = helper_service.DBHelper_service()

    # Buscar as wills que estão associadas ao perfil do utilizador
    # Eventually add timeout
    will_params = db_service.populate_page_with_wills(username)

    return jsonify({'status': 'OK', 'rows': will_params})


@service_blueprint.route("/hasaccesstowill", methods=["POST"])
def has_access_to_will():
    """
    Method to try and inherit a will
    """
    # get jwt token
    will_id = get_from_json("will_id")
    jwt_token = get_from_json("jwt_token")

    # verifica se o jwt é valido
    jwt_data, jwt_valid = is_jwt_valid(jwt_token)

    # caso não seja retorna uma mensagem de erro
    if not jwt_valid:
        return jwt_data
    del jwt_valid

    username = jwt_data['user']

    db_service = helper_service.DBHelper_service()

    dead_man_will_info , has_access  = db_service.has_access_to_will(username,will_id)

    return jsonify({'status': 'OK', 'access': has_access , 'dea_man_will_info': dead_man_will_info})
    

@service_blueprint.route("/decypherwill", methods=["POST"])
def decypher_will():
    db_service = helper_service.DBHelper_service()

    # get jwt token
    jwt_token = get_from_json("jwt_token")
    will_id = get_from_json("will_id")
    try:
        """
        Method to try and inherit a will
        """

        # verifica se o jwt é valido
        jwt_data, jwt_valid = is_jwt_valid(jwt_token)

        # caso não seja retorna uma mensagem de erro
        if not jwt_valid:
            return jwt_data
        del jwt_valid

        username = jwt_data['user']

        #faz update ao teu key_share
        if not db_service.update_your_share(username,will_id):
            db_service.commit()
            raise Exception('An error has occurred in the share update')

        #verifica se já estao todas as chaves reunidas
        will_ready = db_service.is_will_ready(username,will_id)

        if not will_ready:
            db_service.commit()
            raise Exception('Not all shares are ready, try later')

    except Exception as e:
        print(traceback.format_exc())

        #dados para refazer o ecrã
        dead_man_will_info , has_access  = db_service.has_access_to_will(username,will_id)

        if db_service:
            db_service.close()
        return jsonify({'status': 'OK_ACCESS', 'access': has_access , 'dea_man_will_info': dead_man_will_info, 'message':str(e)})
    


def get_from_json(JSONKey):
    """
    Get the parameter from json
    """
    return request.get_json()[JSONKey]
