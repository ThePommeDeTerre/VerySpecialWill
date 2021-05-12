"""

Here are defined the helper methods to communicate with the authetication database

"""


from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

from utils import generate_hash

class DBHelper:
    dbConnection = None

    def __init__(self, filename='config.ini', section='mysql'):

        """
        Create the object
        """

        db_config = self.read_db_config(filename, section)
        
        self.dbConnection = MySQLConnection(**db_config) # If we cannot connect let it crash


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
            raise Exception('{0} not found in the {1} file'.format(section, filename))

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

            cursor.execute("SELECT pwd_salt, pwd_hash FROM user_table WHERE username = %s" , (username,))

            record = cursor.fetchone()

            if record is None:
                return False

            (salt, hash) = record
            
            pwd_hash = generate_hash(password, salt.decode())
            if hash.decode() == pwd_hash:
                return True
            else:
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

            cursor.execute("SELECT fa2_token FROM user_table WHERE username = %s" , (username,))

            # get the returned tuple
            (value_2fa,) = cursor.fetchone()

            # is is none then there is no matches
            if not value_2fa:
                return "NOK"
            else:
                # convert to string
                return value_2fa.decode()
        
        except Error as e:
            print(e)
            return "NOK"