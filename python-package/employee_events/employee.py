# Import the QueryBase class
from .query_base import QueryBase

# Define a subclass of QueryBase
# called Employee
class Employee(QueryBase):

    name = 'employee'

    def names(self):

        query_3=f'''
            SELECT first_name || ' ' || last_name AS full_name, employee_id
            FROM {self.name}
        '''

        return self.query(query_3)


    def username(self, id_arg):

        query_4=f'''
            SELECT first_name || ' ' || last_name AS full_name, employee_id
            FROM {self.name}
            WHERE employee_id = {id_arg}
        '''

        return self.query(query_4)


    def model_data(self, id):

        return self.pandas_query(f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """)
