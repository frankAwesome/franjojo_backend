from typing import List
from models.dialog_tree.dialog_tree import DialogTree
from models.dialog_tree.dialog_tree_node import DialogTreeNode

pig1_dialog_tree_nodes = List[DialogTreeNode] = [
    DialogTreeNode(1, 'Where is the straw house', 'The straw house is down by the river', False, 2)
    DialogTreeNode(2, '*', 'You destroyed my straw house, Ill never forgive you!', True, 2)
]

dialog_trees = List[DialogTree] = [
    DialogTree(1, 1, [1])
]