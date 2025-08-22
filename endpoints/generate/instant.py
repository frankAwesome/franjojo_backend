from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter
from common.verify_token import verify_token
from models.http.GenerateInstantRequest import GenerateInstantRequest
from models.http.GenerateInstantResponse import GenerateInstantResponse
from services.DialogAgentService import DialogAgentService
from services.InstantDialogService import InstantDialogService
from services.LLMService import LLMService
from services.chapter_mission_data import get_chapter_data, are_all_missions_complete, get_mission_status, set_mission_complete

router = APIRouter()
dialog_agent_service = DialogAgentService()
instant_dialog_service = InstantDialogService()
llm_service = LLMService()





@router.get("/generate/instant")
async def get_instant_dialog_response(params: Annotated[GenerateInstantRequest, Depends()], user_data=Depends(verify_token)):
    from_dialog_agent = dialog_agent_service.get_dialog_agent(params.fromId)
    to_dialog_agent = dialog_agent_service.get_dialog_agent(params.toId)

    chapter_data = get_chapter_data(params.story_id, params.chapter)
    missions = chapter_data["missions"]

    # Example: dialog options based on mission status
    if params.action == "mission_status":
        status_lines = [f"Mission: {m['description']} - {'Done' if m['completed'] else 'Not done'}" for m in missions]
        return GenerateInstantResponse(response="\n".join(status_lines))
    elif params.action == "complete_mission":
        # expects params.fromInput to be mission_id
        if set_mission_complete(params.story_id, params.chapter, params.fromInput):
            return GenerateInstantResponse(response=f"Mission '{params.fromInput}' marked as complete.")
        else:
            return GenerateInstantResponse(response=f"Mission '{params.fromInput}' not found.")
    elif params.action == "story_progressed":
        if all(not m['completed'] for m in missions):
            return GenerateInstantResponse(response="You haven't started any missions in this chapter yet. Try exploring or talking to NPCs to begin your adventure!")
        if not are_all_missions_complete(params.story_id, params.chapter):
            # Not all missions done, dialog is blocked
            incomplete = [m['description'] for m in missions if not m['completed']]
            return GenerateInstantResponse(response=f"You must complete these missions first: {', '.join(incomplete)}")
        # All missions done, allow story dialog to progress
        messages = instant_dialog_service.generate_prompt_messages(
            from_dialog_agent=from_dialog_agent,
            from_dialog_agent_input=params.fromInput,
            to_dialog_agent=to_dialog_agent,
            story_id=params.story_id,
            chapter=params.chapter
        )
        response = llm_service.send_prompt(messages)
        return GenerateInstantResponse(response=response.content)
    elif params.action == "idle":
        return GenerateInstantResponse(response="The NPC is idling and does not respond.")
    elif params.action == "annoyed":
        return GenerateInstantResponse(response="The NPC looks annoyed and ignores you.")
    elif params.action == "chapter_info":
        chapter_description = chapter_data["description"]
        return GenerateInstantResponse(response=f"Chapter Info: {chapter_description}")
    else:
        return GenerateInstantResponse(response="The NPC does not have a response for this action.")
