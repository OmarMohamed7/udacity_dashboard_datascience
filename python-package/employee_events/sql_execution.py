from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
current_dir = Path(__file__).parent

# Resolve the absolute path to the database file relative to the script's directory
db_path = (current_dir / 'employee_events.db').resolve()

# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    def __init__(self):
        # Initialize the connection attribute to None
        self.connection = None

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        print(db_path)
        if not self.connection:
            self.connection = connect(db_path)

    def _close_connection(self):
        """Closes the connection to the SQLite database."""
        if self.connection:
            self.connection.close()
            self.connection = None

    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query):
        # Use pandas to execute the SQL query and return a DataFrame
        try:
            self._connect()
            return pd.read_sql(sql_query, self.connection)
        finally:
            self._close_connection()

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def queryMixin(self, sql_query):
        # Use SQLite cursor to execute the query and fetch results as a list of tuples
        try:
            self._connect()
            cursor = self.connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()
            cursor.close()
            return result
        finally:
            self._close_connection()

 
# Leave this code unchanged
# def query(func):
#     """
#     Decorator that runs a standard sql execution
#     and returns a list of tuples
#     """

#     @wraps(func)
#     def run_query(*args, **kwargs):
#         query_string = func(*args, **kwargs)
#         connection = connect(db_path)
#         cursor = connection.cursor()
#         result = cursor.execute(query_string).fetchall()
#         connection.close()
#         return result
    
#     return run_query
