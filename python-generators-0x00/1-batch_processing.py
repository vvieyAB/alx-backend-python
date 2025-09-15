#!/usr/bin/python3
import sqlite3

def stream_users_in_batches(batch_size):
    """
    Generator that streams users in batches from the user_data table.

    Args:
        batch_size (int): number of rows per batch

    Yields:
        list[dict]: A batch of users as dictionaries
    """
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield [dict(row) for row in rows]

    conn.close()


def batch_processing(batch_size):
    """
    Process batches to filter users over the age of 25

    Args:
        batch_size (int): number of rows per batch
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user["age"] > 25:  # filtering
                print(user)
