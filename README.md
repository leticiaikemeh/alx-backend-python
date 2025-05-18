# alx-backend-python

```markdown
# 🐍 Python Generators for Streaming MySQL Rows

## 📖 Overview

This project demonstrates how to use **Python generators** to efficiently stream rows from a MySQL database **one by one**, minimizing memory usage when working with large datasets.

---

## 🗂️ Project Structure

```

python-generators-0x00/

├── seed.py             # Database setup and streaming implementation

└── user_data.csv       # Sample data file (not included in this repo)

````

---

## ✨ Features

- ✅ MySQL database setup and configuration  
- ✅ Efficient data insertion from CSV files  
- ✅ Generator-based row streaming for memory-efficient data processing  
- ✅ Comprehensive error handling and resource management  

---

## 🛠️ Installation

1. Ensure you have **MySQL** installed and running locally.
2. Install the required Python packages:

```bash
pip install mysql-connector-python
````

---

## 🚀 Usage

### 🔧 Database Setup

Run the setup script to create the database and populate it with sample data:

```bash
./0-main.py
```

### 🔁 Streaming Rows

Use the generator to process rows one by one:

```python
from seed import connect_to_prodev, stream_rows

connection = connect_to_prodev()
if connection:
    for row in stream_rows(connection):
        # Process each row here
        print(row)
    connection.close()
```

---

## 🧾 Functions Documentation

| Function              | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `connect_db()`        | Connects to the MySQL database server.                 |
| `create_database()`   | Creates the `ALX_prodev` database if it doesn't exist. |
| `connect_to_prodev()` | Connects to the `ALX_prodev` MySQL database.           |
| `create_table()`      | Creates the `user_data` table with required fields.    |
| `insert_data()`       | Populates the database with data from a CSV file.      |
| `stream_rows()`       | Generator that yields rows from the `user_data` table. |

---

## 🗄️ Database Schema

The `user_data` table has the following structure:

| Column   | Type          | Constraints        |
| -------- | ------------- | ------------------ |
| user_id | VARCHAR(36)   | PRIMARY KEY, INDEX |
| name     | VARCHAR(255)  | NOT NULL           |
| email    | VARCHAR(255)  | NOT NULL           |
| age      | DECIMAL(10,0) | NOT NULL           |

---

## ✅ Best Practices

* Always close database connections when done.
* Use the streaming generator for large datasets to conserve memory.
* Validate data before insertion.
* Handle errors gracefully and roll back transactions when needed.

---

## 📄 License

This project is part of the **ALX Backend Python Curriculum** and is for educational purposes only.

---

## 📚 Related

> **alx-backend-python**
> Advanced Python programming
