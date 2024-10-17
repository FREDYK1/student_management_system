from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Student Management System")

        # Set Menubar
        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")

        # Set Menubar Actions
        student_action = QAction("Add Student", self)
        file_menu_item.addAction(student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        #Create a Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    # Add Student from database
    def load_data(self):
        # Create a connection
        connection = sqlite3.connect("student_database.db")
        result = connection.execute("SELECT * FROM students")
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()


# Create the application instance and start application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())