import mysql.connector
from typing import Generator, Dict, List

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, str | int]], None, None]:
    """
    Generator function that fetches users in batches
    
    Args:
        batch_size: Number of rows to fetch at once
        
    Yields:
        List of dictionaries containing user data for each batch
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def batch_processing(batch_size: int = 50) -> Generator[Dict[str, str | int], None, None]:
   
   
    for batch in stream_users_in_batches(batch_size):  # First loop
        for user in batch:  # Second loop
            if user['age'] > 25:  # Filter condition
                yield user  # Yielding the filtered user
# Example usage
if __name__ == "__main__":
    for user in batch_processing(batch_size=10):
        print(user)
#         count = cursor.fetchone()[0]
#         if count == 0:
#             # If the table is empty, insert all data from the CSV file

#             with open(csv_file, 'r') as file:
#                 next(file)  # Skip the header row
#                 for row in file:
#                     # Validate UUID or generate a new one

#                     try:
#                         user_id = str(uuid.UUID(row['user_id']))
#                     except ValueError:
#                         user_id = str(uuid.uuid4())
#                     # Check if user_id already exists
#                     cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (user_id,))
#                     if not cursor.fetchone():
#                         cursor.execute("""

#                             INSERT INTO user_data (user_id, name, email, age)
#                             VALUES (%s, %s, %s, %s)
#                         """, (user_id, row['name'], row['email'], int(float(row['age']))))
#             connection.commit()
#             print("Data inserted successfully")
#         else:
#             print("Data already exists in the table")
#     finally:
#         if cursor:
#             cursor.close()
#         if connection:
#             connection.close()


#         if 'connection' in locals():
#             connection.close()

#     finally:
#         if cursor:    
