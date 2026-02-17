from PySide6.QtCore import Qt, QVariantAnimation, Signal, QObject, QSize, QTranslator, QLocale, QLibraryInfo, \
    Slot, QCoreApplication
from PySide6.QtGui import QTextOption, QPixmap, QTransform, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QCheckBox, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QPushButton, QDialog, QListWidgetItem, QListWidget



from proment.database import DatabaseHandler
from proment.data_container import DataContainer


class UI_MainWindow(QMainWindow):

    def __init__(self,):
        super(UI_MainWindow, self).__init__()
        self.db_handler = DatabaseHandler()
        self.data_container = DataContainer(self.db_handler)

    def init_main(self):
        self.db_handler = DatabaseHandler()
        self.data_container = DataContainer(self.db_handler)


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
    return UI_MainWindow()

