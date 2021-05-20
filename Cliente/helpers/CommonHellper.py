from flask import escape
import json


# Fazer o trim dos fields e verificar se estao vazias
def trim_params(params):
    valid = True
    for p in params.keys():
        # faz strip ao parametro e faz sanitize (impedir xss)
        if isinstance(params[p], list):
            for i, item in enumerate(params[p]):
                params[p][i] = escape(item.rstrip())
        else:
            params[p] = escape(params[p].rstrip())

        if not params[p]:
            valid = False

    return params, valid


# Faz o sanitize dos elementos da tabela
def sanitize_rows(params):
    for p, param in enumerate(params):
        if isinstance(param, str):
            params[p] = escape(param.rstrip())
    return params


# cria a resposta standard para o frontend
def create_response_message(response_code, success=True, message='', extra_params={}):
    final_params = z = {'success': success, 'msg': message, **extra_params}
    return json.dumps(final_params), response_code, {'ContentType': 'application/json'}


def test_create_will(params):
    if int(params['n_shares']) <= 0 or int(params['min_shares']) <= 0:
        return create_response_message(200, False, 'Shares values can\'t be 0'), False
    elif int(params['n_shares']) < int(params['min_shares']):
        return create_response_message(200, False, 'Number of shares must be superior or equal to number of minimum shares'), False
    elif len(params['emailList']) < int(params['n_shares']):
        return create_response_message(200, False, 'Number of emails must be the same as number of shares'), False
    else :
        return None, True
