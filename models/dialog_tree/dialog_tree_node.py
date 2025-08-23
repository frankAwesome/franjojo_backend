from typing import Optional


class DialogTreeNode:
    def __init__(self, dialog_tree_node_id, match_dialog, respond_dialog, generate_response, next_dialog_tree_node_id):
        self.dialog_tree_node_id: int = dialog_tree_node_id
        self.match_dialog: str = match_dialog
        self.respond_dialog: str = respond_dialog
        self.generate_response: bool = generate_response
        self.next_dialog_tree_node_id: int = next_dialog_tree_node_id

        self.generated_response: Optional[str] = None