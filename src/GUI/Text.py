from PyQt6 import QtCore, QtGui, QtWidgets


class Content2(QtWidgets.QMainWindow):
    def __init__(self, file_name, volume_instance):
        super().__init__()
        self.file_name = file_name
        self.volume = volume_instance
        self.setupUi(self)
        
        self.load_file_content()
        
        
    def setupUi(self, Content2):
        Content2.setObjectName("Content2")
        Content2.resize(842, 619)
        self.centralwidget = QtWidgets.QWidget(parent=Content2)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 822, 578))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        Content2.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=Content2)
        self.statusbar.setObjectName("statusbar")
        Content2.setStatusBar(self.statusbar)

        self.retranslateUi(Content2)
        QtCore.QMetaObject.connectSlotsByName(Content2)
        
        
    def load_file_content(self):
        file_content = self.volume.get_text_file(self.file_name)
        last_file_name = self.file_name.split('/')
        self.label.setText(file_content)
        self.setWindowTitle(last_file_name[-1])
        

    def retranslateUi(self, Content2):
        _translate = QtCore.QCoreApplication.translate
        Content2.setWindowTitle(_translate("Content2", "MainWindow"))
        self.label.setText(_translate("Content2", ""))

