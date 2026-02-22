import pandas as pd
from abc import ABC

from proment.sql.connection import DatabaseConnection


class DataContainer(ABC):
    def __init__(self, db_handler: DatabaseConnection):
        self.db_handler = db_handler

    def load_data(self):
        raise NotImplementedError

    def create_tables(self):
        raise NotImplementedError

    def add(self, other):
        raise NotImplementedError
    def get_all(self, other):
        raise NotImplementedError

    def error(self):
        if not self.properties_df.empty and not self.tenants_df.empty:
            self.master_df = pd.merge(
                self.tenants_df,
                self.properties_df,
                left_on='house_id',
                right_on='id',
                suffixes=('_tenant', '_property')
            )

