import csv
import uuid
import mysql.connector
from mysql.connector import Error
from typing import Generator, Tuple, Any, Optional

def connect_db() -> Optional[mysql.connector.connection.MySQLConnection]:
    """Connects to the MySQL database server"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Creates the database ALX_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()

def connect_to_prodev() -> Optional[mysql.connector.connection.MySQLConnection]:
    """Connects to the ALX_prodev database in MySQL"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection: mysql.connector.connection.MySQLConnection) -> None:
    """Creates a table user_data if it does not exists with the required fields"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10,0) NOT NULL,
                INDEX (user_id)
            )
        """)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()

def insert_data(connection: mysql.connector.connection.MySQLConnection, csv_file: str) -> None:
    """Inserts data in the database if it does not exist"""
    try:
        cursor = connection.cursor()
        
        # First check if table is empty
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("Data already exists in the table")
            return
        
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Validate UUID or generate a new one
                try:
                    user_id = str(uuid.UUID(row['user_id']))
                except ValueError:
                    user_id = str(uuid.uuid4())
                
                # Check if user_id already exists
                cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, row['name'], row['email'], int(float(row['age']))))
        
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    except FileNotFoundError:
        print(f"Error: CSV file {csv_file} not found")
    finally:
        if cursor:
            cursor.close()

def stream_rows(connection: mysql.connector.connection.MySQLConnection) -> Generator[Tuple[Any, ...], None, None]:
    """
    Generator function that streams rows from the user_data table one by one
    
    Args:
        connection: MySQL database connection
    
    Yields:
        Tuple containing the row data
    """
    cursor = None
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
    except Error as e:
        print(f"Error streaming rows: {e}")
    finally:
        if cursor:
            cursor.close()
