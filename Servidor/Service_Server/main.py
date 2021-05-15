"""

Authentication Server main file

"""

from flask import Flask
from blueprint_service import service_blueprint

app = Flask(__name__)

app.register_blueprint(service_blueprint, url_prefix='/service')

if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
