#!/usr/bin/python3
seed = __import__('seed')


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily paginates through user data, fetching one page at a time.
    
    Args:
        page_size (int): Number of users to fetch per page
        
    Yields:
        list: A page of user records (each user is a dictionary)
    """
    offset = 0
    
    while True:
        # Fetch the next page of users
        page = paginate_users(page_size, offset)
        
        # If no more users, break the loop
        if not page:
            break
            
        # Yield the current page
        yield page
        
        # Move to the next page
        offset += page_size