import toga
import warnings

from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from proment.database import DatabaseHandler
from proment.data_container import DataContainer



class HausverwaltungApp(toga.App):
    def startup(self):
        self.db_handler = DatabaseHandler()
        self.data_container = DataContainer(self.db_handler)
        
        # Main Window setup
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Commands (Menu items)
        new_cmd = toga.Command(
            self.action_new,
            text='New',
            tooltip='Create a new database file',
            group=toga.Group.FILE,
            order=0
        )
        open_cmd = toga.Command(
            self.action_open,
            text='Open',
            tooltip='Open a database file',
            group=toga.Group.FILE,
            order=1
        )
        save_cmd = toga.Command(
            self.action_save,
            text='Save',
            tooltip='Save data',
            group=toga.Group.FILE,
            order=2
        )
        
        # Edit commands
        copy_cmd = toga.Command(
            self.action_copy,
            text='Copy',
            group=toga.Group.EDIT,
            order=1
        )
        paste_cmd = toga.Command(
            self.action_paste,
            text='Paste',
            group=toga.Group.EDIT,
            order=2
        )

        # Settings command
        settings_cmd = toga.Command(
            self.action_settings,
            text='Show Metrics',
            group=toga.Group.SETTINGS
        )

        self.commands.add(new_cmd, open_cmd, save_cmd, copy_cmd, paste_cmd, settings_cmd)

        # Layout with Tabs
        main_box = toga.Box(style=Pack(direction=COLUMN, margin=10))
        
        # Welcome label
        label = toga.Label(
            'Welcome to Toga Hausverwaltung!',
            style=Pack(margin=(0, 0, 10, 0))
        )
        main_box.add(label)
        
        # Create tabbed interface
        self.tab_container = toga.Selection(style=Pack(flex=1))
        
        # # Properties Tab
        properties_box = self.create_properties_tab()
        self.tab_container.add("Properties", properties_box)
        #
        # # Tenants Tab
        # tenants_box = self.create_tenants_tab()
        # self.tab_container.add("Tenants", tenants_box)
        #
        # main_box.add(self.tab_container)

        self.main_window.content = main_box
        self.main_window.show()
    
    def create_properties_tab(self):
        """Create the Properties tab with table display."""
        properties_container = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=10))
        
        # Title
        title = toga.Label(
            'Properties Overview',
            style=Pack(margin=5, font_size=14, font_weight='bold')
        )
        properties_container.add(title)
        
        # Create table columns for Properties
        columns = [
            ('ID', 'id'),
            ('Zipcode', 'zipcode'),
            ('City', 'city'),
            ('Street', 'street'),
            ('House #', 'housenumber'),
            ('Unit', 'unit'),
            ('Floor', 'floor'),
            ('Description', 'description'),
        ]
        
        # Store as instance variable for later updates
        self.properties_table = toga.Table(
            headings=['ID', 'Zipcode', 'City', 'Street', 'House #', 'Unit', 'Floor', 'Description'],
            data=[],
            style=Pack(flex=1, margin=5)
        )
        
        properties_container.add(self.properties_table)
        
        # Add button for refreshing
        refresh_btn = toga.Button(
            'Refresh Data',
            on_press=self.refresh_properties_data,
            style=Pack(margin=5, width=150)
        )
        properties_container.add(refresh_btn)
        
        return properties_container
    
    def create_tenants_tab(self):
        """Create the Tenants tab with table display."""
        tenants_container = toga.Box(style=Pack(direction=COLUMN, flex=1, margin=10))
        
        # Title
        title = toga.Label(
            'Tenants Overview',
            style=Pack(margin=5, font_size=14, font_weight='bold')
        )
        tenants_container.add(title)
        
        # Create table for Tenants
        self.tenants_table = toga.Table(
            headings=['ID', 'House ID', 'Family Name', 'Surname', 'Start Date', 'End Date', 'Email', 'Phone', 'People'],
            data=[],
            style=Pack(flex=1, margin=5)
        )
        
        tenants_container.add(self.tenants_table)
        
        # Add button for refreshing
        refresh_btn = toga.Button(
            'Refresh Data',
            on_press=self.refresh_tenants_data,
            style=Pack(margin=5, width=150)
        )
        tenants_container.add(refresh_btn)
        
        return tenants_container
    
    def refresh_properties_data(self, widget):
        """Refresh the properties table with data from the database."""
        try:
            if self.data_container.db_handler.connection:
                self.data_container.load_data()
                df = self.data_container.properties_df
                
                if not df.empty:
                    # Convert DataFrame to table data format
                    table_data = []
                    for _, row in df.iterrows():
                        table_data.append((
                            str(row.get('id', '')),
                            str(row.get('zipcode', '')),
                            str(row.get('city', '')),
                            str(row.get('street', '')),
                            str(row.get('housenumber', '')),
                            str(row.get('unit', '')),
                            str(row.get('floor', '')),
                            str(row.get('description', ''))
                        ))
                    self.properties_table.data = table_data
                else:
                    self.properties_table.data = []
                    print("No properties data available")
        except Exception as e:
            print(f"Error refreshing properties: {e}")
    
    def refresh_tenants_data(self, widget):
        """Refresh the tenants table with data from the database."""
        try:
            if self.data_container.db_handler.connection:
                self.data_container.load_data()
                df = self.data_container.tenants_df
                
                if not df.empty:
                    # Convert DataFrame to table data format
                    table_data = []
                    for _, row in df.iterrows():
                        table_data.append((
                            str(row.get('id', '')),
                            str(row.get('house_id', '')),
                            str(row.get('family_name', '')),
                            str(row.get('surname', '')),
                            str(row.get('start_date', '')),
                            str(row.get('end_date', '')),
                            str(row.get('email', '')),
                            str(row.get('phone_number', '')),
                            str(row.get('amount_people', ''))
                        ))
                    self.tenants_table.data = table_data
                else:
                    self.tenants_table.data = []
                    print("No tenants data available")
        except Exception as e:
            print(f"Error refreshing tenants: {e}")

    async def action_new(self, widget):
        try:
            file_path = await self.main_window.dialog(
                toga.SaveFileDialog(
                    title="Create New SQLite Database",
                    suggested_filename="../../examples/database.db",
                    file_types=['db', 'sqlite', 'sqlite3']
                )
            )
            if file_path:
                print(f"Creating new database: {file_path}")
                self.db_handler.close_connection()
                self.db_handler.open_connection(str(file_path))
                self.data_container.create_tables()
                # Refresh tables
                self.refresh_properties_data(None)
                self.refresh_tenants_data(None)
        except ValueError:
            # User cancelled selection
            pass

    async def action_open(self, widget):
        try:
            file_path = await self.main_window.dialog(
                toga.OpenFileDialog(
                    title="Open SQLite Database",
                    multiple_select=False,
                    file_types=['db', 'sqlite', 'sqlite3']
                )
            )
            if file_path:
                print(f"Selected file: {file_path}")
                self.db_handler.close_connection()
                self.db_handler.open_connection(str(file_path))
                self.data_container.create_tables()
                # Refresh tables
                self.refresh_properties_data(None)
                self.refresh_tenants_data(None)
        except ValueError:
            # User cancelled selection
            pass

    def action_save(self, widget):
        print("Save clicked")

    def action_copy(self, widget):
        print("Copy clicked")

    def action_paste(self, widget):
        print("Paste clicked")

    def action_settings(self, widget):
        print("Show Metrics clicked")

    def on_exit(self, widget=None):
        self.db_handler.close_connection()
        return True

def main():
    return HausverwaltungApp('Hausverwaltung', 'net.heumann.hausverwaltung')

