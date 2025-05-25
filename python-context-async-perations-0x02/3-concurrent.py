#!/usr/bin/python3

"""
run multiple database queries concurrently using
asyncio

"""

import aiosqlite
import asyncio


async def async_fetch_users():
    async with aiosqlite.connect('users.db') as connection:
        cursor = await connection.execute('SELECT * FROM users;')
        rows = await cursor.fetchall()
        return rows


async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as connection:
        cursor = await connection.execute('SELECT * FROM users WHERE age > ?;', (40,))
        rows = await cursor.fetchall()
        return rows


async def fetch_concurrently():
    batch = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    result_fetch_users, result_fetch_older_users = batch

    for row in result_fetch_users:
        print(row)

    for row in result_fetch_older_users:
        print(row)




if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
