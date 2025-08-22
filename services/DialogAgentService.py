from models.dialog_templates.dialog_agent import DialogAgent, DialogAgentType, RelationshipType, CharacterStatus

DIALOG_AGENTS = [
    DialogAgent(
        dialog_agent_id=1,
        dialog_agent_type=DialogAgentType.USER,
        name='John',
        lore='The player. A protagonist adventurer.',
        status=CharacterStatus.ALIVE,
        relationships={
            2: (RelationshipType.FRIEND, 'Helped Bobby in the past'),
            3: (RelationshipType.ENEMY, 'Rival since childhood')
        }
    ),
    DialogAgent(
        dialog_agent_id=2,
        dialog_agent_type=DialogAgentType.SYSTEM,
        name='Bobby',
        lore='A poor fisherman in the town of Floodville.',
        status=CharacterStatus.ALIVE,
        relationships={
            1: (RelationshipType.FRIEND, 'Grateful to John'),
            3: (RelationshipType.FAMILY, 'Cousin')
        }
    ),
    DialogAgent(
        dialog_agent_id=3,
        dialog_agent_type=DialogAgentType.SYSTEM,
        name='Mara',
        lore='A mysterious traveler with a dark past.',
        status=CharacterStatus.DEAD,
        relationships={
            1: (RelationshipType.ENEMY, 'Blames John for her fate'),
            2: (RelationshipType.FAMILY, 'Cousin')
        }
    )
]


class DialogAgentService:
    # TODO: replace with values stored in DB
    def get_dialog_agent(self, dialog_agent_id):
        return next(x for x in DIALOG_AGENTS if x.dialog_agent_id == int(dialog_agent_id))
