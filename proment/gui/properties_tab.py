from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton

class PropertiesTab(QWidget):
    def __init__(self, data_container, parent=None):
        super().__init__(parent)
        self.data_container = data_container
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
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
        refresh_btn.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_btn)

    def refresh_data(self):
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
