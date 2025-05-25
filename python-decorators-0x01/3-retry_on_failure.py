#!/usr/bin/python3

"""
decorator that retries database operations
if they fail due to errors

"""


import time
import sqlite3 
import functools

#### paste your with_db_decorator here


def retry_on_failure(retries=3, delay=1):
    """retries database operation """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries = 0
            while tries < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == retries:
                        raise e
                time.sleep(delay)
        
        return wrapper
    return decorator



def with_db_connection(func):
    """ decorator function"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('users.db')
        try:
            result = func(connection, *args, **kwargs)
        finally:
            connection.close()
        return result
    return wrapper


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_data")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
