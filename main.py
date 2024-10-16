from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys


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



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())