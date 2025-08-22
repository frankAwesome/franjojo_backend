from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

from models.dialog_templates.dialog_agent import DialogAgent
from services.DialogService import DialogService


class InstantDialogService(DialogService):

    def generate_prompt_messages(self, from_dialog_agent: DialogAgent, from_dialog_agent_input: str, to_dialog_agent: DialogAgent):
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(to_dialog_agent.lore + "\nRespond to the following"),
            HumanMessagePromptTemplate.from_template(from_dialog_agent_input)
        ]).format_messages()
