"""

Auxiliar methods to handle the Authentication Database

"""

from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser

class DBHelper_auth:
    dbConnection = None

    def __init__(self, filename='config_auth.ini', section='mysql'):

        """
        Initialize object with reading the configuration
        """
        
        db_config = self.read_db_config(filename, section)
        
        self.dbConnection = MySQLConnection(**db_config) # If we cannot connect let it crash


    def read_db_config_auth(self, filename, section):
        
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

   
    def get_all_usernames_authentication(self):
   
        """
        Get all the usernames in the user_table
        """
        
        try:
            cursor = self.dbConnection.cursor(prepared=True)

            cursor.execute("SELECT username FROM user_table")

            for row in self.iter_row(cursor, 10):
                print(row)

        except Error as e:
            print(e)