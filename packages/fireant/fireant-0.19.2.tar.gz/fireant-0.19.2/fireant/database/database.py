# coding: utf-8

import pandas as pd

from pypika import Query


class Database(object):
    # The pypika query class to use for constructing queries
    query_cls = Query

    def connect(self):
        raise NotImplementedError

    def trunc_date(self, field, interval):
        raise NotImplementedError

    def date_add(self, date_part, interval, field):
        """ Database specific function for adding or subtracting dates """
        raise NotImplementedError

    def fetch(self, query):
        with self.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()

    def fetch_dataframe(self, query):
        with self.connect() as connection:
            return pd.read_sql(query, connection)
