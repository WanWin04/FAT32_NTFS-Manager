import re
from NTFSTreeDirectory import TreeNode, DirectoryTree
from MFTEntry import MFTEntry
from Attribute import Attribute
        
class NTFS:
    def __init__(self, volume: str):
        self.volume = volume
        self.fd = open(r'\\.\%s' % self.volume, 'rb')
        
        # read VBR
        self.vbr = self.fd.read(512)
        self.bytes_per_sector = int.from_bytes(self.vbr[11:13], "little")
        self.sectors_per_cluster = int.from_bytes(self.vbr[13:14], "little")
        self.bytes_per_cluster = self.bytes_per_sector * self.sectors_per_cluster
        self.total_sectors = int.from_bytes(self.vbr[40:48], "little")
        self.mft_cluster = int.from_bytes(self.vbr[48:56], "little")
        self.mft_cluster_offset = self.mft_cluster * self.bytes_per_cluster
        self.mirr_mft_cluster = int.from_bytes(self.vbr[56:64], "little")
        self.bytes_per_mft_entry = 2**abs(int.from_bytes(self.vbr[64:65], 'little', signed=True))
        del self.vbr
        
        
        self.fd.seek(self.mft_cluster_offset)
        self.mft = []
        
        num_mft_entries = self.total_sectors - self.mft_cluster * self.sectors_per_cluster // 2
        # bug
        null_mft_entries = 0
        while num_mft_entries > 0:
            # tinh so entry null (luu data)
            if null_mft_entries > 10:
                break
            
            data = self.fd.read(self.bytes_per_mft_entry)
            
            mft_entry = MFTEntry(data)
            if mft_entry.signature == b"FILE":
                self.mft.append(mft_entry)
            else:
                null_mft_entries += 1
            num_mft_entries -= 1
            del mft_entry
        self.get_data_for_file()
        
                 
    def __del__(self):
        self.fd.close()
        
    def get_data_for_file(self):
        for mft_entry in self.mft:
            txt_file = False
            for attribute in mft_entry.attributes:
                # check file name include .txt
                if attribute.type == 0x30 and attribute.name.endswith(".txt"):
                    txt_file = True
                if attribute.type == 0x80 and attribute.non_resident == 1 and txt_file:
                    # read data     
                    i = 0
                    size_read= 0
                    other_size = attribute.real_size
                    while i < attribute.size.__len__() and attribute.cluster_count[i] > 0:
                        self.fd.seek(attribute.first_cluster[i] * self.bytes_per_cluster)
                        size_read = min(other_size, attribute.cluster_count[i] * self.bytes_per_cluster)
                        if size_read <= 0:
                            break
                        mft_entry.data += self.fd.read(size_read).decode("utf-8")
                        other_size -= size_read
                        i += 1
                    break
                if attribute.type == 0x80 and attribute.non_resident == 0 and txt_file:
                    mft_entry.data = attribute.data.decode("utf-8")
                    break
        return mft_entry.data
                    
    @staticmethod
    def is_NTFS_volume(volume: str) -> bool:
        with open(r'\\.\%s' % volume, 'rb') as file:
            boot_sector = file.read(512)
            return boot_sector[3:11] == b"NTFS    "
        
    # GET INFO FOR UI
    def get_directory_tree(self):
        self.tree = DirectoryTree()
        self.get_children(self.tree.root, 0)
        return self.tree
        
    def get_children(self, current_node, level):
        if level == 0:
            self.array = {mft_entry.record_number: 0 for mft_entry in self.mft}
        for mft_entry in self.mft:
            if  self.array[mft_entry.record_number] == 0 and mft_entry.record_number != 5 and (mft_entry.check_system_entry() == False) and mft_entry.get_parent_id() == current_node.id and mft_entry.get_name() != "." and mft_entry.get_name().__contains__("$") == False:
                self.array[mft_entry.record_number] = 1
                if mft_entry.is_directory():
                    node = TreeNode(mft_entry.get_name(), mft_entry.record_number)
                    current_node.children[mft_entry.get_name()] = node
                    self.get_children(node, level + 1)
                if mft_entry.is_file():
                    current_node.children[mft_entry.get_name()] = TreeNode(mft_entry.get_name(), mft_entry.record_number)
    
    def get_entry_by_path(self, path, a = 0):
        path_parts = path.split('/')
        # get root entry
        for mft_entry in self.mft:
            if mft_entry.get_name() == path_parts[0]:
                result = mft_entry
                path_parts.pop(0)
                break
        # add result that is children of entry
        # stop condition path_part empty 
        while len(path_parts) > 0:
            for mft_entry in self.mft:
                if mft_entry.get_parent_id() == result.record_number and mft_entry.get_name() == path_parts[0]:
                    result = mft_entry
                    path_parts.pop(0)
                    break
        return result
            
    def get_name(self, path):
        return self.get_entry_by_path(path).get_name()
    
    def get_attributes(self, path):
        return self.get_entry_by_path(path).get_attributes()
    def get_created_datetime(self, path):
        return self.get_entry_by_path(path).get_creation_time()

    def is_file(self, path):
        return self.get_entry_by_path(path).is_file()
    
    
    def get_file_size(self, path):
        return self.get_entry_by_path(path).get_real_size()
    def get_folder_size(self, path):
        directory = self.get_entry_by_path(path)
        size = self.get_size_folder(directory, 0)
        return size
    
    def get_size_folder(self, MFTEntry, size):
        for mft_entry in self.mft:
            if mft_entry.get_parent_id() == MFTEntry.record_number:
                if mft_entry.is_file():
                    size += mft_entry.get_real_size()
                if mft_entry.is_directory():
                    size = self.get_size_folder(mft_entry, size)
        return size
        
            
    def is_txt_file(self, path):
        return self.get_entry_by_path(path).get_name().endswith(".txt")
    
    def get_text_file(self, path):
        return self.get_entry_by_path(path).data
    
    # delete function
    def delete_object(self, path):
        entry = self.get_entry_by_path(path)
        entry.delete(self.get_id_recycle_bin())
        return True
            
    def get_id_recycle_bin(self):
        for mft_entry in self.mft:
            if mft_entry.get_name() == "$RECYCLE.BIN":
                return mft_entry.record_number
        return -1