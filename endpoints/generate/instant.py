from typing import Annotated

from fastapi import Depends
from fastapi import APIRouter
from common.verify_token import verify_token
from models.http.GenerateInstantRequest import GenerateInstantRequest
from models.http.GenerateInstantResponse import GenerateInstantResponse
from services.DialogAgentService import DialogAgentService
from services.InstantDialogService import InstantDialogService
from services.LLMService import LLMService

router = APIRouter()
dialog_agent_service = DialogAgentService()
instant_dialog_service = InstantDialogService()
llm_service = LLMService()


@router.get("/generate/instant")
async def get_instant_dialog_response(params: Annotated[GenerateInstantRequest, Depends()], user_data=Depends(verify_token)):

    # Load the relevant Dialog Agents (e.g. npc) to get their lore and personality
    from_dialog_agent = dialog_agent_service.get_dialog_agent(params.fromId)
    to_dialog_agent = dialog_agent_service.get_dialog_agent(params.toId)

    # Generate langchain prompt based off all info gathered
    messages = instant_dialog_service.generate_prompt_messages(
        from_dialog_agent=from_dialog_agent,
        from_dialog_agent_input=params.fromInput,
        to_dialog_agent=to_dialog_agent
    )

    # Get generated llm response
    response = llm_service.send_prompt(messages)

    return GenerateInstantResponse(response=response.content)
