from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

from models.dialog_templates.dialog_agent import DialogAgent
from services.DialogService import DialogService


class InstantDialogService(DialogService):

    def generate_prompt_messages(self, from_dialog_agent: DialogAgent, from_dialog_agent_input: str, to_dialog_agent: DialogAgent, story_id: str, chapter: int):
        # Placeholder: fetch chapter description (replace with real lookup as needed)
        chapter_description = self.get_chapter_description(story_id, chapter)
        system_prompt = (
            f"NPC: {to_dialog_agent.name}\n"
            f"Lore: {to_dialog_agent.lore}\n"
            f"Story ID: {story_id}\n"
            f"Chapter: {chapter}\n"
            f"Chapter Description: {chapter_description}\n"
            f"Respond to the following as your character would in this chapter."
        )
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(from_dialog_agent_input)
        ]).format_messages()

    def get_chapter_description(self, story_id: str, chapter: int) -> str:
        # TODO: Replace with real chapter description lookup (e.g., from DB or config)
        return f"This is a placeholder description for story {story_id}, chapter {chapter}."
