from .sql_execution import QueryMixin

class QueryBase(QueryMixin):

    name=''

    def names(self):
        return list()


    def event_counts(self, id_arg):

        query_1 = f'''
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

        return super().pandas_query(query_1)
            

    def notes(self, id_arg):

        query_2 = f'''
            SELECT  n.note_date,
                    n.note
            FROM notes AS n
            WHERE n.{self.name}_id = {id_arg}
        '''

        return super().pandas_query(query_2)
