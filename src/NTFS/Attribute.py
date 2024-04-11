from datetime import datetime, timezone

class Attribute:
    def __init__(self, attributes: bytes):
        self.type = int.from_bytes(attributes[:4], "little")
        self.length = int.from_bytes(attributes[4:8], "little")
        self.non_resident = attributes[8] & 0x01 if len(attributes) > 8 else None
        if self.non_resident is None:
            return
        self.name_length = attributes[9]
        self.name_offset = int.from_bytes(attributes[10:12], "little")
        self.flags = int.from_bytes(attributes[12:14], "little")
        self.attribute_id = int.from_bytes(attributes[14:16], "little")
        
        if self.non_resident == 0:
            self.real_size = int.from_bytes(attributes[16:20], "little")
            self.offset_to_attribute = int.from_bytes(attributes[20:22], "little")
            self.content_resident(attributes[self.offset_to_attribute:self.offset_to_attribute + self.real_size])
        else:
            if self.type == 0x80:
                self.real_size = int.from_bytes(attributes[48:56], "little")
                self.data_runs_offset = int.from_bytes(attributes[32:34], "little")
                self.content_non_resident(attributes[self.data_runs_offset:self.length])
    
    def content_resident(self, attribute: bytes):
        if self.type == 0x10:
            self.resident_standard_information(attribute)
        elif self.type == 0x30:
            self.resident_file_name(attribute)
        elif self.type == 0x80:
            self.resident_data(attribute)
        else:
            pass
    
    def resident_standard_information(self, attribute: bytes):
        self.creation_time = self.parse_datetime(int.from_bytes(attribute[0:8], "little"))
        self.alteration_time = self.parse_datetime(int.from_bytes(attribute[8:16], "little"))
    
    def parse_datetime(self, timestamp: int):
        # Conversion to seconds and offset from 1601-01-01 to 1970-01-01
        timestamp_seconds = timestamp / 10_000_000 - 11_644_473_600
        return datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
   
    
    def resident_file_name(self, attribute: bytes):
        self.parent_id = int.from_bytes(attribute[0:6], "little")
        # handle file attributes
        self.file_attributes = []
        self.parse_file_attributes(int.from_bytes(attribute[56:60], "little"))
        
        self.file_name_length = attribute[64]
        self.name = attribute[66:66 + self.file_name_length * 2].decode("utf-16-le")
    
    def parse_file_attributes(self, file_attributes: bytes):
        # print bit-sequence of file_attributes
        # read-only bit 0
        if file_attributes & 0x01:
            self.file_attributes.append("Read-only")
        # hidden bit 1
        if file_attributes & 0x02:
            self.file_attributes.append("Hidden")
        # system bit 2
        if file_attributes & 0x04:
            self.file_attributes.append("System")
        # archive bit 5
        if file_attributes & 0x20:
            self.file_attributes.append("Archive")
        # directory bit 28
        if file_attributes & 0x10000000:
            self.file_attributes.append("Directory")
            
        
    def resident_data(self, attribute: bytes):
        self.data = attribute[:self.real_size]
    
    # handle non-resident attributes
    def content_non_resident(self, attribute: bytes):
        self.non_resident_data(attribute)
    
    
    # bug: case multiple data runs
    def non_resident_data(self, attribute: bytes):
        self.size = []
        self.cluster_count = []
        self.first_cluster = []
        
        while attribute:
            size = attribute[0:1].hex()
            if size == "00":
                break
            # get last 4 bits of size assign to cluster_count_size, convert to int
            cluster_count_size = int(attribute[0:1].hex()[1], 16)
            # get first 4 bits of size assign to size
            first_cluster_size = int.from_bytes(attribute[0:1], "little") >> 4
            cluster_count = int.from_bytes(attribute[1:1 + cluster_count_size], "little")
            first_cluster = int.from_bytes(attribute[1 + cluster_count_size: 1 + cluster_count_size + first_cluster_size], "little")
            self.size.append(size)
            self.cluster_count.append(cluster_count)
            self.first_cluster.append(first_cluster)
            attribute = attribute[1 + cluster_count_size + first_cluster_size:]
        
        # assign first_cluster[i + 1] += first_cluster[i], i starts from 1
        for i in range(1, len(self.first_cluster)):
            if self.cluster_count[i] == 0:
                break
            self.first_cluster[i] += self.first_cluster[i - 1]
            
    
            
        