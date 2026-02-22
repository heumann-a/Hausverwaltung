from typing import List, Optional

from proment.sql.connection import DatabaseConnection
from proment.sql.datacontainer import DataContainer
from proment.logger import UniversalLogger
from proment.sql.models import Tenant, Base


class TenantsContainer(DataContainer):
    def __init__(self, db_handler: DatabaseConnection):
        super().__init__(db_handler)
        self.load_data()

    def create_tables(self):
        """Initialize the database schema if it doesn't exist."""
        if not self.db_handler.session:
            return

        Base.metadata.create_all(self.db_handler.session)

    def load_data(self):
        """Load all data from database."""
        if not self.db_handler.session:
            return

        try:
            pass
        except Exception as e:
            UniversalLogger.debug(f"Error loading tenants data: {e}", caller_class='TenantsContainer')

    def add(self, tenant: Tenant) -> int:
        try:
            self.db_handler.session.add(tenant)
            self.db_handler.session.commit()
            return tenant.id
        except Exception as e:
            self.db_handler.session.rollback()
            UniversalLogger.debug(f"Error adding tenant: {e}", caller_class='TenantsContainer')
            raise

    def get_all(self, house_id: Optional[int] = None) -> List[Tenant]:
        try:
            query = self.db_handler.session.query(Tenant)
            if house_id:
                query = query.filter(Tenant.house_id == house_id)
            return query.all()
        except Exception as e:
            UniversalLogger.debug(f"Error retrieving tenants: {e}", caller_class='TenantsContainer')
            return []
