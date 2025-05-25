import sqlite3
import functools
import logging
from typing import Callable , Any , Tuple , List
from datetime import datetime

# Configure thread - safe logging
logger = logging.getLogger('db_queries')                        #creating custom logger
logger.setLevel(logging.DEBUG)                                   #set level
formatter = logging.Formatter(                                  #create formatter object
    '{asctime} - {levelname} - {message}', 
    style="{",
)
file_handler = logging.FileHandler('database_queries.log')      #create file handler
file_handler.setFormatter(formatter)                            #set file handler format
logger.addHandler(file_handler)                                 #add file handler
console_handler = logging.StreamHandler()                       #create console handler
console_handler.setFormatter (formatter)                        #set console handler format
logger.addHandler(console_handler)                              #add console handler                                  


def log_queries ( func : Callable [... , Any ]) -> Callable [... , Any ]:
    """
    Decorator to log SQL queries with parameters and execution time .

    Args :
    func : Function to decorate .
    Returns :
    Callable : Wrapped function with logging .
    """
    @functools . wraps ( func )
    def wrapper (* args , ** kwargs ) -> Any :
        query = args [0] if args else 'Unknown query'
        timestamp = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        logger.info( f" Executing query : {query}\n")
        try:
            result = func (*args , **kwargs )
            return result
        except Exception as e:
            logger.error ( f" Query failed : {e}")
            raise
    return wrapper

@log_queries
def fetch_all_users (query : str) -> List [ Tuple ]:
    """
    Fetch users from the database.
    Args :
    query : SQL query string.
    Returns :
    List of user records .
    """
    logger.debug("starting connection to fetch users from db")
    conn = sqlite3.connect(users.db)
    try:

        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        conn.close()
if __name__ == " __main__ ":
    try :
        logger.debug("starting program\n")
        users = fetch_all_users (" SELECT * FROM users ")
        for user in users :
            print (user)
    except sqlite3 . Error as e :
        print (f" Database error : {e}")
