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

from utils_service import (
    get_jwt_data
)

import service_db_helper as helper_service

service_blueprint = Blueprint('service', __name__,)

@service_blueprint.route("/create", methods=["POST"])
def create_will():

    """
    Method to create a will
    """

    # get parameters
    jwt_token = get_from_json("jwt_token")
    
    # verify token
    jwt_data = get_jwt_data(jwt_token)
    
    if not jwt_data:
        message = {"status": "NOK",
                   "message": "Invalid Token"}
        # 401 - UNAUTHORIZED - session token doesn't authorize the user anymore
        return jsonify(message)


    # populate database
    dbHelper = helper_service.DBHelper_service()

    if dbHelper.populate_service_with_auth():
        message = {"status": "OK"}

        # created
        dbHelper.close()
        return jsonify(message)
    else:
        print("Erro")

    # TODO : continue this - get the message, the people to give keys ...


def get_from_json(JSONKey):

    """
    Get the parameter from json 
    """
    return request.get_json()[JSONKey]