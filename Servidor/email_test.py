from flask_mail import Mail, Message


def mail_config(app):
    # Configurações smtp para flask-email
    app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = 'ee8998e171334d'
    app.config['MAIL_DEFAULT_SENDER'] = 'ee8998e171334d'
    app.config['MAIL_PASSWORD'] = '674d5516a4c748'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    return Mail(app)


def test_send(mail):
    """
    Função de teste para enviar um email
    """

    # TODO: move to \Server

    try:
        msg = Message('crlh!', recipients=['takemyinfoandgo@gmail.com'])
        msg.body = "fuck me up"
        mail.send(msg)

    except Exception as e:
        print(e)