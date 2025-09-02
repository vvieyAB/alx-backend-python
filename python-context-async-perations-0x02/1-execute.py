import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name='users.db'):
        self.query = query
        self.params = params
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        # Open the database connection and execute the query
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Execute the query with parameters if provided
        if self.params:
            self.cursor.execute(self.query, self.params)
        else:
            self.cursor.execute(self.query)
        
        # Fetch all results
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        
        # Return False to propagate exceptions
        return False

# Using the context manager to execute the query with parameter
with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("Users over 25 years old:")
    for row in results:
        print(row)