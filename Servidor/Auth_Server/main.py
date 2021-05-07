"""

Authentication Server main file

"""

from flask import Flask, render_template
from werkzeug import exceptions
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import mysql.connector
from mysql.connector import MySQLConnection, Error
from contextlib import closing
from configparser import ConfigParser

app = Flask(__name__)

# initialize the Flask app and the MySQL configuration from env - obtained with settings.py
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@172.20.1.1:3306/users'
#app.config["MYSQL_USER"] = MYSQL_USER
#app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
#app.config["MYSQL_DB"] = MYSQL_DB
#app.config["MYSQL_CURSORCLASS"] = "DictCursor"

#db = MySQL(app)

# must be here to avoid circular imports
#from blueprint_auth import authentication

#app.register_blueprint(authentication, url_prefix="/api/auth") 

def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to MySQL database """

    db_config = read_db_config()
    conn = None
    try:
        print('Connecting to MySQL database...')
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except Error as error:
        print(error)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print('Connection closed.') 

def iter_row(cursor, size=10):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row

def query_with_fetchmany():
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_table")

        for row in iter_row(cursor, 10):
            print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def insert_user(username, mail, pwd_salt, pwd_hash):
    query = "INSERT INTO user_table(username, mail, pwd_salt, pwd_hash) " \
            "VALUES(%s,%s,%s,%s)"
    args = (username, mail, pwd_salt, pwd_hash)

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.execute(query, args)

        conn.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    print(read_db_config())
    query_with_fetchmany()
    insert_user('antonia', 'antonia@mail.com', '12k4jnfwa', 'asldkf9438a')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug=True
    # listening in all ports
    app.run(host="0.0.0.0", port="80")
