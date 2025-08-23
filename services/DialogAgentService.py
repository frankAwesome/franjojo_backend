from models.dialog_templates.dialog_agent import DialogAgent, DialogAgentType

DIALOG_AGENTS = [
    DialogAgent(
        dialog_agent_id=1,
        dialog_agent_type=DialogAgentType.USER,
        name='Big Bad Wolf',
        lore='Wants to eat the pigs.'
    ),
    DialogAgent(
        dialog_agent_id=2,
        dialog_agent_type=DialogAgentType.SYSTEM,
        name='Pig 1',
        lore='A lazy pig who just wants to lay about all day. '
    )
]


class DialogAgentService:
    # TODO: replace with values stored in DB
    def get_dialog_agent(self, dialog_agent_id):
        return next(x for x in DIALOG_AGENTS if x.dialog_agent_id == int(dialog_agent_id))
