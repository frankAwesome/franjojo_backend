from models.dialog_templates.dialog_agent import DialogAgent, DialogAgentType

DIALOG_AGENTS = [
    DialogAgent(
        dialog_agent_id=1,
        dialog_agent_type=DialogAgentType.USER,
        name='John',
        lore='The player. A protagonist adventurer.'
    ),
    DialogAgent(
        dialog_agent_id=2,
        dialog_agent_type=DialogAgentType.SYSTEM,
        name='Bobby',
        lore='A poor fisherman in the town of Floodville.'
    )
]


class DialogAgentService:
    # TODO: replace with values stored in DB
    def get_dialog_agent(self, dialog_agent_id):
        return next(x for x in DIALOG_AGENTS if x.dialog_agent_id == int(dialog_agent_id))
