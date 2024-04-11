from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QDialog, QTreeWidgetItem
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon

from Text import Content2


class Application(object):
    def __init__(self, volume_instance, disk_name, tree_dir_instance):
        self.volume = volume_instance
        self.disk_name = disk_name
        self.directory_tree = self.volume.get_directory_tree()
        self.tree_dir = tree_dir_instance
        
                
    def setupUi(self, Dialog):
        Dialog.setObjectName("Application")
        Dialog.resize(652, 582)
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 631, 561))
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(parent=self.widget)
        self.label_2.setGeometry(QtCore.QRect(130, 0, 501, 571))
        self.label_2.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
                                   "font-weight: bold;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 141, 561))
        self.label.setStyleSheet("background-color: rgba(250, 128, 114, 1);\n"
        "\n"
        "border: 10px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(parent=self.widget)
        self.label_4.setGeometry(QtCore.QRect(40, 80, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font-weight: bold;")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.widget)
        self.label_5.setGeometry(QtCore.QRect(150, 20, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font-weight: bold;")
        self.label_5.setObjectName("label_5")
        self.treeWidget = QtWidgets.QTreeWidget(parent=self.widget)
        self.treeWidget.setGeometry(QtCore.QRect(5, 91, 131, 461))
        self.treeWidget.setStyleSheet("background-color: rgba(143, 188, 143, 1);\n"
                                      "font-weight: bold;")
        self.treeWidget.setObjectName("treeWidget")
        icon = QIcon("resources/disk_icon.jpg")
        self.treeWidget.headerItem().setIcon(0, icon)
        self.treeWidget.headerItem().setText(0, self.disk_name)
        self.label_3 = QtWidgets.QLabel(parent=self.widget)
        self.label_3.setGeometry(QtCore.QRect(500, 0, 131, 561))
        self.label_3.setStyleSheet("background-color: rgb(149, 128, 255);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(parent=self.widget)
        self.label_6.setGeometry(QtCore.QRect(0, 0, 631, 81))
        self.label_6.setStyleSheet("background-color: rgb(111, 154, 255)")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.widget)
        self.label_7.setGeometry(QtCore.QRect(180, 20, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "font-weight: bold;")
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton.setGeometry(QtCore.QRect(510, 150, 111, 41))
        self.pushButton.setStyleSheet("QPushButton#pushButton {\n"
        "    background-color: rgba(255, 255, 255, 255);\n"
        "    border-radius: 5px;\n"
        "    font-weight: bold;\n"
        "}\n"
        "\n"
        "QPushButton#pushButton:hover {\n"
        "    background-color: rgba(255, 107, 107, 255);\n"
        "    color: rgb(255, 255, 255);\n"
        "}\n"
        "\n"
        "QPushButton#pushButton:pressed {\n"
        "    background-color: rgba(255, 255, 255, 255);\n"
        "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/open_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 280, 111, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton#pushButton_2 {\n"
        "    background-color: rgba(255, 255, 255, 255);\n"
        "    border-radius: 5px;\n"
        "    font-weight: bold;\n"
        "}\n"
        "\n"
        "QPushButton#pushButton_2:hover {\n"
        "    background-color: rgba(255, 107, 107, 255);\n"
        "    color: rgb(255, 255, 255);\n"
        "}\n"
        "\n"
        "QPushButton#pushButton_2:pressed {\n"
        "    background-color: rgba(255, 255, 255, 255);\n"
        "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/delete_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(510, 390, 111, 91))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton#pushButton_3 {\n"
        "    background-color: rgba(255, 255, 255, 255);\n"
        "    border-radius: 5px;\n"
        "    font-weight: bold;\n"
        "}\n"
        "\n"
        "QPushButton#pushButton_3:hover {\n"
        "    background-color: rgba(11, 156, 49, 0.7);\n"
        "    color: rgb(255, 255, 255);\n"
        "}\n"
        "\n"
        "QPushButton#pushButton_3:pressed {\n"
        "    background-color: rgba(255, 255, 255, 255);\n"
        "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("resources/recycle_bin_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_8 = QtWidgets.QLabel(parent=self.widget)
        self.label_8.setGeometry(QtCore.QRect(230, 100, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(255, 106, 126);\n"
                                   "font-weight: bold;")
        self.label_8.setObjectName("label_8")
        
        self.label_9 = QtWidgets.QLabel(parent=self.widget)
        self.label_9.setGeometry(QtCore.QRect(160, 200, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_9.setStyleSheet("font-weight: bold;")
        self.label_10 = QtWidgets.QLabel(parent=self.widget)
        self.label_10.setGeometry(QtCore.QRect(160, 250, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("font-weight: bold;")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(parent=self.widget)
        self.label_11.setGeometry(QtCore.QRect(160, 310, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_11.setStyleSheet("font-weight: bold;")
        self.label_12 = QtWidgets.QLabel(parent=self.widget)
        self.label_12.setGeometry(QtCore.QRect(160, 370, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("font-weight: bold;")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(parent=self.widget)
        self.label_13.setGeometry(QtCore.QRect(160, 430, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("font-weight: bold;")
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(parent=self.widget)
        self.label_14.setGeometry(QtCore.QRect(230, 200, 251, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(parent=self.widget)
        self.label_15.setGeometry(QtCore.QRect(260, 250, 221, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(parent=self.widget)
        self.label_16.setGeometry(QtCore.QRect(290, 310, 191, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(parent=self.widget)
        self.label_17.setGeometry(QtCore.QRect(290, 370, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(parent=self.widget)
        self.label_18.setGeometry(QtCore.QRect(220, 430, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Myanmar Text")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        # Show content of text file 
        self.pushButton.clicked.connect(self.content_screen)
        
        # Execute delete function 
        self.pushButton_2.clicked.connect(self.delete_function)
        
    
    def get_content_file(self, file_name):
        self.content_file = file_name
    
        
    def content_screen(self):    
        if not self.volume.is_file(self.content_file):
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Invalid! Please select file.")
            return

        if not self.volume.is_txt_file(self.content_file):
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Invalid! Please select Text File.")
            return

        self.content = Content2(self.content_file, self.volume)
        self.content.show()

        
    def get_delete_object(self, path):
        self.delete_path = path
        
        
    def delete_function(self):
        # if not self.directory_tree.delete_node(self.delete_path) or not self.volume.delete_object(self.delete_path):
        if not self.volume.delete_object(self.delete_path):
            QtWidgets.QMessageBox.warning(self.widget, "Error", "Deleted failed!")
        else:
            # add this line
            self.directory_tree = self.volume.get_directory_tree()
            self.tree_dir.update_directory_tree(self.directory_tree)
            QMessageBox.information(self.widget, "Success", "Deleted successfully!")
            

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Application", "Application"))
        self.label_4.setText(_translate("Dialog", ""))
        self.label_5.setText(_translate("Dialog", "File System Manager"))
        self.label_7.setText(_translate("Dialog", "File System Manager"))
        self.pushButton.setText(_translate("Dialog", "Open TXT"))
        self.pushButton_2.setText(_translate("Dialog", "Delete File"))
        self.pushButton_3.setText(_translate("Dialog", "Recycle Bin"))
        self.label_8.setText(_translate("Dialog", "INFORMATION"))
        self.label_9.setText(_translate("Dialog", "Name :"))
        self.label_10.setText(_translate("Dialog", "Attributes :"))
        self.label_11.setText(_translate("Dialog", "Created Date :"))
        self.label_12.setText(_translate("Dialog", "Created Time :"))
        self.label_13.setText(_translate("Dialog", "Size :"))
        self.label_14.setText(_translate("Dialog", "Unknown"))
        self.label_15.setText(_translate("Dialog", "Unknown"))
        self.label_16.setText(_translate("Dialog", "Unknown"))
        self.label_17.setText(_translate("Dialog", "Unknown"))
        self.label_18.setText(_translate("Dialog", "Unknown"))