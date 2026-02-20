from typing import List
import pandas as pd

from proment.sql.database import DatabaseHandler
from proment.sql.datacontainer import DataContainer
from proment.logger import UniversalLogger
from proment.sql.models import Property

class PropertyContainer(DataContainer):
    def __init__(self, db_handler: DatabaseHandler):
        super().__init__(db_handler)
        self.load_data()

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

    def add(self, prop: Property) -> int:
        cursor = self.db_handler.connection.cursor()
        cursor.execute(
            "INSERT INTO properties (zipcode, city, street, housenumber, unit, floor, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (prop.zipcode, prop.city, prop.street, prop.housenumber, prop.unit, prop.floor, prop.description)
        )
        self.db_handler.connection.commit()
        return cursor.lastrowid

    def get_all(self) -> List[Property]:
        cursor = self.db_handler.connection.cursor()
        cursor.execute("SELECT id, zipcode, city, street, housenumber, unit, floor, description FROM properties")
        rows = cursor.fetchall()
        return [Property(id=row[0], zipcode=row[1], city=row[2], street=row[3], housenumber=row[4], unit=row[5], floor=row[6], description=row[7]) for row in rows]
