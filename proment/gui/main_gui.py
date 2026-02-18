import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QTabWidget,
    QLabel, QMenuBar, QMenu, QFileDialog, QHeaderView, QStatusBar
)

from proment.database import DatabaseHandler
from proment.data_container import DataContainer

class UI_MainWindow(QMainWindow):
    def __init__(self, title="Hausverwaltung", app_id="net.heumann.hausverwaltung"):
        # Ensure QApplication exists before initializing QMainWindow
        self._app = QApplication.instance()
        if not self._app:
            self._app = QApplication(sys.argv)
            
        super(UI_MainWindow, self).__init__()
        self.setWindowTitle(title)
        self.resize(1000, 600)
        
        self.db_handler = DatabaseHandler()
        self.data_container = DataContainer(self.db_handler)
        
        self.setup_ui()
        self.setup_menus()
        
    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Welcome label
        self.welcome_label = QLabel("Welcome to Hausverwaltung!")
        self.welcome_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.main_layout.addWidget(self.welcome_label)
        
        # Tab container
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Properties Tab
        self.properties_tab = self.create_properties_tab()
        self.tab_widget.addTab(self.properties_tab, "Properties")
        
        # Tenants Tab
        self.tenants_tab = self.create_tenants_tab()
        self.tab_widget.addTab(self.tenants_tab, "Tenants")
        
        self.setStatusBar(QStatusBar())

    def create_properties_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("Properties Overview")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)
        
        self.properties_table = QTableWidget()
        self.properties_table.setColumnCount(8)
        self.properties_table.setHorizontalHeaderLabels([
            'ID', 'Zipcode', 'City', 'Street', 'House #', 'Unit', 'Floor', 'Description'
        ])
        self.properties_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.properties_table)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.setFixedWidth(150)
        refresh_btn.clicked.connect(lambda: self.refresh_properties_data())
        layout.addWidget(refresh_btn)
        
        return tab

    def create_tenants_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("Tenants Overview")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)
        
        self.tenants_table = QTableWidget()
        self.tenants_table.setColumnCount(9)
        self.tenants_table.setHorizontalHeaderLabels([
            'ID', 'House ID', 'Family Name', 'Surname', 'Start Date', 'End Date', 'Email', 'Phone', 'People'
        ])
        self.tenants_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tenants_table)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.setFixedWidth(150)
        refresh_btn.clicked.connect(lambda: self.refresh_tenants_data())
        layout.addWidget(refresh_btn)
        
        return tab

    def setup_menus(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.action_new)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.action_open)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.action_save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.action_copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.action_paste)
        edit_menu.addAction(paste_action)
        
        # Settings Menu
        settings_menu = menubar.addMenu("&Settings")
        
        metrics_action = QAction("Show &Metrics", self)
        metrics_action.triggered.connect(self.action_settings)
        settings_menu.addAction(metrics_action)

    def refresh_properties_data(self, widget=None):
        try:
            if self.data_container.db_handler.connection:
                self.data_container.load_data()
                df = self.data_container.properties_df
                
                self.properties_table.setRowCount(0)
                if not df.empty:
                    for i, (idx, row) in enumerate(df.iterrows()):
                        self.properties_table.insertRow(i)
                        self.properties_table.setItem(i, 0, QTableWidgetItem(str(row.get('id', ''))))
                        self.properties_table.setItem(i, 1, QTableWidgetItem(str(row.get('zipcode', ''))))
                        self.properties_table.setItem(i, 2, QTableWidgetItem(str(row.get('city', ''))))
                        self.properties_table.setItem(i, 3, QTableWidgetItem(str(row.get('street', ''))))
                        self.properties_table.setItem(i, 4, QTableWidgetItem(str(row.get('housenumber', ''))))
                        self.properties_table.setItem(i, 5, QTableWidgetItem(str(row.get('unit', ''))))
                        self.properties_table.setItem(i, 6, QTableWidgetItem(str(row.get('floor', ''))))
                        self.properties_table.setItem(i, 7, QTableWidgetItem(str(row.get('description', ''))))
                else:
                    print("No properties data available")
        except Exception as e:
            print(f"Error refreshing properties: {e}")

    def refresh_tenants_data(self, widget=None):
        try:
            if self.data_container.db_handler.connection:
                self.data_container.load_data()
                df = self.data_container.tenants_df
                
                self.tenants_table.setRowCount(0)
                if not df.empty:
                    for i, (idx, row) in enumerate(df.iterrows()):
                        self.tenants_table.insertRow(i)
                        self.tenants_table.setItem(i, 0, QTableWidgetItem(str(row.get('id', ''))))
                        self.tenants_table.setItem(i, 1, QTableWidgetItem(str(row.get('house_id', ''))))
                        self.tenants_table.setItem(i, 2, QTableWidgetItem(str(row.get('family_name', ''))))
                        self.tenants_table.setItem(i, 3, QTableWidgetItem(str(row.get('surname', ''))))
                        self.tenants_table.setItem(i, 4, QTableWidgetItem(str(row.get('start_date', ''))))
                        self.tenants_table.setItem(i, 5, QTableWidgetItem(str(row.get('end_date', ''))))
                        self.tenants_table.setItem(i, 6, QTableWidgetItem(str(row.get('email', ''))))
                        self.tenants_table.setItem(i, 7, QTableWidgetItem(str(row.get('phone_number', ''))))
                        self.tenants_table.setItem(i, 8, QTableWidgetItem(str(row.get('amount_people', ''))))
                else:
                    print("No tenants data available")
        except Exception as e:
            print(f"Error refreshing tenants: {e}")

    def action_new(self, widget=None):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Create New SQLite Database", "", "Database Files (*.db *.sqlite *.sqlite3)"
        )
        if file_path:
            print(f"Creating new database: {file_path}")
            self.db_handler.close_connection()
            self.db_handler.open_connection(file_path)
            self.data_container.create_tables()
            self.refresh_properties_data()
            self.refresh_tenants_data()

    def action_open(self, widget=None):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open SQLite Database", "", "Database Files (*.db *.sqlite *.sqlite3)"
        )
        if file_path:
            print(f"Selected file: {file_path}")
            self.db_handler.close_connection()
            self.db_handler.open_connection(file_path)
            self.data_container.create_tables()
            self.refresh_properties_data()
            self.refresh_tenants_data()

    def action_save(self, widget=None):
        print("Save clicked")

    def action_copy(self, widget=None):
        print("Copy clicked")

    def action_paste(self, widget=None):
        print("Paste clicked")

    def action_settings(self, widget=None):
        print("Show Metrics clicked")

    def closeEvent(self, event):
        self.db_handler.close_connection()
        event.accept()

    def main_loop(self):
        """Compatibility method for Toga-like app startup."""
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        self.show()
        sys.exit(app.exec())

def main():
    app = QApplication(sys.argv)
    window = UI_MainWindow()
    window.show()
    sys.exit(app.exec())
