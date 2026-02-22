from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from proment.logger import UniversalLogger
from proment.sql.models import Base


class DatabaseConnection:
    _instance = None
    engine = None
    SessionLocal = None
    session = None

    def __new__(cls):
        if cls._instance is None:
            UniversalLogger.debug('Creating the object', caller_class='DatabaseHandler')
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def open_connection(self, db_file):
        """Create a database connection to a SQLite database using SQLAlchemy"""
        try:
            db_url = f"sqlite:///{db_file}"
            self.engine = create_engine(db_url, echo=False)
            self.SessionLocal = sessionmaker(bind=self.engine)
            self.session = self.SessionLocal()

            Base.metadata.create_all(self.engine)
            UniversalLogger.debug(f"Successfully connected to SQLite: {db_file}", caller_class='DatabaseHandler')
        except Exception as e:
            UniversalLogger.debug(f"Error connecting to database: {e}", caller_class='DatabaseHandler')

    def close_connection(self):
        """Close the database connection"""
        if self.session:
            self.session.close()
            UniversalLogger.debug("SQLite connection closed", caller_class='DatabaseHandler')
            self.session = None
            self.engine = None
            self.SessionLocal = None
