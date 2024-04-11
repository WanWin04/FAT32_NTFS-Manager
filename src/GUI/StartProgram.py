from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import os

from TreeDir import TreeDir
sys.path.append("../FAT32")
from FAT32 import FAT32
sys.path.append("../NTFS")
from NTFS import NTFS

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Start")
        Form.resize(653, 544)
        self.widget = QtWidgets.QWidget(parent=Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 621, 511))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setGeometry(QtCore.QRect(330, 40, 271, 411))
        self.label.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
        "border-radius: 10px;\n"
        "font-weight: bold;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 341, 441))
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 98, 112, 255), stop:1 rgba(255, 107, 107, 255));\n"
        "border-radius: 10px;\n"
        "font-weight: bold;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        # self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        # self.lineEdit.setGeometry(QtCore.QRect(380, 130, 201, 41))
        # font = QtGui.QFont()
        # font.setPointSize(9)
        # font.setBold(True)
        # font.setItalic(False)
        # font.setWeight(75)
        # self.lineEdit.setFont(font)
        # self.lineEdit.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
        # "border: 2px solid rgba(0, 0, 0, 0);\n"
        # "border-bottom-color: rgba(46, 82, 101, 200);\n"
        # "color: rgb(0, 0, 0);\n"
        # "padding-bottom: 7px;\n"
        # "font-weight: bold;")
        # self.lineEdit.setText("")
        # self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(380, 220, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
        "border: 2px solid rgba(0, 0, 0, 0);\n"
        "border-bottom-color: rgba(46, 82, 101, 200);\n"
        "color: rgb(0, 0, 0);\n"
        "padding-bottom: 7px;\n"
        "font-weight: bold;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setGeometry(QtCore.QRect(380, 340, 211, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton#pushButton {\n"
        "    background-color: rgba(85, 98, 112, 255);\n"
        "    color: rgba(255, 255, 255, 200);\n"
        "    border-radius: 5px;\n"
        "    font-weight: bold;"
        "}\n"
        "\n"
        "QPushButton#pushButton:hover {\n"
        "    padding-left: 5px;\n"
        "    padding-top: 5px;\n"
        "    background-color: rgba(255, 107, 107, 255);\n"
        "    background-position: calc(100% - 10px)center;\n"
        "}\n"
        "\n"
        "QPushButton#pushButton:pressed {\n"
        "   background-color: rgba(255, 107, 107, 255);\n"
        "}")
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setGeometry(QtCore.QRect(50, 80, 291, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgba(255, 255, 255, 255);\n"
                                   "font-weight: bold;"
        "")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.widget)
        self.label_4.setGeometry(QtCore.QRect(90, 310, 71, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgba(255, 255, 255, 255);\n"
                                   "font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.widget)
        self.label_5.setGeometry(QtCore.QRect(240, 310, 71, 61))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgba(255, 255, 255, 255);\n"
                                   "font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setGeometry(QtCore.QRect(380, 60, 211, 41))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # Change to Application frame 
        self.pushButton.clicked.connect(self.app_screen)
        
    
    def app_screen(self):
        # type_file_system = self.lineEdit.text().strip()
        # if type_file_system.upper() not in ["FAT32", "NTFS"]:
        #     QtWidgets.QMessageBox.warning(self.widget, "Error", "Invalid file system! Please enter 'FAT32' or 'NTFS'.")
        #     return
        
        disk_name = self.lineEdit_2.text().strip()
        if not os.path.exists(disk_name):
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Invalid disk path! Please enter a valid disk name.")
            return
        else:
            with open(r'\\.\%s' % disk_name, 'rb') as file:
                boot_sector = file.read(512)
                # Check if the disk is FAT32 or NTFS
                if boot_sector[3:11] == b'NTFS    ':
                        volume = NTFS(disk_name)
                if boot_sector[0x52:0x5A] == b'FAT32   ':
                    volume = FAT32(disk_name)
                
            
        # Open Application screen 
        self.tree_dir = TreeDir(volume, disk_name)
        self.tree_dir.show()
        
        # Close start program screen 
        self.widget.window().close()
    

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Start", "Start"))
        # self.lineEdit.setPlaceholderText(_translate("Form", "Enter the file system type"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Enter name of the disk"))
        self.pushButton.setText(_translate("Form", "Enter"))
        self.label_3.setText(_translate("Form", "File System Manager"))
        self.label_4.setText(_translate("Form", "FAT32"))
        self.label_5.setText(_translate("Form", "NTFS"))
        self.label_6.setText(_translate("Form", "Information"))

