import sqlite3
import functools


def with_db_connection(func):
    """Decorator Function that creates db connection"""
    conn = sqlite3.connect('users.db')

    @functools.wraps (func)
    def wrapper_with_db_connection(*args, **kwags):
        try:
            result = func(conn, *args, **kwags)
        finally:
            conn.close()
        return result
    return wrapper_with_db_connection

def transactional(func):
    """Decorator function that commits changes or rolls back"""
    @functools.wraps (func)
    def wrapper_transactional(conn, *args, **kwags):
        try:
            result = func(conn, *args, **kwags)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
    return wrapper_transactional



@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')