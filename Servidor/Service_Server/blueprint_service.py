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

import service_db_helper as helper_service

service_blueprint = Blueprint('service', __name__,)

# must be here to avoid circular imports
from utils_service import (
    get_jwt_data,
    is_jwt_equals
)

@service_blueprint.route("/create", methods=["POST"])
def create_will():

    """
    Method to create a will
    """

    # get jwt token
    jwt_token = get_from_json("jwt_token")
    
    # verify token
    jwt_data = get_jwt_data(jwt_token)

    # connect to service db
    dbHelper = helper_service.DBHelper_service()
    
    # if the signature is invalid or the jwt isn't the most recent one
    if ((not jwt_data) or (not is_jwt_equals(jwt_token))):
        message = {"status": "NOK",
                   "message": "Invalid Token"}

        # 401 - UNAUTHORIZED - session token doesn't authorize the user anymore
        return jsonify(message)


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