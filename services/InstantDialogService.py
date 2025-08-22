from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

from models.dialog_templates.dialog_agent import DialogAgent
from services.chapter_mission_data import get_chapter_data
from services.DialogService import DialogService


class InstantDialogService(DialogService):

    def generate_prompt_messages(self, from_dialog_agent: DialogAgent, from_dialog_agent_input: str, to_dialog_agent: DialogAgent, story_id: str, chapter: int):
        # Placeholder: fetch chapter description (replace with real lookup as needed)
        chapter_description = self.get_chapter_description(story_id, chapter)
        # Mission progress
        chapter_data = get_chapter_data(story_id, chapter)
        missions = chapter_data.get("missions", [])
        missions_done = sum(1 for m in missions if m.get("completed"))
        missions_total = len(missions)

        # Relationship and status context
        rel = to_dialog_agent.relationships.get(from_dialog_agent.dialog_agent_id, ("none", ""))
        rel_type, rel_note = rel if isinstance(rel, tuple) else (rel, "")
        status = to_dialog_agent.status if hasattr(to_dialog_agent, 'status') else 'unknown'

        # Simple tone analysis (demo: can be replaced with ML/NLP)
        def analyze_tone(text):
            text = text.lower()
            if any(word in text for word in ["please", "help", "thank", "grateful"]):
                return "polite"
            if any(word in text for word in ["now", "hurry", "quick", "urgent"]):
                return "urgent"
            if any(word in text for word in ["hate", "angry", "annoyed", "stupid"]):
                return "angry"
            if any(word in text for word in ["love", "friend", "happy", "joy"]):
                return "friendly"
            return "neutral"

        tone = analyze_tone(from_dialog_agent_input)

        system_prompt = (
            f"NPC: {to_dialog_agent.name}\n"
            f"Lore: {to_dialog_agent.lore}\n"
            f"Status: {status}\n"
            f"Relationship to {from_dialog_agent.name}: {rel_type}"
            + (f" ({rel_note})" if rel_note else "") + "\n"
            f"Story ID: {story_id}\n"
            f"Chapter: {chapter}\n"
            f"Chapter Description: {chapter_description}\n"
            f"Mission Progress: {missions_done} out of {missions_total} missions completed.\n"
            f"Incoming message tone: {tone}\n"
            f"Respond to the following as your character would in this chapter, considering your relationship, status, mission progress, and the tone of the message."
        )
        return ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(from_dialog_agent_input)
        ]).format_messages()

    def get_chapter_description(self, story_id: str, chapter: int) -> str:
        # TODO: Replace with real chapter description lookup (e.g., from DB or config)
        return f"This is a placeholder description for story {story_id}, chapter {chapter}."
