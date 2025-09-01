import sqlite3
import functools
import inspect

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the function signature to find the query parameter
        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        
        # Look for a parameter named 'query' in the function signature
        query_param = None
        for param_name, param_value in bound_args.arguments.items():
            if param_name == 'query':
                query_param = param_value
                break
        
        # Log the SQL query before execution
        if query_param:
            print(f"Executing SQL query: {query_param}")
        else:
            print("No query parameter found in function call")
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        return result
    return wrapper