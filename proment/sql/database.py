import sqlite3
from sqlite3 import Error
from proment.logger import UniversalLogger

class DatabaseHandler:
    _instance = None
    connection = None

    def __new__(cls):
        if cls._instance is None:
            UniversalLogger.debug('Creating the object', caller_class='DatabaseHandler')
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
        return cls._instance

    def open_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.connection = sqlite3.connect(db_file)
            UniversalLogger.debug(f"Successfully connected to SQLite: {db_file}", caller_class='DatabaseHandler')
        except Error as e:
            UniversalLogger.debug(f"Error connecting to database: {e}", caller_class='DatabaseHandler')

    def close_connection(self):
        """ close the database connection """
        if self.connection:
            self.connection.close()
            UniversalLogger.debug("SQLite connection closed", caller_class='DatabaseHandler')
            self.connection = None
