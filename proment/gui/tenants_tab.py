from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
from proment.logger import UniversalLogger

class TenantsTab(QWidget):
    def __init__(self, data_container, parent=None):
        super().__init__(parent)
        self.data_container = data_container
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
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
        refresh_btn.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_btn)

    def refresh_data(self):
        try:
            if self.data_container.db_handler.connection:
                # Use TenantsContainer to load data
                self.data_container.load_data()
                tenants = tenants_container.get_tenants()
                
                self.tenants_table.setRowCount(0)
                if tenants:
                    for i, tenant in enumerate(tenants):
                        self.tenants_table.insertRow(i)
                        self.tenants_table.setItem(i, 0, QTableWidgetItem(str(tenant.id if tenant.id is not None else '')))
                        self.tenants_table.setItem(i, 1, QTableWidgetItem(str(tenant.house_id)))
                        self.tenants_table.setItem(i, 2, QTableWidgetItem(tenant.family_name))
                        self.tenants_table.setItem(i, 3, QTableWidgetItem(tenant.surname))
                        self.tenants_table.setItem(i, 4, QTableWidgetItem(tenant.start_date))
                        self.tenants_table.setItem(i, 5, QTableWidgetItem(tenant.end_date if tenant.end_date else ''))
                        self.tenants_table.setItem(i, 6, QTableWidgetItem(tenant.email if tenant.email else ''))
                        self.tenants_table.setItem(i, 7, QTableWidgetItem(tenant.phone_number if tenant.phone_number else ''))
                        self.tenants_table.setItem(i, 8, QTableWidgetItem(str(tenant.amount_people)))
                else:
                    UniversalLogger.debug("No tenants data available", caller_class='TenantsTab')
        except Exception as e:
            UniversalLogger.debug(f"Error refreshing tenants: {e}", caller_class='TenantsTab')
