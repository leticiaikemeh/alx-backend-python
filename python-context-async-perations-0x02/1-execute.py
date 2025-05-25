#!/usr/bin/python3

import sqlite3


class ExecuteQuery():
    """
    custom context manager that 
    takes a query and param as input and execute it
    manages both connection and query execution
    """
    
    def __init__(self, db_name, query, param):
        self.db_name = db_name
        self.query = query
        self.param = param
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, (self.param,))
        return self.cursor


    def __exit__(self, exc_value, exc_type, traceback):
        self.connection.close()


with ExecuteQuery('users.db', 'SELECT * FROM users WHERE age > ?', 25) as cursor:
    users = cursor.fetchall()
    for user in users:
        print(user)
