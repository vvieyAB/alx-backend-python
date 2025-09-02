import sqlite3

class DatabaseConnection:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        # Open the database connection
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print(f"Connected to database: {self.db_name}")
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed")
        
        # Return False to propagate exceptions, True to suppress them
        return False

# Using the context manager to perform the query
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query results:")
    for row in results:
        print(row)