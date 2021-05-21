from flask import Flask, render_template, session, request, flash, send_file, redirect, url_for, g, escape
import secrets
import helpers.SessionHelper as SessionHelper
import helpers.CommonHellper as Common
import static.ServerRoutes as SerRoutes
import pyotp
import os

# Este nao usem o pip para instalar, mas o gestor de packages do pycharm
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_qrcode import QRcode
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
            params = request.form.to_dict()

            # Fazer o trim dos fields e verificar se estao vazias
            params, valid = Common.trim_params(params)

            if not valid:
                flash('Please fill all fields', "danger")
                return redirect('/')

            url = SerRoutes.ROUTES['login']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200 and response.status_code != 401:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                session['user'] = \
                    {
                        '2fa_logged': False,
                        '2fa_token': response_params['token_2fa'],
                        'username': response_params['username'],
                        'jwt_token': response_params['jwt_token'],
                    }
                return redirect(url_for('login_2fa'))
            elif response_params['status'] == 'NOK':
                flash(response_params['message'], "danger")
                return redirect('/')
            else:
                flash("An Error has occurred, please contact support", "danger")
                return redirect('/')
        else:
            flash("An Error has occurred, please contact support", "danger")
            return redirect('/')

    # Caso haja erros de status ou conexão
    except Exception as e:
        flash("An Error has occurred, please contact support", "error")
        return redirect('/')


# Efetua o registo
@app.route('/registo', methods=['POST'])
def registo():
    try:
        if request.method == 'POST':
            params = request.form.to_dict();

            # Fazer o trim dos fields e verificar se estao vazios
            params, valid = Common.trim_params(params)

            if not valid:
                flash('Please fill all fields', "danger")
                return redirect('/')

            url = SerRoutes.ROUTES['registo']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                session['user'] = \
                    {
                        '2fa_logged': False,
                        '2fa_token': response_params['token_2fa'],
                        'username': response_params['username'],
                        'jwt_token': response_params['jwt_token'],
                    }
                flash("Welcome", "primary")
                return redirect(url_for('login_2fa'))
            elif response_params['status'] == 'NOK':
                flash(response_params['message'], "danger")
                return redirect('/')
            else:
                flash("An Error has occurred, please contact support", "error")
                return redirect('/')

        else:
            flash("An Error has occurred, please contact support", "error")
            return redirect('/')
            # return Common.create_response_message(200, False, 'Ocorreu um erro')
    # Caso haja erros de status ou conexão
    except Exception as e:
        flash("An Error has occurred, please contact support", "error")
        return redirect('/')
        # return Common.create_response_message(200, False, 'Ocorreu um erro')


# endregion

# region 2fa
@app.route('/login/2fa', methods=['GET', 'POST'])
def login_2fa():
    try:
        if request.method == 'POST':
            params = request.form.to_dict()
            params, valid = Common.trim_params(params)

            if not valid:
                flash('Please fill all fields', "danger")
                return redirect('/')

            params['jwt_token'] = session['user']['jwt_token']
            url = SerRoutes.ROUTES['login_2fa']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                session['user'] = \
                    {
                        '2fa_logged': True,
                        'username': session['user']['username'],
                        'jwt_token': session['user']['jwt_token'],
                    }
                return redirect('/inheritedwills')
            elif response_params['status'] == 'NOK':
                flash(response_params['message'], "danger")
                return redirect('/')
            elif response_params['status'] == 'NOK_TOKEN':
                flash('Token Expired', 'danger')
                return redirect('/cancel_2fa')
            else:
                return redirect('/')
        else:
            # ir buscar secret key do user, por enquanto usar random
            secret = pyotp.random_base32()
            uri = pyotp.totp.TOTP(secret).provisioning_uri(name=(session['user']['username']),
                                                           issuer_name='A Very Special Will')
            secreturi = uri
            return render_template('login_2fa.html', secret=secret, secreturi=secreturi)
    # Caso haja erros de status ou conexão
    except Exception  as e:
        print(e)
        return Common.create_response_message(200, False, 'Ocorreu um erro')


@app.route('/login/cancel2fa', methods=['GET'])
def cancel_2fa():
    session.pop('user', None)
    return redirect('/')


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get("data", "")
    return send_file(qrcode(data, mode="raw"), mimetype="image/png")


# endregion

