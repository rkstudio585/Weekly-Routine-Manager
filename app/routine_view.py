from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QFileDialog, QToolTip, QLineEdit, QDialog, QFormLayout, QMessageBox
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
import os
import xml.etree.ElementTree as ET
import sqlite3

class RoutineView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weekly Routine")
        self.setWindowIcon(QIcon("assets/app_icon.png"))

        # Initialize theme
        self.is_dark_mode = False

        # Main layout
        self.main_layout = QVBoxLayout()

        # Top layout for buttons
        self.top_layout = QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(0)

        # Create Exit button
        self.exit_button = QPushButton("X")
        self.exit_button.setToolTip("Exit Application")
        self.exit_button.setStyleSheet("""
            background-color: #dc3545;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            min-width: 30px;
            min-height: 30px;
        """)
        self.exit_button.clicked.connect(self.close)

        # Create Toggle button
        self.toggle_button = QPushButton("M")
        self.toggle_button.setToolTip("Check Dark/White Mode")
        self.toggle_button.setStyleSheet("""
            background-color: #6c757d;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            min-width: 30px;
            min-height: 30px;
        """)
        self.toggle_button.clicked.connect(self.toggle_theme)

        # Add buttons to the top layout
        self.top_layout.addWidget(self.exit_button)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.toggle_button)

        # Add top layout to main layout
        self.main_layout.addLayout(self.top_layout)

        self.day_label = QLabel("Select a day to view the routine:")
        self.day_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.day_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.day_label)

        self.day_selector = QComboBox()
        self.day_selector.addItems(["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.main_layout.addWidget(self.day_selector)

        self.show_button = QPushButton("Show Routine")
        self.main_layout.addWidget(self.show_button)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Time", "Activity"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only

        # Set column widths
        self.table.setColumnWidth(0, 100)  # Width of Time column
        self.table.setColumnWidth(1, 300)  # Width of Activity column

        # Center align the header
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.table)

        # Create Export button
        self.export_button = QPushButton("Export")
        self.export_button.setToolTip("Export Routine to XML")

        # Create Import button
        self.import_button = QPushButton("Import")
        self.import_button.setToolTip("Import Routine from XML")

        # Create Add button
        self.add_button = QPushButton("Add New Routine")
        self.add_button.setToolTip("Add New Routine")

        # Create Delete button
        self.delete_button = QPushButton("Delete Routine")
        self.delete_button.setToolTip("Delete Routine Entry")

        # Create Edit button
        self.edit_button = QPushButton("Edit Routine")
        self.edit_button.setToolTip("Edit Routine Entry")

        self.main_layout.addWidget(self.export_button)
        self.main_layout.addWidget(self.import_button)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addWidget(self.edit_button)

        self.setLayout(self.main_layout)

        # Apply initial theme
        self.apply_theme()

        # Connect signals to slots
        self.export_button.clicked.connect(self.export_to_xml)
        self.import_button.clicked.connect(self.import_from_xml)
        self.add_button.clicked.connect(self.open_add_dialog)
        self.delete_button.clicked.connect(self.open_delete_dialog)
        self.edit_button.clicked.connect(self.open_edit_dialog)

    def update_routine(self, routine):
        self.table.setRowCount(len(routine))
        
        for row, (time, activity) in enumerate(routine):
            time_item = QTableWidgetItem(time)
            activity_item = QTableWidgetItem(activity)
            time_item.setTextAlignment(Qt.AlignCenter)
            activity_item.setTextAlignment(Qt.AlignCenter)

            # Insert items into table
            self.table.setItem(row, 0, time_item)  # Time in the left column
            self.table.setItem(row, 1, activity_item)  # Activity in the right column

        # Adjust column width to fit content
        self.table.resizeColumnsToContents()

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            # Dark mode styles
            self.setStyleSheet("background-color: #333333; color: #f0f0f0;")
            self.day_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #f0f0f0;")
            self.table.setStyleSheet("""
                background-color: #444444; 
                color: #f0f0f0;
                selection-background-color: #555555;
                selection-color: #f0f0f0;
            """)
            self.table.horizontalHeader().setStyleSheet("""
                background-color: #555555; 
                color: #f0f0f0;
            """)
            self.show_button.setStyleSheet("""
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.export_button.setStyleSheet("""
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.import_button.setStyleSheet("""
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.add_button.setStyleSheet("""
                background-color: #17a2b8;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.delete_button.setStyleSheet("""
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.edit_button.setStyleSheet("""
                background-color: #ffc107;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.toggle_button.setStyleSheet("""
                background-color: #6c757d;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
                min-width: 30px;
                min-height: 30px;
            """)
            self.toggle_button.setText("M")
        else:
            # Light mode styles
            self.setStyleSheet("background-color: #f0f0f0; color: #333333;")
            self.day_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333333;")
            self.table.setStyleSheet("""
                background-color: white; 
                color: #333333;
                selection-background-color: #e9ecef;
                selection-color: #333333;
            """)
            self.table.horizontalHeader().setStyleSheet("""
                background-color: #007bff; 
                color: white;
            """)
            self.show_button.setStyleSheet("""
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.export_button.setStyleSheet("""
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.import_button.setStyleSheet("""
                background-color: #007bff;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.add_button.setStyleSheet("""
                background-color: #17a2b8;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.delete_button.setStyleSheet("""
                background-color: #dc3545;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.edit_button.setStyleSheet("""
                background-color: #ffc107;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
            """)
            self.toggle_button.setStyleSheet("""
                background-color: #6c757d;
                color: white;
                font-weight: bold;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
                min-width: 30px;
                min-height: 30px;
            """)
            self.toggle_button.setText("M")

    def export_to_xml(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", f"{os.path.expanduser('~/Documents')}/routine.xml", "XML Files (*.xml)")
        
        if not file_path:
            return
        
        root = ET.Element("Routine")
        day_elem = ET.SubElement(root, "Day")
        
        for row in range(self.table.rowCount()):
            time = self.table.item(row, 0).text()
            activity = self.table.item(row, 1).text()
            
            entry_elem = ET.SubElement(day_elem, "Entry")
            time_elem = ET.SubElement(entry_elem, "Time")
            time_elem.text = time
            activity_elem = ET.SubElement(entry_elem, "Activity")
            activity_elem.text = activity
        
        tree = ET.ElementTree(root)
        tree.write(file_path)

    def import_from_xml(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", f"{os.path.expanduser('~/Documents')}", "XML Files (*.xml)")
        
        if not file_path:
            return
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Clear existing data
        self.table.setRowCount(0)
        
        day_elem = root.find("Day")
        if day_elem is None:
            return
        
        for entry in day_elem.findall("Entry"):
            time = entry.find("Time").text
            activity = entry.find("Activity").text
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(time))
            self.table.setItem(row_position, 1, QTableWidgetItem(activity))
        
        # Adjust column width to fit content
        self.table.resizeColumnsToContents()

    def open_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Routine")
        dialog.setFixedSize(300, 150)
        
        layout = QFormLayout()
        
        self.time_input = QLineEdit()
        self.activity_input = QLineEdit()
        
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        layout.addRow("Time:", self.time_input)
        layout.addRow("Activity:", self.activity_input)
        layout.addRow(ok_button, cancel_button)
        
        ok_button.clicked.connect(self.add_new_routine)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def add_new_routine(self):
        time = self.time_input.text()
        activity = self.activity_input.text()
        
        if not time or not activity:
            return
        
        selected_day = self.day_selector.currentText()
        
        # Add data to table
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(time))
        self.table.setItem(row_position, 1, QTableWidgetItem(activity))
        
        # Add data to database
        conn = sqlite3.connect("routine.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO routine (day, time, activity) VALUES (?, ?, ?)", (selected_day, time, activity))
        conn.commit()
        conn.close()

    def open_delete_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Routine")
        dialog.setFixedSize(300, 150)
        
        layout = QFormLayout()
        
        self.delete_index_input = QLineEdit()
        self.delete_index_input.setPlaceholderText("Enter row number to delete")
        
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        layout.addRow("Row Number:", self.delete_index_input)
        layout.addRow(ok_button, cancel_button)
        
        ok_button.clicked.connect(self.delete_routine)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def delete_routine(self):
        try:
            row = int(self.delete_index_input.text()) - 1  # Convert to 0-based index
            if row < 0 or row >= self.table.rowCount():
                raise ValueError("Invalid row number")
            
            time = self.table.item(row, 0).text()
            activity = self.table.item(row, 1).text()
            
            selected_day = self.day_selector.currentText()
            
            # Remove from table
            self.table.removeRow(row)
            
            # Remove from database
            conn = sqlite3.connect("routine.db")
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM routine WHERE day=? AND time=? AND activity=?", (selected_day, time, activity))
            conn.commit()
            conn.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid row number. Please enter a valid number.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    def open_edit_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Routine")
        dialog.setFixedSize(300, 200)
        
        layout = QFormLayout()
        
        self.edit_row_input = QLineEdit()
        self.edit_time_input = QLineEdit()
        self.edit_activity_input = QLineEdit()
        
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        
        layout.addRow("Row Number:", self.edit_row_input)
        layout.addRow("New Time:", self.edit_time_input)
        layout.addRow("New Activity:", self.edit_activity_input)
        layout.addRow(ok_button, cancel_button)
        
        ok_button.clicked.connect(self.edit_routine)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def edit_routine(self):
        try:
            row = int(self.edit_row_input.text()) - 1  # Convert to 0-based index
            new_time = self.edit_time_input.text()
            new_activity = self.edit_activity_input.text()
            
            if row < 0 or row >= self.table.rowCount() or not new_time or not new_activity:
                raise ValueError("Invalid input")
            
            old_time = self.table.item(row, 0).text()
            old_activity = self.table.item(row, 1).text()
            
            # Update table
            self.table.setItem(row, 0, QTableWidgetItem(new_time))
            self.table.setItem(row, 1, QTableWidgetItem(new_activity))
            
            # Update database
            selected_day = self.day_selector.currentText()
            conn = sqlite3.connect("routine.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE routine
                SET time=?, activity=?
                WHERE day=? AND time=? AND activity=?
            """, (new_time, new_activity, selected_day, old_time, old_activity))
            conn.commit()
            conn.close()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid input. Please enter valid values.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
