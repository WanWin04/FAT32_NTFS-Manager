from Attribute import Attribute
class MFTEntry:
    def __init__(self, mft_entry: bytes):
        self.signature = mft_entry[:4]
        if self.signature != b"FILE":
            return
        self.update_sequence_offset = int.from_bytes(mft_entry[4:6], "little")
        self.update_sequence_number = int.from_bytes(mft_entry[6:8], "little")
        self.logfile_sequence_number = int.from_bytes(mft_entry[8:16], "little")
        self.sequence_number = int.from_bytes(mft_entry[16:18], "little")
        self.hardlink_count = int.from_bytes(mft_entry[18:20], "little")
        self.offset_to_first_attribute = int.from_bytes(mft_entry[20:22], "little")
        
        self.flags_temp = int.from_bytes(mft_entry[22:24], "little")
        self.parse_flags()
        
        self.used_size = int.from_bytes(mft_entry[24:28], "little")
        self.allocated_size = int.from_bytes(mft_entry[28:32], "little")
        self.file_reference = int.from_bytes(mft_entry[32:40], "little")
        self.next_attribute_id = int.from_bytes(mft_entry[40:42], "little")
        self.record_number = int.from_bytes(mft_entry[44:48], "little")
        
        attributes = mft_entry[self.offset_to_first_attribute:]
        self.attributes = []
        while attributes:
            attribute = Attribute(attributes)
            if attribute.type == 0xffffffff:
                break
            self.attributes.append(attribute)
            attributes = attributes[attribute.length:]
        self.data = ""

    def parse_flags(self):
        if self.flags_temp & 0x01:
            self.flags = "In Use"
        else:
            self.flags = "Not In Use"
        if self.flags_temp & 0x02:
            self.flags += ", Directory"
        else:
            self.flags += ", File"
    
    def is_directory(self):
        return self.flags == "In Use, Directory"
    
    def is_file(self):
        return self.flags == "In Use, File"
    
    def add_child_entry(self, entry):
        self.child_entries.append(entry)
        
    def get_name(self):
        for attribute in self.attributes:
            if attribute.type == 0x30:
                return attribute.name
        return "Unknown"
    def get_attributes(self):
        for attribute in self.attributes:
            if attribute.type == 0x30:
                return attribute.file_attributes 
        return "Unknown"
    def get_creation_time(self):
        for attribute in self.attributes:
            if attribute.type == 0x10:
                return attribute.creation_time
        return "Unknown"
    def get_alteration_time(self):
        for attribute in self.attributes:
            if attribute.type == 0x10:
                return attribute.alteration_time
        return "Unknown"
    def get_parent_id(self):
        for attribute in self.attributes:
            if attribute.type == 0x30:
                return attribute.parent_id
        return "Unknown"
    
    def is_file(self):
        return self.flags == "In Use, File"
    
    def is_directory(self):
        return self.flags == "In Use, Directory"
    
    def get_real_size(self):
        if self.is_file():
            for attribute in self.attributes:
                if attribute.type == 0x80:
                    return attribute.real_size
        return "Unknown"
    
    def delete(self, recycle_bin_id):
        # change bytes in flags_temp to "Not In Use"
        self.flags_temp &= 0xfe
        self.parse_flags()
        # update parent id to recycle bin id
        if recycle_bin_id != -1:
            for attribute in self.attributes:
                if attribute.type == 0x30:
                    attribute.parent_id = recycle_bin_id
        
    def check_system_entry(self):
        system_sign = 'System'
        for attribute in self.get_attributes():
            if system_sign in attribute:
                return True
        return False
    