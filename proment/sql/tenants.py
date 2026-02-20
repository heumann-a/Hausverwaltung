from typing import List, Optional
import pandas as pd

from proment.sql.database import DatabaseHandler
from proment.sql.datacontainer import DataContainer
from proment.logger import UniversalLogger
from proment.sql.models import Tenant

class TenantsContainer(DataContainer):
    def __init__(self, db_handler: DatabaseHandler):
        super().__init__(db_handler)
        self.load_data()
    def create_tables(self):
        """Initialize the database schema if it doesn't exist."""
        if not self.db_handler.connection:
            return

        cursor = self.db_handler.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tenants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                house_id INTEGER NOT NULL,
                family_name TEXT NOT NULL,
                surname TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT,
                email TEXT,
                phone_number TEXT,
                amount_people INTEGER NOT NULL,
                FOREIGN KEY (house_id) REFERENCES properties (id)
                )
            ''')
        self.db_handler.connection.commit()

    def load_data(self):
        """Load all data from sqlite tables into pandas DataFrames."""
        if not self.db_handler.connection:
            return

        try:
            self.tenants_df = pd.read_sql_query("SELECT * FROM tenants", self.db_handler.connection)
        except pd.io.sql.DatabaseError as e:
            UniversalLogger.debug(f"Error loading tenants data: {e}", caller_class='TenantsContainer')

    def add(self, tenant: Tenant) -> int:
        cursor = self.db_handler.connection.cursor()
        cursor.execute(
            "INSERT INTO tenants (house_id, family_name, surname, start_date, end_date, email, phone_number, amount_people) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tenant.house_id, tenant.family_name, tenant.surname, tenant.start_date, tenant.end_date, tenant.email, tenant.phone_number, tenant.amount_people)
        )
        self.db_handler.connection.commit()
        return cursor.lastrowid

    def get_all(self, house_id: Optional[int] = None) -> List[Tenant]:
        cursor = self.db_handler.connection.cursor()
        if house_id:
            cursor.execute("SELECT id, house_id, family_name, surname, start_date, end_date, email, phone_number, amount_people FROM tenants WHERE house_id = ?", (house_id,))
        else:
            cursor.execute("SELECT id, house_id, family_name, surname, start_date, end_date, email, phone_number, amount_people FROM tenants")
        rows = cursor.fetchall()
        return [Tenant(id=row[0], house_id=row[1], family_name=row[2], surname=row[3], start_date=row[4], end_date=row[5], email=row[6], phone_number=row[7], amount_people=row[8]) for row in rows]
