#!/usr/bin/python3
from typing import Generator, List, Dict
import seed

def lazy_paginate(page_size: int) -> Generator[List[Dict[str, str | int]], None, None]:
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop when no more results
            break
        yield page
        offset += page_size

def paginate_users(page_size: int, offset: int) -> List[Dict[str, str | int]]:
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows