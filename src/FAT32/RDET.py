from Entry import Entry


class RDET:
    def __init__(self, data: bytes) -> None:
        self.RDET_data: bytes = data
        self.entries = []
        long_name = ""
        
        for i in range(0, len(data), 32):
            single_entry = self.RDET_data[i: i + 32]
            self.entries.append(Entry(single_entry))
            
            if self.entries[-1].empty or self.entries[-1].deleted:
                long_name = ""
                continue
            if not self.entries[-1].subentry:
                if long_name != "":
                    self.entries[-1].name = long_name
                else:
                    extend = self.entries[-1].ext.strip().decode()
                    if extend == "":
                        self.entries[-1].name = self.entries[-1].name.strip().decode()
                    else:
                        self.entries[-1].name = self.entries[-1].name.strip().decode() + "." + extend
                long_name = ""
            else:
                long_name = self.entries[-1].name + long_name


    def get_main_entries(self):
        return [entry for entry in self.entries if entry.is_main_entry()]


    def find_entry_by_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        
        name_lower = name.lower()
        for entry in self.entries:
            if entry.is_main_entry() and entry.name.lower() == name_lower:
                return entry
        return None
    
