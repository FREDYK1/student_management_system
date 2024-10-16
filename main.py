from PyQt6.QtWidgets import QApplication, QMainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.setWindowTitle("Student Management System")





app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())