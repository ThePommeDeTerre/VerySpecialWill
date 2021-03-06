"""

Here are defined the helper methods to communicate with the authetication database

"""


from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

from utils import generate_hash
from base64 import b64encode, b64decode


class DBHelper:
    dbConnection = None

    def __init__(self, filename='config.ini', section='mysql'):
        """
        Create the object
        """

        db_config = self.read_db_config(filename, section)

        # If we cannot connect let it crash
        self.dbConnection = MySQLConnection(**db_config)

    def close(self):
        self.dbConnection.close()

    def read_db_config(self, filename, section):
        """
        Get the database
        :param filename: name of the file where the configuration shoud the read
        :param section: database configuration
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
            raise Exception(
                '{0} not found in the {1} file'.format(section, filename))

        return db

    def iter_row(self, cursor, size=10):
        """
        Helper method to iterate over the rows of the table
        """

        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    def verify_user(self, username, password):
        """
        Verify is a given user is in the database
        """

        try:
            cursor = self.dbConnection.cursor(prepared=True)

            cursor.execute(
                "SELECT pwd_salt, pwd_hash FROM user_table WHERE username = %s", (username,))

            record = cursor.fetchone()

            if record is None:
                return False

            (salt, hash) = record

            pwd_hash = generate_hash(password, salt)
            if hash == pwd_hash:
                cursor.close()
                return True
            else:
                cursor.close()
                return False
        except Error as e:
            print(e)
            return False

    def insert_user(self, username, mail, pwd_salt, pwd_hash):
        """
        Insert one single user
        """

        query = "INSERT INTO user_table(username, mail, pwd_salt, pwd_hash) " \
                "VALUES(%s,%s,%s,%s)"
        args = (username, mail, pwd_salt, pwd_hash)

        try:
            cursor = self.dbConnection.cursor(prepared=True)
            cursor.execute(query, args)

            self.dbConnection.commit()
            return True
        except:
            return False

    def user_has_2fa(self, username):
        """
        Verify is 2FA for a given user is enabled and, if it is, the token is returned
        """

        try:
            cursor = self.dbConnection.cursor(prepared=True)

            cursor.execute(
                "SELECT fa2_token FROM user_table WHERE username = %s", (username,))

            # get the returned tuple
            (value_2fa,) = cursor.fetchone()

            # is is none then there is no matches
            if not bool(value_2fa):
                cursor.close()
                return "NOK"
            else:
                cursor.close()
                # convert to string
                return value_2fa

        except Error as e:
            print(e)
            return "NOK"

    def store_jwt(self, token, username):
        """
        IDC insert jwt in authentication database
        """

        try:
            cursor = self.dbConnection.cursor(prepared=True)
            query = "UPDATE user_table SET jwt = %s WHERE username = %s"
            cursor.execute(query, (token, username))

            cursor.close()
            self.dbConnection.commit()
            return True

        except Error as e:
            print(e)
            return False

    def get_user_info_for_2fa(self, username):
        """
        Get user info for 2fa encryption
        """

        try:
            cursor = self.dbConnection.cursor(buffered=True)
            cursor.execute(
                "SELECT created_at, pwd_salt, fa2_token FROM user_table WHERE username = %s", (username, ))
            (created_at, pwd_salt, fa2_token) = cursor.fetchone()
            cursor.close()

            if not username:
                return ""

            return created_at, pwd_salt, fa2_token

        except Error as e:
            print(e)
            return ""

    def insert_user_info_for_2fa(self, fa_crypt, username):
        try:
            cursor = self.dbConnection.cursor(prepared=True)

            query = "UPDATE user_table SET fa2_token = %s WHERE username = %s"
            cursor.execute(query, (b64encode(fa_crypt).decode(), username))

        except Error as e:
            print(e)
            return False

        finally:
            cursor.close()

        return True

    def get_jwt_from_user(self, username):
        """
        Get the most recent entry of jwt for a given user
        """

        try:
            cursor = self.dbConnection.cursor(buffered=True)

            cursor.execute(
                "SELECT jwt FROM user_table WHERE username = %s", (username, ))
            (jwt, ) = cursor.fetchone()
            cursor.close()

            if not jwt:
                return ""

            return jwt

        except Error as e:
            print(e)
            return ""

    def commit(self):
        try:
            self.dbConnection.commit()
        except Error as e:
            print(e)
