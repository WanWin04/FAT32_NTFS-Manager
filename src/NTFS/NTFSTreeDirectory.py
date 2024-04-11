class TreeNode:
    def __init__(self, name, id_entry):
        self.name = name
        self.id = id_entry
        self.children = {}

class DirectoryTree:
    def __init__(self):
        self.root = TreeNode("root", 5)

        