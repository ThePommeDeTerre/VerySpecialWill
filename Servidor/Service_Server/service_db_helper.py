"""

Auxiliar methods to handle the Service Database

"""

from os import name
from dotenv.main import with_warn_for_invalid_lines
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from mysql.connector import cursor

from mysql.connector.cursor import CursorBase

import auth_db_helper as helper_auth

class DBHelper_service:
    dbConnection = None

    def __init__(self, filename='config_service.ini', section='mysql'):
        db_config = self.read_db_config_service(filename, section)
        
        self.dbConnection = MySQLConnection(**db_config) # If we cannot connect let it crash


    def close(self):
        self.dbConnection.close()


    def read_db_config_service(self, filename, section):

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

            
    def check_if_user_exists(self, username):

        """
        Given the name of a user, we check if he already exists
        :param username: string
        """

        try:
            cursor = self.dbConnection.cursor(buffered=True)
            result = cursor.execute("SELECT service_username FROM service_user WHERE service_username = %s" , (username, ))
           
            cursor.close()

            if not result:
                return False

            return True

        except Error as e:
            print(e)
            return False


    def insert_username(self, username):
        
        """
        Insert one single username
        :return: boolean depending on whether the operation is successful
        """

        try:
            cursor = self.dbConnection.cursor(buffered=True)
            cursor.execute("INSERT IGNORE INTO service_user (service_username) VALUES (%s)", (username, ))

            self.dbConnection.commit()
            cursor.close()
            return True

        except Error as e:
            print(e)
            return False



    def populate_service_with_auth(self):

        """
        Get the usernames from the authentication database and insert them in the service database
        :return: boolean depending on whether the operation is successful
        """

        try:
            dbHelper_auth = helper_auth.DBHelper_auth()
            usernames_auth = dbHelper_auth.get_all_usernames_authentication()

            dbHelper_auth.close()

            if not usernames_auth:
                return False

            for i in usernames_auth:
                if not self.check_if_user_exists(i):
                    self.insert_username(i)
                else:
                    continue        

            return True

        except Error as e:
            print(e)
            return False