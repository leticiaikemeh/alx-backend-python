#!/usr/bin/python3
import sqlite3



class DatabaseConnection():
    """
    class based context manager to handle automatic
    opening and closing of database connections
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()



with DatabaseConnection('users.db') as connection:
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users;')
    users = cursor.fetchall()
    for user in users:
       print(user)


