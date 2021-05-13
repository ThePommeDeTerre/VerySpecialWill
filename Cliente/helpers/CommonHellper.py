from flask import escape
import json


# Fazer o trim dos fields e verificar se estao vazias
def trim_params(params):
    valid = True
    for p in params.keys():
        # faz strip ao parametro e faz sanitize (impedir xss)
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
