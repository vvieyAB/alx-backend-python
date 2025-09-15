#!/usr/bin/python3
import sqlite3


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database.
    
    Yields:
        int: The age of a single user
    """
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")
    
    # First loop: iterate through database rows
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        age = row[0]
        if age is not None:  # Skip null ages
            yield age
    
    conn.close()


def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.
    
    Returns:
        float: The average age of users
    """
    total_age = 0
    count = 0
    
    # Second loop: iterate through the generator
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    if count == 0:
        return 0.0
    
    return total_age / count


if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age}")