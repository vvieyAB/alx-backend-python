import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries with timestamps
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # The first argument is typically the SQL query
        if args:
            print(f"[{timestamp}] Query: {args[0]}")
        elif 'query' in kwargs:
            print(f"[{timestamp}] Query: {kwargs['query']}")
        else:
            print(f"[{timestamp}] Query executed (no query parameter found)")
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query, *args, **kwargs):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query, *args, **kwargs)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query with timestamp
users = fetch_all_users("SELECT * FROM users")