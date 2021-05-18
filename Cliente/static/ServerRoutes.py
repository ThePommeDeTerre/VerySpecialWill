# IP = "149.90.108.93"
IP = "localhost"
PORT = "5005"

SERVER = "http://" + IP + ":" + PORT + "/"
ROUTES = {
    'login': SERVER + "auth/login",
    'registo': SERVER + "auth/register"
}
