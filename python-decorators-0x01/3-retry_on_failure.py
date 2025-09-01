import time
import sqlite3 
import functools

def retry_on_failure(retries=3, delay=2):
    """Decorator that retries database operations on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_exception = None
            
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}")
                    
                    if attempt < retries:
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"All {retries} attempts failed")
                        raise last_exception
            
            return func(*args, **kwargs)
        return wrapper
    return decorator