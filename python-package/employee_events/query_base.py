# Import any dependencies needed to execute sql queries
from sql_execution import QueryMixin

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
class QueryBase(QueryMixin):

    # Create a class attribute called `name`
    # set the attribute to an empty string
    name=''

    # Define a `names` method that receives
    # no passed arguments
    def names(self):
        
        # Return an empty list
        return list()


    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    def event_counts(self, id_arg):

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column

        query_1 = f'''
            SELECT  e.event_date as event_date,
                    SUM(e.positive_events),
                    SUM(e.negative_events)
            FROM {self.name} AS t
            GROUP BY e.event_date
            ORDER BY e.event_date
        '''

        query_99 = f'''
            SELECT  e.event_date as event_date,
                    SUM(e.positive_events),
                    SUM(e.negative_events)
            FROM {self.name} AS t
            JOIN employee_events AS e
                ON e.{self.name}_id = t.{self.name}_id
            WHERE e.{self.name}_id = {id_arg}
            GROUP BY e.event_date
            ORDER BY e.event_date
        '''


        #return super().pandas_query(query_1)
        return "Hello"
            
    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    def notes(self, id_arg):

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        query_2 = f'''
            SELECT  n.note_date,
                    n.note
            FROM notes AS n
            WHERE n.{self.name}_id = {id_arg}
        '''

        return super().pandas_query(query_2)
