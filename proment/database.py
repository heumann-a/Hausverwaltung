import sqlite3
from sqlite3 import Error

class DatabaseHandler:
    _instance = None
    connection = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
        return cls._instance

    def open_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.connection = sqlite3.connect(db_file)
            print(f"Successfully connected to SQLite: {db_file}")
        except Error as e:
            print(f"Error connecting to database: {e}")

    def close_connection(self):
        """ close the database connection """
        if self.connection:
            self.connection.close()
            print("SQLite connection closed")
            self.connection = None
