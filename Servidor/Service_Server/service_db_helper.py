"""

Auxiliar methods to handle the Service Database

"""

from os import name
from dotenv.main import with_warn_for_invalid_lines
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from mysql.connector import cursor

from helpers.OurShamir import OurShamir
from helpers.OurAES import OurAES as AesHelper

from mysql.connector.cursor import CursorBase

import auth_db_helper as helper_auth
from base64 import b64encode


class DBHelper_service:
    dbConnection = None

    def __init__(self, filename='config_service.ini', section='mysql'):
        db_config = self.read_db_config_service(filename, section)

        # If we cannot connect let it crash
        self.dbConnection = MySQLConnection(**db_config)

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

    def check_if_user_exists(self, username):
        """
        Given the name of a user, we check if he already exists
        :param username: string
        """

        try:
            cursor = self.dbConnection.cursor(buffered=True)
            result = cursor.execute(
                "SELECT service_username FROM service_user WHERE service_username = %s", (username, ))

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
            # not insert duplicates
            cursor.execute(
                "INSERT IGNORE INTO service_user (service_username) VALUES (%s)", (username, ))

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
            # connect
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

    def insert_will(self, username, will_ct, will_hmac, will_sign, will_pub, min_shares,cripto_f,hash_f):
        try:
            cursor = self.dbConnection.cursor(prepared=True)
            query = "INSERT INTO will (will_message, will_hmac, will_sign, will_pub, user_owner, n_min_shares,cypher_id,hash_id) " \
                    "VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"

            args = (will_ct, will_hmac, will_sign,will_pub, username, min_shares,cripto_f,hash_f)

            cursor.execute(query, args)
            id_will = cursor.lastrowid

            cursor.close()
            return id_will

        except Error as e:
            print(e)
            return -1

    def insert_usershare(self):
        try:
            cursor = self.dbConnection.cursor(prepared=True)

            query = "INSERT INTO user_share (username_share, key_id_share, will_id_share)"

            cursor.commit()
            cursor.close()
            return True
        except Error as e:
            print(e)
            return False

    def insert_users_of_will(self, will_id, key, username_list, min_shares, n_shares, date_hash):
        try:
            secrets = OurShamir.split_secret(min_shares, n_shares, key)
            secrets_key = date_hash[-32:-16]

            aes_worker = AesHelper('ECB')

            for i, username in enumerate(username_list):
                secret_x = aes_worker.encrypt(secrets[i][0], secrets_key)
                secret_y = aes_worker.encrypt(secrets[i][1], secrets_key)
                secret_x = b64encode(secret_x).decode('utf-8')
                secret_y = b64encode(secret_y).decode('utf-8')

                cursor = self.dbConnection.cursor(prepared=True)
                query = "INSERT INTO share_key (value_of_key_x, value_of_key_y) Values (%s,%s)"
                cursor.execute(query, (secret_x, secret_y))
                key_id = cursor.lastrowid

                query = "INSERT INTO user_share (username_share, key_id_share, will_id_share) Values (%s,%s,%s)"
                cursor.execute(query, (username, key_id, will_id))

            cursor.close()
            return True
        except Error as e:
            print(e)
            return False

    def populate_page_with_wills(self, username):
        try:
            cursor = self.dbConnection.cursor(prepared=True)
            query = "SELECT w.will_id, w.n_min_shares, w.user_owner, s.active FROM will w "
            query += "INNER JOIN user_share u ON u.will_id_share = w.will_id "
            query += "INNER JOIN share_key s ON u.key_id_share = s.key_id "
            query += "WHERE username_share = (%s)"
            cursor.execute(query, (username,))

            # Iterate over every select that has (will_id, n_min_shares, user_owner)
            content = []
            for row in self.iter_row(cursor, 10):
                if not row:
                    break
                will_id, n_min_shares, user_owner, active = row

                content.append([will_id, user_owner, active, n_min_shares])

            cursor.close()
            return content

        except Exception as e:
            print(e)
            return []

    def has_access_to_will(self, username, will_id):
        try:
            cursor = self.dbConnection.cursor(prepared=True)
            query = "Select Count(*) from user_share "
            query += "WHERE will_id_share = %s AND username_share = %s "
            cursor.execute(query, (will_id, username,))
            count = cursor.fetchone()
            cursor.close()
            if count[0] == 1:
                cursor = self.dbConnection.cursor(prepared=True)
                query = "SELECT user_owner, n_min_shares from will WHERE will_id = %s "
                cursor.execute(query, (will_id,))
                user, n_min_shares = cursor.fetchone()
                cursor.close()
                return [user, n_min_shares], True
            else:
                return None, False

        except Exception as e:
            print(e)
            return None, False

    def commit(self):
        try:
            self.dbConnection.commit()
        except Error as e:
            print(e)

    def rollback(self):
        try:
            self.dbConnection.rollback()
        except Error as e:
            print(e)
