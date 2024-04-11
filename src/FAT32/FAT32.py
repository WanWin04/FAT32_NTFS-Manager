import re
import datetime
import os
import errno
import subprocess

from RDET import RDET
from Entry import Entry
from DirectoryTree import TreeNode, DirectoryTree
from Attributes import Attributes


class FAT32:
    info = [
        "Bytes Per Sector",
        "Sectors Per Cluster",
        "Reserved Sectors", 
        "Number of Copies of FAT",
        "Number of Sectors Per FAT", 
        "Cluster Number of the Start of the Root Directory",
        "FAT Name",
    ]
    FAT_data = ""
    FAT_elements = []


    def __init__(self, name_of_volume):
        self.attributes = Attributes()
        self.name = name_of_volume
        self.fd = open(r'\\.\%s' % self.name, 'rb')
        self.boot_sector_raw = self.fd.read(0x200) # read 512 bytes
        
        with open('bootsector.dat', 'wb') as file:
            file.write(self.boot_sector_raw)
            
        self.boot_sector = {}
        self.__extract_boot_sector()
        self.SB = self.boot_sector["Reserved Sectors"]
        self.SF = self.boot_sector["Number of Sectors Per FAT"]
        self.NF = self.boot_sector["Number of Copies of FAT"]
        self.SC = self.boot_sector["Sectors Per Cluster"]
        self.BS = self.boot_sector["Bytes Per Sector"]
        
        # read sector for disk
        self.boot_sector_reserved_raw = self.fd.read(self.BS * (self.SB - 1))
        
        with open('bootsector2.dat', 'wb') as file:
            file.write(self.boot_sector_reserved_raw)
            
        self.get_FAT_data()

        start = self.boot_sector["Cluster Number of the Start of the Root Directory"]
        RDET_data = self.get_cluster_data_chain(start)
        self.RDET = RDET(RDET_data)
        
        with open('RDET.dat', 'wb') as file:
            file.write(RDET_data)
            
            
    def get_FAT_data(self):
        FAT_size = self.SF * self.BS # All sector of FAT (FAT1, FAT2)
        data = b""
        
        for _ in range(self.NF):
            data = self.fd.read(FAT_size)
            
        self.FAT_data = data
        
        for i in range(0, len(self.FAT_data), 4):
            self.FAT_elements.append(int.from_bytes(self.FAT_data[i : i + 4], byteorder='little'))


    def get_cluster_chain(self, index: int) -> 'list[int]':
        index_list = []
        while True:
            if index is None:
                break
            if index >= len(self.FAT_elements):
                break
            index_list.append(index)
            index = self.FAT_elements[index]
            if index == 0x0FFFFFFF or index == 0x0FFFFFF7:
                break
        return index_list


    def __extract_boot_sector(self):
        self.boot_sector["Bytes Per Sector"] = int.from_bytes(self.boot_sector_raw[0xB:0xD], byteorder='little') # 2 bytes (11 -> 13)
        self.boot_sector["Sectors Per Cluster"] = int.from_bytes(self.boot_sector_raw[0xD:0xE], byteorder='little')
        self.boot_sector["Reserved Sectors"] = int.from_bytes(self.boot_sector_raw[0xE:0x10], byteorder='little')
        self.boot_sector["Number of Copies of FAT"] = int.from_bytes(self.boot_sector_raw[0x10:0x11], byteorder='little')
        self.boot_sector["Number of Sectors Per FAT"] = int.from_bytes(self.boot_sector_raw[0x24:0x28], byteorder='little')
        self.boot_sector["Cluster Number of the Start of the Root Directory"] = int.from_bytes(self.boot_sector_raw[0x2C:0x30], byteorder='little')
        self.boot_sector["FAT Name"] = self.boot_sector_raw[0x52:0x5A].decode()


    def get_cluster_data_chain(self, cluster_index):
        # index_list containing the indices of consecutive clusters in the cluster chain, starting from cluster_index.
        index_list = self.get_cluster_chain(cluster_index)
        data = b""
        
        for i in index_list:
            # Calculate the offset of the cluster in the data region of the disk
            offset = self.SB + self.SF * self.NF + (i - 2) * self.SC
            
            # Seek to the beginning of the cluster in the disk file
            self.fd.seek(offset * self.BS)
            
            # Read the data of the cluster from the disk file and append it to the 'data' variable
            data += self.fd.read(self.SC * self.BS)

            
        with open('Data.dat', 'wb') as file:
            file.write(data)
            
        return data
    
    
    def get_RDET_for_cluster(self, cluster_index):
        start = cluster_index
        RDET_data = self.get_cluster_data_chain(start)
        
        return RDET(RDET_data)
    
    
    def get_directory_entries(self, cluster_index):
        rdet = self.get_RDET_for_cluster(cluster_index)
        return rdet.get_main_entries()
    
    
    def is_file(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return False
        return self.is_file_recursive(entry, path_parts[1:])
                
            
    def is_file_recursive(self, entry, path_parts):
        if not path_parts:
            return not (entry.attribute[0] & self.attributes.DIRECTORY)

        directory_entries = self.get_directory_entries(entry.start_cluster)
        for subentry in directory_entries:
            if subentry.name == path_parts[0]:
                if subentry.attribute[0] & self.attributes.DIRECTORY:
                    subcluster_index = subentry.start_cluster
                    if subcluster_index >= 2:
                        return self.is_file_recursive(subentry, path_parts[1:])
                else:
                    return not (subentry.attribute[0] & self.attributes.DIRECTORY)

        return False 
    
    
    @staticmethod
    def is_txt_file(file_name):
        file_extension = file_name.split('.')[-1].lower()
        return file_extension == 'txt'
    
    
    def get_name(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return None
        return self.get_name_recursive(entry, path_parts[1:])
            
        
    def get_name_recursive(self, entry, path_parts):
        if not path_parts:
            return entry.name

        directory_entries = self.get_directory_entries(entry.start_cluster)
        for subentry in directory_entries:
            if subentry.name == path_parts[0]:
                if subentry.attribute[0] & self.attributes.DIRECTORY:
                    subcluster_index = subentry.start_cluster
                    if subcluster_index >= 2:
                        return self.get_name_recursive(subentry, path_parts[1:])
                else:
                    return subentry.name

        return None   
    
    
    def get_attributes(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return None
        return self.get_attributes_recursive(entry, path_parts[1:])


    def get_attributes_recursive(self, entry, path_parts):
        if not path_parts:
            return self.parse_attributes(entry.attribute)

        if entry.attribute[0] & self.attributes.DIRECTORY:
            directory_entries = self.get_directory_entries(entry.start_cluster)
            for subentry in directory_entries:
                if subentry.name == path_parts[0]:
                    return self.get_attributes_recursive(subentry, path_parts[1:])

        return None
    
    
    def get_created_datetime(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return None
        return self.get_created_datetime_recursive(entry, path_parts[1:])
    
    
    def get_created_datetime_recursive(self, entry, path_parts):
        if not path_parts:
            return entry.create_time

        directory_entries = self.get_directory_entries(entry.start_cluster)
        for subentry in directory_entries:
            if subentry.name == path_parts[0]:
                if subentry.attribute[0] & self.attributes.DIRECTORY:
                    subcluster_index = subentry.start_cluster
                    if subcluster_index >= 2:
                        return self.get_created_datetime_recursive(subentry, path_parts[1:])
                else:
                    return subentry.create_time

        return None 
    
    
    def get_file_size(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return None
        return self.get_file_size_recursive(entry, path_parts[1:])
                
            
    def get_file_size_recursive(self, entry, path_parts):
        if not path_parts:
            return entry.size

        directory_entries = self.get_directory_entries(entry.start_cluster)
        for subentry in directory_entries:
            if subentry.name == path_parts[0]:
                if subentry.attribute[0] & self.attributes.DIRECTORY:
                    subcluster_index = subentry.start_cluster
                    if subcluster_index >= 2:
                        return self.get_file_size_recursive(subentry, path_parts[1:])
                else:
                    return subentry.size

        return None
        
    
    def get_folder_size(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return None
        return self.get_folder_size_recursive(entry, path_parts[1:])

    
    def get_folder_size_recursive(self, entry, path_parts):
        if not path_parts:
            return self.calculate_folder_size(entry)
        
        directory_entries = self.get_directory_entries(entry.start_cluster)
        for subentry in directory_entries:
            if subentry.name == path_parts[0]:
                if subentry.attribute[0] & self.attributes.DIRECTORY:
                    subcluster_index = subentry.start_cluster
                    if subcluster_index >= 2:
                        return self.get_folder_size_recursive(subentry, path_parts[1:])

        return None


    def calculate_folder_size(self, folder_entry):
        if not folder_entry.attribute[0] & self.attributes.DIRECTORY:
            return 0
        
        total_size = 0
        entries = self.get_directory_entries(folder_entry.start_cluster)
        
        for entry in entries:
            if entry.name not in ['.', '..']:
                if entry.attribute[0] & self.attributes.DIRECTORY:
                    subcluster_index = entry.start_cluster
                    if subcluster_index >= 2:
                        total_size += self.calculate_folder_size(entry)
                else:
                    total_size += entry.size
        
        return total_size


    def parse_attributes(self, attribute_byte):
        attributes = []
        attribute_int = int.from_bytes(attribute_byte, byteorder='little')
        if attribute_int & self.attributes.READ_ONLY:
            attributes.append(self.attributes.NAMES[self.attributes.READ_ONLY])
        if attribute_int & self.attributes.HIDDEN:
            attributes.append(self.attributes.NAMES[self.attributes.HIDDEN])
        if attribute_int & self.attributes.SYSTEM:
            attributes.append(self.attributes.NAMES[self.attributes.SYSTEM])
        if attribute_int & self.attributes.VOLUME_LABEL:
            attributes.append(self.attributes.NAMES[self.attributes.VOLUME_LABEL])
        if attribute_int & self.attributes.DIRECTORY:
            attributes.append(self.attributes.NAMES[self.attributes.DIRECTORY])
        if attribute_int & self.attributes.ARCHIVE:
            attributes.append(self.attributes.NAMES[self.attributes.ARCHIVE])

        return attributes
          
                    
    def get_text_file(self, path):
        path_parts = path.split('/')
        entry = self.RDET.find_entry_by_name(path_parts[0])
        if entry is None:
            return None
        return self.get_text_file_recursive(entry, path_parts[1:])


    def get_text_file_recursive(self, entry, path_parts):
        if not path_parts:
            if entry.attribute[0] & self.attributes.ARCHIVE:
                # Get cluster chain information
                cluster_chain = self.get_cluster_chain(entry.start_cluster)

                # Read the cluster chain
                file_content = b""
                for cluster_index in cluster_chain:
                    cluster_data = self.get_cluster_data_chain(cluster_index)
                    file_content += cluster_data

                # Decode content 
                file_content = file_content.decode('utf-8')
                return file_content
            else:
                return None

        if entry.attribute[0] & self.attributes.DIRECTORY:
            directory_entries = self.get_directory_entries(entry.start_cluster)
            for subentry in directory_entries:
                if subentry.name == path_parts[0]:
                    return self.get_text_file_recursive(subentry, path_parts[1:])

        return None
    

    def get_directory_tree(self):
        tree = DirectoryTree()
        root_cluster = self.boot_sector["Cluster Number of the Start of the Root Directory"]
        self._get_directory_tree_data_recursive(tree.root, "", root_cluster)
        return tree


    def _get_directory_tree_data_recursive(self, current_node, path, cluster_index):
        directory_entries = self.get_directory_entries(cluster_index)

        if directory_entries:
            for entry in directory_entries:
                if entry.name not in ['.', '..']:
                    if entry.attribute[0] & self.attributes.DIRECTORY:
                        subcluster_index = entry.start_cluster
                        if subcluster_index >= 2:
                            sub_path = path + "/" + entry.name
                            sub_node = TreeNode(entry.name)
                            current_node.children[entry.name] = sub_node
                            self._get_directory_tree_data_recursive(sub_node, sub_path, subcluster_index)
                    else:
                        current_node.children[entry.name] = TreeNode(entry.name)

    
    # ============================ DELETE ============================
    def delete_object(self, path):
        return True
