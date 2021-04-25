from flask import Flask, render_template, session, request
import secrets
import helpers.SessionHelper as SessionHelper
import helpers.CommonHellper as Common
import static.ServerRoutes as SerRoutes
import json

# Este nao usem o pip para instalar, mas o gestor de packages do pycharm
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
        params = request.get_json();

        # Fazer o trim dos fields e verificar se estao vazias
        params, valid = Common.trim_params(params)

        url = SerRoutes.ROUTES['login']
        response = requests.post(url, json=params)

        if valid:
            return Common.create_response_message(200, True)
        else:
            return Common.create_response_message(200, False, 'Por favor preencha todos os campos')

    else:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


# Efetua o registo
@app.route('/registo', methods=['POST'])
def registo():
    if request.method == 'POST':
        params = request.get_json();

        # Fazer o trim dos fields e verificar se estao vazios
        params, valid = Common.trim_params(params)

        url = SerRoutes.ROUTES['registo']
        # response = requests.post(url, data=params)
        if valid:
            return Common.create_response_message(200, True)
        else:
            return Common.create_response_message(200, False, 'Por favor preencha todos os campos')

    else:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


# Como é por ajax, mudo o primeiro parametro para json, e retorno uma mensagem de erro
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return Common.create_response_message(400, True, 'Csrf Inválido', {'CsrfError': True})


if __name__ == '__main__':
    app.run()

# response = requests.get("http://149.90.108.93:80")
