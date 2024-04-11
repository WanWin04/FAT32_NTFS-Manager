from PyQt6.QtWidgets import QApplication, QDialog, QTreeWidgetItem
import xml.etree.ElementTree as ET
import sys

from StartProgram import Ui_Form

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)


if __name__ == "__main__":
    system = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(system.exec())
