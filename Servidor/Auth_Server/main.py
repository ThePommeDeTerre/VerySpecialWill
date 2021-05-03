"""

Authentication Server main file

"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

# initialize the Flask app and the MySQL configuration from env - obtained with settings.py
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

db = MySQL(app)

# must be here to avoid circular imports
from blueprint_auth import authentication

app.register_blueprint(authentication, url_prefix="/api/auth")


@app.route('/login', methods=['POST'])
def run():
    return jsonify(
        {
            "status":"OK"
        }
    )


if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="88")
