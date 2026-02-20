
import pandas as pd

from proment.sql.database import DatabaseHandler
from proment.sql.datacontainer import DataContainer
from proment.logger import UniversalLogger

class PropertyContainer(DataContainer):
    def __init__(self, db_handler: DatabaseHandler):
        super().__init__(db_handler)
        self.load_data()

    def load_data(self):
        """Load all data from sqlite tables into pandas DataFrames."""
        if not self.db_handler.connection:
            return

        try:
            self.properties_df = pd.read_sql_query("SELECT * FROM properties", self.db_handler.connection)

            if not self.properties_df.empty and not self.tenants_df.empty:
                self.master_df = pd.merge(
                    self.tenants_df,
                    self.properties_df,
                    left_on='house_id',
                    right_on='id',
                    suffixes=('_tenant', '_property')
                )
        except pd.io.sql.DatabaseError as e:
            UniversalLogger.debug(f"Error loading properties data: {e}", caller_class='PropertyContainer')

    def create_tables(self):
        """Initialize the database schema if it doesn't exist."""
        if not self.db_handler.connection:
            return

        cursor = self.db_handler.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zipcode TEXT NOT NULL,
                city TEXT NOT NULL,
                street TEXT NOT NULL,
                housenumber TEXT NOT NULL,
                unit INTEGER NOT NULL,
                floor INTEGER NOT NULL,
                description TEXT
            )
        ''')
        self.db_handler.connection.commit()