from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QLineEdit, \
    QPushButton, QComboBox, QToolBox, QToolBar, QStatusBar, QGridLayout, QLabel, QMessageBox
import sys
import sqlite3

from pyexpat.errors import messages


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Add favicon
        self.setWindowIcon(QIcon("icons/Kantech_favicon.png"))

        # Set the window title and size
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # Set Menubar
        file_menu_item = self.menuBar().addMenu("File")
        help_menu_item = self.menuBar().addMenu("Help")
        edit_student_item = self.menuBar().addMenu("Edit")

        # Set Menubar Actions
        student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        student_action.triggered.connect(self.insert)
        file_menu_item.addAction(student_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu_item.addAction(about_action)

        search_student_action = QAction(QIcon("icons/search.png"), "Search Student", self)
        search_student_action.triggered.connect(self.search)
        edit_student_item.addAction(search_student_action)

        #Create a Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create Tool Bar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(student_action)
        toolbar.addAction(search_student_action)

        # Create Status Bar and add status bar elements
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)

        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    # Add Student from database
    def load_data(self):
        # Clear the table
        self.table.setRowCount(0)

        # Create a connection
        connection = sqlite3.connect("student_database.db")
        result = connection.execute("SELECT * FROM students")
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()

        # Dialog box Title
        self.setWindowTitle("About")

        content = """
        he program is a Student Management System built using PyQt6 and SQLite3. It provides a graphical user interface 
        (GUI) for managing student records, including adding, editing, searching, and deleting student information. 
        The main window features a menu bar, toolbar, and a table to display student data. Dialogs are used for various 
        operations like inserting, updating, and searching student records. The program connects to an SQLite database 
        to store and retrieve student information, ensuring data persistence.
        """

        self.setText(content)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog box Title
        self.setWindowTitle("Update Student Data")

        grid = QGridLayout()

        delete_message = QLabel("Are you sure you want to delete this student record?")
        yes = QPushButton("Yes")
        no = QPushButton("No")


        grid.addWidget(delete_message, 0, 0, 1, 2)
        grid.addWidget(yes, 1, 0)
        grid.addWidget(no, 1, 1)

        self.setLayout(grid)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.reject)

    def delete_student(self):
        row_index = window.table.currentRow()
        student_id = window.table.item(row_index, 0).text()
        connection =sqlite3.connect("student_database.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()

        self.close()

        message = QMessageBox()
        message.setWindowTitle("Success")
        message.setText("Student Record Deleted")
        message.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog box Title
        self.setWindowTitle("Update Student Data")

        # Dimensions of dialog box
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Index of row
        row_index = window.table.currentRow()

        # Add student Line Edit
        name = window.table.item(row_index, 1).text()
        self.student_name = QLineEdit(name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Course Line Edit
        course_name = window.table.item(row_index, 2).text()
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("Course")
        self.course_name.addItems(["Biology", "Math", "Physics", "Astrology", "Chemistry"])
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add Mobile
        mobile = window.table.item(row_index, 3).text()
        self.mobile_number = QLineEdit(mobile)
        self.mobile_number.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_number)

        # Add "Add Student" Button
        add_student_button = QPushButton("Update")
        add_student_button.clicked.connect(self.update_student_data)
        layout.addWidget(add_student_button)

        self.setLayout(layout)

    def update_student_data(self):
        # Student id
        student_id = window.table.item(window.table.currentRow(), 0).text()

        # Connect to database
        connection = sqlite3.connect("student_database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(), self.course_name.currentText(), self.mobile_number.text(),
                        student_id))
        connection.commit()
        cursor.close()
        window.load_data()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog box Title
        self.setWindowTitle("Insert Student Data")

        # Dimensions of dialog box
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student Line Edit
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Course Line Edit
        self.course_name = QComboBox()
        self.course_name.setPlaceholderText("Course")
        self.course_name.addItems(["Biology", "Math", "Physics", "Astrology", "Chemistry"])
        layout.addWidget(self.course_name)

        # Add Mobile
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile_number)

        # Add "Add Student" Button
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student)
        layout.addWidget(add_student_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile_number.text()
        connection = sqlite3.connect("student_database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Dialog box Title
        self.setWindowTitle("Search Student")

        # Dimensions of dialog box
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add student name line
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout)
    def search(self):
        window.load_data()

        name = self.student_name.text()
        connection = sqlite3.connect("student_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        items =  window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()



# Create the application instance and start application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
window.load_data()
sys.exit(app.exec())