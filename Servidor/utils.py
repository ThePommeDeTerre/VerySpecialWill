"""
Validation of user inputs
"""

from hashlib import pbkdf2_hmac
from flask_mysqldb import MySQLdb
from settings import JWT_SECRET_KEY
import os
import jwt


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"] <= 255 and len(kwargs["password"]) <= 255 ):
            return True
        else:
            return False

def generate_salt():
    salt = os.urandom(128)
    return salt.hex()

def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac (
        "sha512",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()

# write password to database
def db_write(query, params):
    cursor = db.connection.cursor()
    try:
        cursor.execute(query, params)
        db.connection.commit()
        cursor.close()

        return True
    
    except MySQLdb._exceptions.IntegrityError:
        cursor.close()
        return False

# login with the credentials
def db_read(query, params=None):
    cursor = db.connection.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    entries = cursor.fetchall()
    cursor.close()

    content = []

    for entry in entries:
        content.append(entry)

    return content

# generate a JWT to respond to the user
def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS512")
    token = str(encoded_content).split("'")[1]
    return token

# verification of the provided credentials and the stored ones in the database
def validate_user(email, password):
    current_user = db_read("""SELECT * FROM users WHERE email = %s""", (email,))

    if len(current_user) == 1:
        saved_password_hash = current_user[0]["password_hash"]
        saved_password_salt = current_user[0]["password_salt"]
        password_hash = generate_hash(password, saved_password_salt)

        if password_hash == saved_password_hash:
            user_id = current_user[0]["id"]
            jwt_token = generate_jwt_token({"id": user_id})
            return jwt_token
        else:
            return False
    else:
        return False    