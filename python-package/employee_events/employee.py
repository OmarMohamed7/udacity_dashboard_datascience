# Import the QueryBase class
from .query_base import *
# Import dependencies needed for sql execution
# from the `sql_execution` module
from .sql_execution import *

# Define a subclass of QueryBase
# called Employee
class Employee(QueryBase):

    name = "employee"

    # Set the class attribute `name`
    # to the string "employee"
    def __init__(self):
        self.query_mixin = QueryMixin()  # Create an instance of QueryMixin


    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    
        
        # Query 3
        # Write an SQL query
        # that selects two columns 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data
        # for all employees in the database
    def names(self):
        query_str = f"""
            SELECT {self.name}_id, first_name || ' ' || last_name AS full_name
            FROM {self.name}
        """
        return self.query_mixin.query(query_str) 


    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
        
        # Query 4
        # Write an SQL query
        # that selects an employees full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee
        # with an id equal to the id argument
    def username(self, id):
        # Query 4
        # Write an SQL query that selects an employees full name
        # Use f-string formatting and a WHERE filter to only return the full name of the employee
        # with an id equal to the id argument
        qquery = f"""
            SELECT CONCAT(first_name, ' ', last_name) AS full_name
            FROM {self.name}
            WHERE {self.name}_id = {id}
        """
        return self.query_mixin.query(qquery)

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    def model_data(self, id):
        # Query 3: This is the original SQL query
        sql_query = f"""
            SELECT SUM(positive_events) positive_events
                 , SUM(negative_events) negative_events
            FROM {self.name}
            JOIN employee_events
            ON employee_events.{self.name}_id = {id}
        """
        # Return the result of the SQL query as a pandas DataFrame
        return self.query_mixin.pandas_query(sql_query)