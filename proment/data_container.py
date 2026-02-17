from typing import List, Optional
import pandas as pd
from abc import ABC

from proment.database import DatabaseHandler
from proment.models import Property, Tenant

class DataContainer(ABC):
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler
        self.properties_df = pd.DataFrame()
        self.tenants_df = pd.DataFrame()
        self.master_df = pd.DataFrame()
        self.load_data()

    def load_data(self):
        """Load all data from sqlite tables into pandas DataFrames."""
        if not self.db_handler.connection:
            return

        try:
            self.properties_df = pd.read_sql_query("SELECT * FROM properties", self.db_handler.connection)
            self.tenants_df = pd.read_sql_query("SELECT * FROM tenants", self.db_handler.connection)
            
            if not self.properties_df.empty and not self.tenants_df.empty:
                self.master_df = pd.merge(
                    self.tenants_df,
                    self.properties_df,
                    left_on='house_id',
                    right_on='id',
                    suffixes=('_tenant', '_property')
                )
        except pd.io.sql.DatabaseError:
            # Tables might not exist yet
            pass

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

    def add_properties(self, prop: Property) -> int:
        cursor = self.db_handler.connection.cursor()
        cursor.execute(
            "INSERT INTO properties (zipcode, city, street, housenumber, unit, floor, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (prop.zipcode, prop.city, prop.street, prop.housenumber, prop.unit, prop.floor, prop.description)
        )
        self.db_handler.connection.commit()
        return cursor.lastrowid

    def get_properties(self) -> List[Property]:
        cursor = self.db_handler.connection.cursor()
        cursor.execute("SELECT id, zipcode, city, street, housenumber, unit, floor, description FROM properties")
        rows = cursor.fetchall()
        return [Property(id=row[0], zipcode=row[1], city=row[2], street=row[3], housenumber=row[4], unit=row[5], floor=row[6], description=row[7]) for row in rows]

    def add_tenant(self, tenant: Tenant) -> int:
        cursor = self.db_handler.connection.cursor()
        cursor.execute(
            "INSERT INTO tenants (house_id, family_name, surname, start_date, end_date, email, phone_number, amount_people) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tenant.house_id, tenant.family_name, tenant.surname, tenant.start_date, tenant.end_date, tenant.email, tenant.phone_number, tenant.amount_people)
        )
        self.db_handler.connection.commit()
        return cursor.lastrowid

    def get_tenants(self, house_id: Optional[int] = None) -> List[Tenant]:
        cursor = self.db_handler.connection.cursor()
        if house_id:
            cursor.execute("SELECT id, house_id, family_name, surname, start_date, end_date, email, phone_number, amount_people FROM tenants WHERE house_id = ?", (house_id,))
        else:
            cursor.execute("SELECT id, house_id, family_name, surname, start_date, end_date, email, phone_number, amount_people FROM tenants")
        rows = cursor.fetchall()
        return [Tenant(id=row[0], house_id=row[1], family_name=row[2], surname=row[3], start_date=row[4], end_date=row[5], email=row[6], phone_number=row[7], amount_people=row[8]) for row in rows]

class TenantsContainer(DataContainer):
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler
        self.properties_df = pd.DataFrame()
        self.tenants_df = pd.DataFrame()
        self.master_df = pd.DataFrame()
        self.load_data()

class PropertyContainer(DataContainer):
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler
        self.properties_df = pd.DataFrame()
        self.tenants_df = pd.DataFrame()
        self.master_df = pd.DataFrame()
        self.load_data()
