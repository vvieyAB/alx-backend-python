#!/usr/bin/python3
import sqlite3

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.

    Yields:
        dict: A dictionary containing user_id, name, email, and age
    """
    # Connect to your SQLite database (adjust if using a different DB)
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row  # allows fetching rows as dictionaries
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_data")

    # Only one loop as required
    for row in cursor:
        yield dict(row)

    conn.close()
