from igraph import Graph
from plot import plot_tree

class Tree():
  '''
    Parameters:
    - If current Tree is a leaf node or not
    - Value of current node
    - Left child of current node
    - Right child of current node
    - Number of nodes from the current node to leaf nodes following the child nodes
  '''
  def __init__(self, value, is_leaf, size=1, left=None, right=None):
    self.is_leaf = is_leaf
    self.value = value
    self.left = left
    self.right = right
    self.size = size

  # Retrieve edges structure to plot  
  def get_structure(self, id):
    parsed_value = self.value if self.is_leaf else self.value.__str__
    res = {
      "value": parsed_value,
      "edges": []
    }
    if not self.is_leaf:  
      right_id = id + self.left.size + 1
      res["edges"] = [(id,id+1),(id,right_id)]
      return [res] + self.left.get_structure(id + 1) + self.right.get_structure(right_id)
    else:
      return [res]

  def get_sub_tree(self, current_idx, current_level, desired_idx):
    if current_idx == desired_idx:
      return (current_level,self)
    if not self.is_leaf:
      right_id = current_idx + 1 + self.left.size
      return self.left.get_sub_tree(current_idx+1,current_level+1, desired_idx) or self.right.get_sub_tree(right_id,current_level+1,desired_idx)
  def get_sub_trees_by_level(self, current_level, current_idx,  available_deepness, max_allowed_deepness):
    if (max_allowed_deepness - current_level) <= available_deepness or (self.size // 2) <=  available_deepness:
      if self.is_leaf:
        return [(current_idx, self)]
      right_id = current_idx + 1 + self.left.size
      return [(current_idx, self)] + self.left.get_sub_trees_by_level(current_level+1,current_idx+1,available_deepness,max_allowed_deepness) + self.right.get_sub_trees_by_level(current_level+1,right_id,available_deepness,max_allowed_deepness)
    
    if not self.is_leaf:
      right_id = current_idx + 1 + self.left.size
      return self.left.get_sub_trees_by_level(current_level+1,current_idx+1,available_deepness,max_allowed_deepness) + self.right.get_sub_trees_by_level(current_level+1,right_id,available_deepness,max_allowed_deepness)
    return []
  def update_sub_tree(self, current_idx, idx_to_be_replaced, replacement_tree):
    if not self.is_leaf:
      right_idx = current_idx + self.left.size + 1
      if current_idx + 1 == idx_to_be_replaced:
        self.left = replacement_tree
      elif right_idx == idx_to_be_replaced:
        self.right = replacement_tree
      else:
        self.left.update_sub_tree(current_idx + 1,idx_to_be_replaced,replacement_tree)
        self.right.update_sub_tree(right_idx,idx_to_be_replaced,replacement_tree)
      self.size = self.left.size + self.right.size + 1
  def print(self):
    data = self.get_structure(0)
    labels = []
    edges = []
    for x in data:
      labels.append(x["value"])
      edges += x["edges"]
    g = Graph()
    g.add_vertices(self.size)
    g.add_edges(edges)
    plot_tree(g, self.size, labels)
  def copy(self):
    return deepcopy(self)

  def eval_in_order(self):
    if not self.is_leaf:
      res = self.left.eval_in_order()
      res += self.value.__str__
      res += self.right.eval_in_order()
      return res
    return str(self.value)
  
  def eval_post_order(self):
    if not self.is_leaf:
      res_l = self.left.eval_post_order()
      res_r = self.right.eval_post_order()
      res = f"{self.value.__name__}({res_l}, {res_r})"      
      return res
    return str(self.value)
