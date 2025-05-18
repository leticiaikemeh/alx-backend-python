# This script connects to a MySQL database, retrieves user ages from a table,
# and calculates the average age using a generator function to stream the ages.
import mysql.connector
from typing import Generator

def stream_user_ages() -> Generator[int, None, None]:
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        
        # Stream ages one by one
        cursor.execute("SELECT age FROM user_data")
        while True:
            age = cursor.fetchone()
            if age is None:
                break
            yield age[0]  # Yield just the age value
            
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def calculate_average_age() -> float:
    total = 0
    count = 0
    
    for age in stream_user_ages():  # First loop
        total += age
        count += 1
    
    return total / count if count > 0 else 0

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")