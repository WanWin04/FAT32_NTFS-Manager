from itertools import chain
from datetime import datetime


class Entry:
    def __init__(self, data):
        self.subentry = self.deleted = self.empty = self.label = False
        self.size = 0
        self.ext = b""
        self.name = ""
        self.entry_data = data
        self.attribute = data[11:12] # offset 0B
        
        # sub entry 
        if self.attribute == b'\x0F':
            self.subentry = True
            
        # main entry 
        if not self.subentry: 
            self.name = self.entry_data[:8] # 8 bytes for main name
            self.ext = self.entry_data[8:11] # 3 bytes (8 -> 10) for extended name
            status = self.name[:1] 
            
            if status == b'\xE5':
                self.deleted = True
            elif status == b'\x00':
                self.empty = True
                self.name = ""
                return
                
            if self.attribute == b"\x08":
                self.label = True
                return
            
            self.start_cluster = int.from_bytes(self.entry_data[26:28][::-1], byteorder='big') # 2 bytes (26 -> 27)
            self.size = int.from_bytes(self.entry_data[28:32], byteorder='little') # 4 bytes (28 -> 31)
            
            # datetime
            self.create_time = self.get_create_time(self.entry_data)
                        
        # sub entry
        else:
            self.index = self.entry_data[0]
            self.name = b""
            
            for i in chain(range(1, 11), range(14, 26), range(28, 32)):
                self.name += int.to_bytes(self.entry_data[i], 1, byteorder='little')
                
                if self.name.endswith(b"\xFF\xFF"):
                    self.name = self.name[:-2]
                    break
                
            self.name = self.name.decode('utf-16le').strip('\x00')


    def get_create_time(self, data):
        self.time_created_raw = int.from_bytes(data[0xD:0x10], byteorder='little') # 3 bytes
        self.date_created_raw = int.from_bytes(data[0x10:0x12], byteorder='little') # 2 bytes
        
        self.datetime_created = self.extract_datetime(self.time_created_raw, self.date_created_raw)
        
        return self.datetime_created
        
    
    def extract_datetime(self, time_created_raw, date_created_raw):
        if time_created_raw is None:
            return None
        
        hours = (time_created_raw & 0b111110000000000000000000) >> 19 # get bit 19 -> bit 23, shift right 19 bits
        minutes = (time_created_raw & 0b000001111110000000000000) >> 13  # get bit 13 -> bit 18, shift right 13 bits
        seconds = (time_created_raw & 0b000000000001111110000000) >> 7 # get bit 7 -> bit 12, shift right 7 bits
        
        year = ((date_created_raw & 0b1111111000000000) >> 9) + 1980
        month = (date_created_raw & 0b0000000111100000) >> 5
        day = date_created_raw & 0b0000000000011111
        
        if date_created_raw is None:
            return datetime(year, month, day)
        return datetime(year, month, day, hours, minutes, seconds)
    

    def is_main_entry(self):
        if self.empty or self.subentry or self.deleted or self.label or (self.attribute == b"\x16"):
            return False
        return True
