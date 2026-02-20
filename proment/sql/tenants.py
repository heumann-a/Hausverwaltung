class TenantsContainer(DataContainer):
    def __init__(self, db_handler: DatabaseHandler):
        super().__init__(db_handler)
        self.load_data()

    def load_data(self):
        """Load all data from sqlite tables into pandas DataFrames."""
        if not self.db_handler.connection:
            return

        try:
            self.tenants_df = pd.read_sql_query("SELECT * FROM tenants", self.db_handler.connection)
        except pd.io.sql.DatabaseError as e:
            UniversalLogger.debug(f"Error loading tenants data: {e}", caller_class='TenantsContainer')

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