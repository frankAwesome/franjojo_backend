class DialogAgentType:
    SYSTEM = 'system'
    USER = 'user'


class DialogAgent:
    def __init__(self, dialog_agent_id, dialog_agent_type: DialogAgentType, name: str, lore: str, personality: str = ''):
        self.dialog_agent_id = dialog_agent_id
        self.dialog_agent_type = dialog_agent_type
        self.name = name
        self.lore = lore
        self.personality = personality

