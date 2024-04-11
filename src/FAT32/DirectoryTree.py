import os


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = {}


class DirectoryTree:
    def __init__(self):
        self.root = TreeNode("root")

    
    def delete_node(self, path):
        path_parts = path.split('/')
        current_node = self.root
        
        for node in path_parts[:-1]:
            if node not in current_node.children:
                return False
            current_node = current_node.children[node]
            
        last_node = path_parts[-1]
        if last_node not in current_node.children:
            return False
        
        del current_node.children[last_node]
        return True

