from .query_base import QueryBase

class Team(QueryBase):

    name = 'team'

    def names(self):

        query_5 = f'SELECT team_name, team_id FROM {self.name}'

        return self.query(query_5)


    def username(self, id_arg):

        query_6 = f'SELECT team_name, team_id FROM {self.name} WHERE team_id = {id_arg}'

        return self.query(query_6)


    def model_data(self, id):

        return self.pandas_query(f"""
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
                """)
