import time
import sqlite3 
import functools

query_cache = {}

def cache_query(func):
    """Decorator that caches database query results"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from arguments (assuming it's the first arg or keyword 'query')
        query = None
        
        # Check if query is passed as a positional argument
        if args and isinstance(args[0], str) and args[0].strip().upper().startswith('SELECT'):
            query = args[0]
        # Check if query is passed as a keyword argument
        elif 'query' in kwargs:
            query = kwargs['query']
        
        # If we found a query and it's in cache, return cached result
        if query and query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # If not in cache or not a query, execute the function
        result = func(*args, **kwargs)
        
        # Cache the result if it's a query
        if query:
            print(f"Caching result for query: {query}")
            query_cache[query] = result
        
        return result
    return wrapper