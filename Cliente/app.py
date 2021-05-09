from flask import Flask, render_template, request, send_file, redirect, url_for
import secrets
import helpers.SessionHelper as SessionHelper
import helpers.CommonHellper as Common
import static.ServerRoutes as SerRoutes
import pyotp

# Este nao usem o pip para instalar, mas o gestor de packages do pycharm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_mail import Mail
from flask_qrcode import QRcode

from Servidor import email_test
import requests

app = Flask(__name__)
qrcode = QRcode(app)

# Cria a secret key para a sessão e ativa proteção por csrf
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


csrf = CSRFProtect(app)


# region index
@app.route('/')
def main():
    SessionHelper.start_session(app)
    # flash("Welcome to death", "success")
    return render_template('login.html')


# Efetua o login, caso seja inválido ou nao seja post, retorna mensagem de erro
@app.route('/login', methods=['POST'])
def login():
    try:
        if request.method == 'POST':
            params = request.get_json();

            # Fazer o trim dos fields e verificar se estao vazias
            params, valid = Common.trim_params(params)

            if not valid:
                return Common.create_response_message(200, False, 'Por favor preencha todos os campos')

            url = SerRoutes.ROUTES['login']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                return Common.create_response_message(200, True)
            elif response_params['status'] == 'NOK':
                return Common.create_response_message(200, False, response_params.message)
            else:
                return Common.create_response_message(200, False, 'Ocorreu um erro, por favor contrate o suporte')

        else:
            return Common.create_response_message(200, False, 'Ocorreu um erro')

    # Caso haja erros de status ou conexão
    except:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


# Efetua o registo
@app.route('/registo', methods=['POST'])
def registo():
    try:
        if request.method == 'POST':
            params = request.get_json();

            # Fazer o trim dos fields e verificar se estao vazios
            params, valid = Common.trim_params(params)

            if not valid:
                return Common.create_response_message(200, False, 'Por favor preencha todos os campos')

            url = SerRoutes.ROUTES['registo']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                return Common.create_response_message(200, True)
            elif response_params['status'] == 'NOK':
                return Common.create_response_message(200, False, response_params.message)
            else:
                return Common.create_response_message(200, False, 'Ocorreu um erro, por favor contrate o suporte')

        else:
            return Common.create_response_message(200, False, 'Ocorreu um erro')
    # Caso haja erros de status ou conexão
    except:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


# endregion

# region 2fa
@app.route('/login/2fa', methods=['GET'])
def login_2fa():
    try:
        if request.method == 'POST':
            params = request.get_json();
        else:

            # ir buscar secret key do user, por enquanto usar random
            secret = pyotp.random_base32()
            uri = pyotp.totp.TOTP(secret).provisioning_uri(name='test@google.com', issuer_name='A Very Special Will')
            secreturi = uri
            return render_template('login_2fa.html', secret=secret, secreturi=secreturi)
    # Caso haja erros de status ou conexão
    except Exception  as e:
        print(e)
        return Common.create_response_message(200, False, 'Ocorreu um erro')


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")

# endregion


# region beforeRequest
@app.before_request
def before_request():
    request_guest_handpoints = ['login', 'registo', 'qrcode', 'main', 'sendemail', 'static']
    # implementar função de teste de sessão

    if True and (request.endpoint not in request_guest_handpoints):
        return redirect(url_for('main'))
    return


# endregion

# region errorHandling
# Como é por ajax, mudo o primeiro parametro para json, e retorno uma mensagem de erro
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return Common.create_response_message(400, True, 'Csrf Inválido', {'CsrfError': True})


# endregion

if __name__ == '__main__':
    app.run()

# response = requests.get("http://149.90.108.93:80")
