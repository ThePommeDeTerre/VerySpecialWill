from flask_mail import Message


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