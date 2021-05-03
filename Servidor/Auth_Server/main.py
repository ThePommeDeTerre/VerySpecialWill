"""

Authentication Server main file

"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

# initialize the Flask app and the MySQL configuration from env - obtained with settings.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@mysql:3306/'
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

db = MySQL(app)

# must be here to avoid circular imports
from blueprint_auth import authentication

import mysql.connector

try:
    conn = mysql.connector.connect(host='172.20.1.1',
                                         database='auth_DB',
                                         user='root')

    cursor = conn.cursor(prepared=True)
    # Parameterized query
    sql_insert_query = """ INSERT INTO users
                       username, email, password_salt, password_hash) VALUES (%s, %s, %s, %s)"""
    # tuple to insert at placeholder
    tuple1 = ("cu", "cu@email", "1234jh2b34u12", "iodsghfverhg")

    cursor.execute(sql_insert_query, tuple1)
    conn.commit()
    print("Data inserted successfully into employee table using the prepared statement")

except mysql.connector.Error as error:
    print("parameterized query failed {}".format(error))
    exit


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
