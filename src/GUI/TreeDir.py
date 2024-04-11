import sys
from PyQt6.QtWidgets import QApplication, QDialog, QTreeWidgetItem
from PyQt6 import QtCore, QtGui, QtWidgets

sys.path.append("../FAT32")
from FAT32 import FAT32
sys.path.append("../NTFS")
from NTFS import NTFS
from Application import Application
import datetime


class TreeDir:
    def __init__(self, volume_instance, disk_name):
        self.dialog = QDialog()
        self.ui = Application(volume_instance, disk_name, self)
        self.ui.setupUi(self.dialog)
        
        self.volume = volume_instance

        directory_tree = self.volume.get_directory_tree()
        
        self.update_directory_tree(directory_tree)
        
        self.ui.treeWidget.itemClicked.connect(self.onItemClicked)
        

    def onItemClicked(self, item):
        self.ui.get_content_file(self.getParentPath(item))
        self.ui.get_delete_object(self.getParentPath(item))
                
        full_long_name = self.volume.get_name(self.getParentPath(item))
        attributes = self.volume.get_attributes(self.getParentPath(item))
        attributes_str = ", ".join(attributes)
        created_datetime = self.volume.get_created_datetime(self.getParentPath(item))
        
        if self.volume.is_file(self.getParentPath(item)):
            file_size = self.volume.get_file_size(self.getParentPath(item))
            
            self.ui.label_18.setText(str(file_size) + " bytes")
        else:
            folder_size = self.volume.get_folder_size(self.getParentPath(item))
            
            self.ui.label_18.setText(str(folder_size) + " bytes")
        
        self.ui.label_14.setText(full_long_name)
        self.ui.label_15.setText(attributes_str)
        self.ui.label_16.setText(created_datetime.strftime("%d-%m-%Y"))
        self.ui.label_17.setText(created_datetime.strftime("%H:%M:%S"))        
            

    def getParentPath(self, item):
        def getParent(item, outstring):
            if item.parent() is None:
                return outstring
            outstring = item.parent().text(0) + "/" + outstring
            return getParent(item.parent(), outstring)

        output = getParent(item, item.text(0))
        return output


    def update_directory_tree(self, directory_tree):
        self.ui.treeWidget.clear()
        
        root_node = directory_tree.root
        
        for child_node in root_node.children.values():
            self.add_items(None, child_node)
    

    def add_items(self, parent_item, current_node):
        if parent_item is None:
            item = QTreeWidgetItem([current_node.name])
            self.ui.treeWidget.addTopLevelItem(item)
        else:
            item = QTreeWidgetItem([current_node.name])
            parent_item.addChild(item)
        
        for child_node in current_node.children.values():
            self.add_items(item, child_node)


    def show(self):
        self.dialog.show()
        
        
    def get_disk_name(self, disk_name):
        self.disk_name = disk_name
