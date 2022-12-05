from printree import printree

class BTSNode():
    def __init__(self, key, info=None, left=None, right=None, parent = None) -> None:
        self.key = key
        self.info = info
        self.left = left
        self.right = right
        self.parent = parent


    def to_str(self) -> str:
        return (f"Node {id(self)}:\n" +
                f"key = {self.key} ; info = {self.info}\n" +
                f"left = {None if (self.left is None) else self.left.key} ; right = {None if (self.right is None) else self.right.key} ; parent = {None if (self.parent is None) else self.parent.key}")
        
        
    def __repr__(self) -> str:
        return str(self.key)
    
        
class BST():
    def __init__(self) -> None:
        self.root = None
        
        
    def insert(self, key, info=None):
        temp = BTSNode(key, info)
        parent_node = self.tree_position(key)
        if parent_node is None:
            self.root = temp
        else:
            temp.parent = parent_node
            if parent_node.key > key:
                parent_node.left = temp
            else:
                parent_node.right = temp
        return temp
        
        
    def __repr__(self): #no need to understand the implementation of this one
        out = ""
        for row in printree(self.root): #need printree.py file
            out = out + row + "\n"
        return out
    
    
    def height(self, target_node=None):
        if target_node is None:
            target_node = self.root
        return self._height_rec(target_node)
 
    def _height_rec(self, current_node):
        if current_node == None:
            return -1
        return max(self._height_rec(current_node.right), self._height_rec(current_node.left)) + 1


    def depth(self, target_node=None):
        if target_node is None:
            target_node = self.root
        return self._depth_rec(target_node)
    
    def _depth_rec(self, current_node):
        if current_node is self.root:
            return 0
        return self._depth_rec(current_node.parent) + 1


    def tree_search(self, k):
        return self._tree_search_rec(self.root, k)
    
    def _tree_search_rec(self, current_node, k):
        if  current_node is None or current_node.key == k:
            return current_node
        elif current_node.key > k:
            return self._tree_search_rec(current_node.left, k)
        else:
            return self._tree_search_rec(current_node.right, k)
        

    def tree_position(self, k):
        if self.root is None:
            return None
        return self._tree_position_rec(self.root, k)
  
    def _tree_position_rec(self, current_node, k):
        if current_node.key == k:
            raise AttributeError(f"Key {k} already exists.")
        elif current_node.key > k:
            if current_node.left is None:
                return current_node
            return self._tree_position_rec(current_node.left, k)
        else:
            if current_node.right is None:
                return current_node
            return self._tree_position_rec(current_node.right, k)
        
    
    def sorted_walk_func(self, func):
        self._sorted_walk_func_rec(self.root, func)
        
    def _sorted_walk_func_rec(self, current_node, func):
        if current_node is not None:
            self._sorted_walk_func_rec(current_node.left, func)
            func(current_node)
            self._sorted_walk_func_rec(current_node.right, func)
            
            
    def min(self, target_root=None):
        if target_root is None:
            target_root = self.root
        return self._min_rec(target_root)
           
    def _min_rec(self, current_node):
        if current_node.left is None:
            return current_node
        return self._min_rec(current_node.left)
    
    
    def max(self, target_root=None):
        if target_root is None:
            target_root = self.root
        return self._max_rec(target_root)

    def _max_rec(self, current_node):
        if current_node.right is None:
            return current_node
        return self._max_rec(current_node.right)
            
       
    def successor(self, current_node):
        return  self._successor_rec(current_node)     
    # if return None than max
    def _successor_rec(self, current_node):
        if current_node.right is None:
            temp = current_node
            while temp.parent is not None:
                if temp.parent.left is temp:
                    return temp.parent
                temp = temp.parent
            return None
        else:
            return self.min(current_node.right)
        
        
    def predecessor(self, current_node):
        return  self._predecessor_rec(current_node)     
    # if return None than min
    def _predecessor_rec(self, current_node):
        if current_node.left is None:
            temp = current_node
            while temp.parent is not None:
                if temp.parent.right is temp:
                    return temp.parent
                temp = temp.parent
            return None
        else:
            return self.max(current_node.left)
        
        
    # Edge case: when removing root with only one son, we delete the root and the son becomes root, not the successor 
    def delete(self, current_node):
        is_root = False
        if self.root is current_node:
            is_root = True
        if current_node.left is None and current_node.right is None:
            if is_root:
                self.root = None
            else:
                if current_node.parent.left is current_node:
                    current_node.parent.left = None
                else:
                    current_node.parent.right = None
        elif current_node.left is not None and current_node.right is not None:
            succ = self.successor(current_node)
            self.delete(succ)
            succ.parent = None if is_root else current_node.parent
            succ.left = current_node.left
            if current_node.left is not None:
                current_node.left.parent = succ
            succ.right = current_node.right
            if current_node.right is not None:
                current_node.right.parent = succ
            if is_root:
                self.root = succ
            else:
                if current_node.parent.left is current_node:
                    current_node.parent.left = succ
                else:
                    current_node.parent.right = succ
        else:
            only_node = current_node.right if current_node.left is None else current_node.left
            only_node.parent = None if (current_node.parent is None) else current_node.parent
            if is_root:
                self.root = only_node
            else:
                if current_node.parent.left is current_node:
                    current_node.parent.left = only_node
                else:
                    current_node.parent.right = only_node
        return current_node
                
    
    def print_inorder_non_rec(self):
        if self.root is not None:
            stack = []
            temp = self.root
            stack.append(temp)
            while (len(stack) > 0):
                if temp.left is not None:
                    stack.append(temp.left)
                    temp = temp.left
                else:
                    target = stack.pop()
                    print(target.key)
                    if target.right is not None:
                        stack.append(target.right)
                        temp = target.right
                        
                        
    def is_bst(self):
        return self.is_bst_rec(self.root, None, None)

    
    def is_bst_rec(self, node, min_key, max_key):
        if node is None:
            return True
        if min_key is not None:
            if node.key < min_key:
                return False
        if max_key is not None:
            if node.key > max_key:
                return False
        return self.is_bst_rec(node.left, min_key, node.key) and self.is_bst_rec(node.right, node.key, max_key)
            