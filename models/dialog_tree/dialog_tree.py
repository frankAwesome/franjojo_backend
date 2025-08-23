from typing import List


class DialogTree:
    def __init__(self, dialog_tree_id, starting_dialog_tree_id, current_available_dialog_tree_ids):
        self.dialog_tree_id: int = dialog_tree_id
        self.starting_dialog_tree_id: int = starting_dialog_tree_id
        self.current_available_dialog_tree_ids: List[int] = current_available_dialog_tree_ids
