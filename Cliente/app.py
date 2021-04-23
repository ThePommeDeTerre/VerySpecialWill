from flask import Flask, render_template, session, request
import secrets
import helpers.SessionHelper as SessionHelper
import json

# este nao usem o pip para instalar, mas o gestor de packages do pycharm
from flask_wtf.csrf import CSRFProtect, CSRFError
import requests

app = Flask(__name__)

# Cria a secret key para a sessão e ativa proteção por csrf
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
csrf = CSRFProtect(app)


@app.route('/')
def main():
    SessionHelper.start_session(app)
    return render_template('login.html')


# Efetua o login, caso seja inválido ou nao seja post, retorna mensagem de erro
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        valid = True
        params = request.get_json();

        # Fazer o trim dos fields e verificar se estao vazias
        for p in params.keys():
            params[p] = params[p].rstrip()
            if not params[p]:
                valid = False

        url = "http://149.90.108.93:80"
        # response = requests.post(url, data=params)
        if valid:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False, 'msg': 'Por favor preencha todos os campos'}), 200, {
                'ContentType': 'application/json'}

    else:
        return json.dumps({'success': False, 'msg': 'Ocorreu um erro'}), 200, {'ContentType': 'application/json'}


# Efetua o registo
@app.route('/registo', methods=['POST'])
def registo():
    if request.method == 'POST':
        valid = True
        params = request.get_json();

        # Fazer o trim dos fields e verificar se estao vazias
        for p in params.keys():
            params[p] = params[p].rstrip()
            if not params[p]:
                valid = False

        url = "http://149.90.108.93:80"
        # response = requests.post(url, data=params)
        if valid:
            return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
        else:
            return json.dumps({'success': False, 'msg': 'Por favor preencha todos os campos'}), 200, {
                'ContentType': 'application/json'}

    else:
        return json.dumps({'success': False, 'msg': 'Ocorreu um erro'}), 200, {'ContentType': 'application/json'}


# Como é por ajax, mudo o primeiro parametro para json, e retorno uma mensagem de erro
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return json.dumps({'CsrfError': True, 'msg': 'Csrf Inválido'}), 400, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run()

# response = requests.get("http://149.90.108.93:80")
