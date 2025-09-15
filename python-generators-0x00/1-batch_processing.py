#!/usr/bin/python3
import sqlite3


def stream_users_in_batches(batch_size):
    """
    Generator that streams rows from the user_data table in batches.

    Yields:
        tuple(sqlite3.Row, ...): a batch (sequence) of sqlite3.Row objects
    """
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    # loop 1
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        # yield the raw rows (conversion to dict happens later)
        yield rows

    conn.close()


def batch_processing(batch_size):
    """
    Generator that consumes batches and yields users older than 25.

    Yields:
        dict: a single user record (user_id, name, email, age)
    """
    # loop 2 (over batches)
    for batch in stream_users_in_batches(batch_size):
        # loop 3 (over rows in a batch)
        for row in batch:
            user = dict(row)
            # ensure numeric comparison for age
            try:
                if int(user.get("age", 0)) > 25:
                    yield user
            except (TypeError, ValueError):
                # skip rows with invalid age values
                continue
