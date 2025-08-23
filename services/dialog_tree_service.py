from typing import List
from models.dialog_tree.dialog_tree import DialogTree
from models.dialog_tree.dialog_tree_node import DialogTreeNode

pig1_dialog_tree_nodes: List[DialogTreeNode] = [
    DialogTreeNode(1, 'Where is the straw house', 'The straw house is down by the river', True, 2),
    DialogTreeNode(2, '*', 'You destroyed my straw house, Ill never forgive you!', True, 2)
]

dialog_trees: List[DialogTree] = [
    DialogTree(1, 1, [1])
]


class DialogTreeService:

    def get_dialog_tree(self, project_id, dialog_tree_id):
        return next(x for x in dialog_trees if x.dialog_tree_id == int(dialog_tree_id))
    
    def get_dialog_tree_node(self, dialog_tree_node_id: int):
        return next(x for x in pig1_dialog_tree_nodes if x.dialog_tree_node_id == dialog_tree_node_id)
    
    def get_dialog_tree_nodes(self):
        return pig1_dialog_tree_nodes