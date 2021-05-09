"""

Here are defined the helper methods to communicate with the authetication database

"""


from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from utils import generate_hash

class DBHelper:
    dbConnection = None

    def __init__(self, filename='config.ini', section='mysql'):
        db_config = self.read_db_config(filename, section)
        
        self.dbConnection = MySQLConnection(**db_config) # If we cannot connect let it crash

    """
    Get the database configuration
    """
    def read_db_config(self, filename, section):
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

    """
    Helper method to iterate over the rows of the table
    """
    def iter_row(self, cursor, size=10):
        while True:
            rows = cursor.fetchmany(size)
            if not rows:
                break
            for row in rows:
                yield row

    """
    Get many data from the table
    """
    def query_with_fetchmany(self):
        try:
            cursor = self.dbConnection.cursor()

            cursor.execute("SELECT * FROM user_table")

            for row in self.iter_row(cursor, 10):
                print(row)

        except Error as e:
            print(e)

    def verify_user(self, username, password):
        try:
            cursor = self.dbConnection.cursor()

            cursor.execute("SELECT pwd_salt, pwd_hash FROM user_table WHERE username = '%s'" % username)

            record = cursor.fetchone()

            if record is None:
                return False

            (salt, hash) = record   
            
            pwd_hash = generate_hash(password, salt)
            if hash == pwd_hash:
                return True
            else:
                return False
        except Error as e:
            print(e)
            return False

    """
    Insert one single user
    """
    def insert_user(self, username, mail, pwd_salt, pwd_hash):
        query = "INSERT INTO user_table(username, mail, pwd_salt, pwd_hash) " \
                "VALUES(%s,%s,%s,%s)"
        args = (username, mail, pwd_salt, pwd_hash)

        try:
            cursor = self.dbConnection.cursor()
            cursor.execute(query, args)

            self.dbConnection.commit()
            return True
        except:
            return False