@app.route('/createwill', methods=['POST', 'GET'])
def createwill():
    try:
        if request.method == 'POST':
            params = request.get_json()
            params, valid = Common.trim_params(params)

            if not valid:
                flash('Please fill all fields', "danger")
                return redirect('/createwill')

            message, valid = Common.test_create_will(params)
            if not valid:
                return message

            params['jwt_token'] = session['user']['jwt_token']
            url = SerRoutes.ROUTES['createwill']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                return Common.create_response_message(200, True)
            elif response_params['status'] == 'NOK':
                return Common.create_response_message(200, False, response_params['message'])
            elif response_params['status'] == 'NOK_TOKEN':
                flash('Token Expired', 'danger')
                return redirect('/cancel_2fa')
            else:
                return Common.create_response_message(200, False, 'Ocorreu um erro')
        else:
            return render_template('createwill.html')
    # Caso haja erros de status ou conexão
    except Exception as e:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


@app.route('/inheritedwills', methods=['POST', 'GET'])
def inheritedwills():
    try:
        params = {}
        params['jwt_token'] = session['user']['jwt_token']
        url = SerRoutes.ROUTES['inheritwill']
        response = requests.post(url, json=params)

        # Caso a resposta nao seja ok
        if response.status_code != 200:
            raise Exception()

        # Tratamento da resposta
        response_params = response.json()

        if response_params['status'] == 'OK':
            wills_list = response_params['rows']
            wills_list = Common.sanitize_rows(wills_list)
            return render_template('inheritedwills.html', wills_list=wills_list)
        elif response_params['status'] == 'NOK_TOKEN':
            flash('Token Expired', 'danger')
            return redirect('/cancel_2fa')
    # Caso haja erros de status ou conexão
    except Exception as e:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


@app.route('/willview', methods=['POST', 'GET'])
def willview():
    try:
        if request.method == 'GET':
            params = {}
            params['will_id'] = escape(request.args.get('id'))
            params['jwt_token'] = session['user']['jwt_token']
            url = SerRoutes.ROUTES['hasaccesstowill']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK':
                if response_params['access']:
                    dead_man_params = response_params['dea_man_will_info']
                    dead_man_params = Common.sanitize_rows(dead_man_params)
                    return render_template('willview.html', dead_man_params=dead_man_params)
                else:
                    return redirect('/inheritedwills')
            elif response_params['status'] == 'NOK_TOKEN':
                flash('Token Expired', 'danger')
                return redirect('/cancel_2fa')
        elif request.method == 'POST':
            params = {}
            params['will_id'] = escape(request.args.get('id'))
            params['jwt_token'] = session['user']['jwt_token']

            url = SerRoutes.ROUTES['decypherwill']
            response = requests.post(url, json=params)

            # Caso a resposta nao seja ok
            if response.status_code != 200:
                raise Exception()

            # Tratamento da resposta
            response_params = response.json()
            if response_params['status'] == 'OK_ACCESS':
                if response_params['access']:
                    dead_man_params = response_params['dea_man_will_info']
                    dead_man_params = Common.sanitize_rows(dead_man_params)
                    flash(response_params['message'], 'danger')
                    return render_template('willview.html', dead_man_params=dead_man_params)
                else:
                    return redirect('/inheritedwills')
            elif response_params['status'] == 'NOK_TOKEN':
                flash('Token Expired', 'danger')
                return redirect('/cancel_2fa')
            else:
                return redirect('/inheritedwills')

    # Caso haja erros de status ou conexão
    except Exception as e:
        return Common.create_response_message(200, False, 'Ocorreu um erro')


# region beforeRequest
@app.before_request
def before_request():
    request_guest_handpoints = ['login', 'registo', 'qrcode', 'main', 'sendemail', 'static']

    # for testing
    # request_guest_handpoints.append('createwill')
    # request_guest_handpoints.append('inheritedwills')

    if 'user' in session:
        g.user = session['user']
        # os gets de css ou de logout
        if request.endpoint in ['static', 'cancel_2fa', 'logout'] or request.endpoint is None:
            return
        # caso esteja logged in mas nao tenha feito o 2fa
        if not session['user']['2fa_logged'] and request.endpoint != 'login_2fa':
            flash('Please Authenticate Using 2FA', 'danger')
            return redirect(url_for('login_2fa'))
        # caso esteja logged in mas nao tenha feito o 2fa
        else:
            g.user = session['user']
            return
    elif request.endpoint not in request_guest_handpoints:
        flash("Sem Acesso", "error")
        return redirect(url_for('main'))
    else:
        return


# endregion

# region errorHandling
# Como é por ajax, mudo o primeiro parametro para json, e retorno uma mensagem de erro
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    # caso seja ajax
    if request.is_xhr:
        return Common.create_response_message(400, True, 'Csrf Inválido', {'CsrfError': True})
    else:
        flash('Invalid Csrf Token', 'danger')
        return redirect('/')


# endregion

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    app.run(ssl_context=(dir_path + '/cert.pem', dir_path + '/key.pem'), port='32182')

# response = requests.get("http://149.90.108.93:80")
