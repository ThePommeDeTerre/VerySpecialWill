from flask import Flask, render_template
from flask_cors import CORS
from flask_mysqldb import MySQL
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from blueprint_auth import authentication
import json

app = Flask(__name__)

# initialize the Flask app and the MySQL configuration from env - obtained with setting.py
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

db = MySQL(app)

app.register_blueprint(authentication, url_prefix="/api/auth")


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
