import json


# Fazer o trim dos fields e verificar se estao vazias
def trim_params(params):
    valid = True
    for p in params.keys():
        params[p] = params[p].rstrip()
        if not params[p]:
            valid = False
    return params, valid


# cria a resposta standard para o frontend
def create_response_message(response_code, success=True, message='', extra_params={}):
    final_params = z = {'success': success, 'msg': message, **extra_params}
    return json.dumps(final_params), response_code, {'ContentType': 'application/json'}
