class DialogAgentType:
    SYSTEM = 'system'
    USER = 'user'



class RelationshipType:
    NONE = 'none'
    FRIEND = 'friend'
    ENEMY = 'enemy'
    FAMILY = 'family'

class CharacterStatus:
    ALIVE = 'alive'
    DEAD = 'dead'

class DialogAgent:
    def __init__(self, dialog_agent_id, dialog_agent_type: DialogAgentType, name: str, lore: str, status=CharacterStatus.ALIVE, relationships=None):
        self.dialog_agent_id = dialog_agent_id
        self.dialog_agent_type = dialog_agent_type
        self.name = name
        self.lore = lore
        self.status = status
        # relationships: dict of {other_agent_id: (relationship_type, optional_note)}
        self.relationships = relationships or {}

