# Import the QueryBase class
# YOUR CODE HERE
from .query_base import QueryBase

# Create a subclass of QueryBase
# called  `Team`
class Team(QueryBase):
    # Set the class attribute `name`
    # to the string "team"
    def __init__(self):
        self.name = 'team'
        super().__init__()

    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
        
        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
    def names(self):
        # Query 5: Select team_name and team_id from the team table for all teams
        sql_query = f"""
            SELECT team_name, team_id
            FROM {self.name}
        """
        # Execute the query and return the result as a list of tuples
        return self.queryMixin(sql_query)
    

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
    def username(self, team_id):
        # Query 6: Select team_name where team_id matches the provided ID
        sql_query = f"""
            SELECT team_name
            FROM {self.name}
            WHERE team_id = {team_id}
        """
        # Execute the query and return the result as a list of tuples
        return self.queryMixin(sql_query)


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    def model_data(self, id):
        sql_query = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        return self.pandas_query(sql_query)