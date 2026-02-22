from typing import List

from proment.sql.connection import DatabaseConnection
from proment.sql.datacontainer import DataContainer
from proment.logger import UniversalLogger
from proment.sql.models import Property, Base

class PropertyContainer(DataContainer):
    def __init__(self, db_handler: DatabaseConnection):
        super().__init__(db_handler)
        self.load_data()

    def create_tables(self):
        """Initialize the database schema if it doesn't exist."""
        if not self.db_handler.engine:
            return


        Base.metadata.create_all(self.db_handler.engine)

    def load_data(self):
        """Load all data from database."""
        if not self.db_handler.session:
            return

        try:
            pass
        except Exception as e:
            UniversalLogger.debug(f"Error loading properties data: {e}", caller_class='PropertyContainer')

    def add(self, prop: Property) -> int:
        try:
            self.db_handler.session.add(prop)
            self.db_handler.session.commit()
            return prop.id
        except Exception as e:
            self.db_handler.session.rollback()
            UniversalLogger.debug(f"Error adding property: {e}", caller_class='PropertyContainer')
            raise

    def get_all(self) -> List[Property]:
        try:
            return self.db_handler.session.query(Property).all()
        except Exception as e:
            UniversalLogger.debug(f"Error retrieving properties: {e}", caller_class='PropertyContainer')
            return []
