import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure the connection is closed even if an error occurs
            conn.close()
    return wrapper

def transactional(func):
    """Decorator that automatically manages database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Execute the function within a transaction
            result = func(conn, *args, **kwargs)
            # If no exception was raised, commit the transaction
            conn.commit()
            print("Transaction committed successfully")
            return result
        except Exception as e:
            # If an exception occurred, rollback the transaction
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            # Re-raise the exception to maintain the error flow
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')