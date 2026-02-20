import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout,
    QTabWidget, QLabel, QFileDialog, QStatusBar
)

from proment.sql.database import DatabaseHandler
from proment.sql.datacontainer import DataContainer
from proment.gui.properties_tab import PropertiesTab
from proment.gui.tenants_tab import TenantsTab
from proment.logger import UniversalLogger
from proment.sql.property import PropertyContainer
from proment.sql.tenants import TenantsContainer


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

        self.properties_tab = PropertiesTab(PropertyContainer(self.db_handler))
        self.tab_widget.addTab(self.properties_tab, "Properties")
        
        # Tenants Tab
        self.tenants_tab = TenantsTab(TenantsContainer(self.db_handler))
        self.tab_widget.addTab(self.tenants_tab, "Tenants")
        
        self.setStatusBar(QStatusBar())

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

    def action_new(self, widget=None):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Create New SQLite Database", "", "Database Files (*.db *.sqlite *.sqlite3)"
        )
        if file_path:
            UniversalLogger.debug(f"Creating new database: {file_path}", caller_class='UI_MainWindow')
            self.db_handler.close_connection()
            self.db_handler.open_connection(file_path)
            self.data_container.create_tables()
            self.properties_tab.refresh_data()
            self.tenants_tab.refresh_data()

    def action_open(self, widget=None):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open SQLite Database", "", "Database Files (*.db *.sqlite *.sqlite3)"
        )
        if file_path:
            UniversalLogger.debug(f"Selected file: {file_path}", caller_class='UI_MainWindow')
            self.db_handler.close_connection()
            self.db_handler.open_connection(file_path)
            self.properties_tab.refresh_data()
            self.tenants_tab.refresh_data()

    def action_save(self, widget=None):
        UniversalLogger.debug("Save clicked", caller_class='UI_MainWindow')

    def action_copy(self, widget=None):
        UniversalLogger.debug("Copy clicked", caller_class='UI_MainWindow')

    def action_paste(self, widget=None):
        UniversalLogger.debug("Paste clicked", caller_class='UI_MainWindow')

    def action_settings(self, widget=None):
        UniversalLogger.debug("Show Metrics clicked", caller_class='UI_MainWindow')

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
