import mysql.connector
from typing import Generator, Dict

def stream_users() -> Generator[Dict[str, str | int], None, None]:
    """
    Generator function that streams rows from user_data table one by one
    
    Yields:
        Dictionary containing user data (user_id, name, email, age)
    """
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        cursor.execute("SELECT * FROM user_data")
        
        # Stream rows one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        # Clean up resources
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
