import mysql.connector
from dotenv import load_dotenv
import os


class Sql:

    def __init__(self):
        load_dotenv()
        self.host = os.getenv('host')
        self.user = os.getenv('user')
        self.password = os.getenv('password')
        self.database = os.getenv('database')
        self.port = int(os.getenv('port'))
        self.db = mysql.connector.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database,
                                          port=self.port,
                                          autocommit=True)
        self.cursor = self.db.cursor(dictionary=True)
        self.table_name = 'user_words'

    def add_message(self, user_id, message):
        if self.user_id_exists(user_id):
            old_message = self.get_message(user_id=user_id)
            new_message = old_message + " " + message
            self.cursor.execute(f"UPDATE {self.table_name} SET message = %s WHERE discord_id = %s", (new_message, user_id))
        else:
            self.cursor.execute(f"INSERT INTO {self.table_name} (`discord_id`, `message`) VALUES (%s, %s)", (user_id, message))

    def get_table(self):
        self.cursor.execute(f"SELECT * FROM {self.table_name}")
        results = self.cursor.fetchall()
        return results

    def user_id_exists(self, user_id=447560916427472907):
        self.cursor.execute(f"SELECT COUNT(*) FROM {self.table_name} WHERE discord_id = {user_id}")
        user_ids = self.cursor.fetchall()[0]
        # Returns true if user id is found.
        return user_ids['COUNT(*)'] > 0

    def get_message(self, user_id):
        self.cursor.execute(f"SELECT message FROM {self.table_name} WHERE discord_id = {user_id}")
        message = self.cursor.fetchall()[0]
        return message['message']

    def clear_table(self):
        self.cursor.execute(f"DELETE FROM {self.table_name}")


# sql = Sql()
# print(sql.user_id_exists())
# sql.add_message()
#
# # sql.user_id_exists(123123)
# # sql.get_message(123123)
# sql.clear_table()
#
# print(sql.get_table())

