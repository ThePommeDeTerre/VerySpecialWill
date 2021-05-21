# IP = "149.90.108.93"
IP = "localhost"
PORT = "5000"

SERVER = "http://" + IP + ":" + PORT + "/"
ROUTES = {
    'login': SERVER + "auth/login",
    'registo': SERVER + "auth/register",
    'login_2fa': SERVER + "auth/login2fa",
    'createwill': SERVER + "service/create",
    'inheritwill': SERVER + "service/inheritpage",
    'hasaccesstowill': SERVER + "service/hasaccesstowill",
    'decypherwill': SERVER + "service/decypherwill",
}
