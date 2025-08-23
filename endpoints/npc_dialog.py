
from fastapi import APIRouter, Depends, HTTPException
from common.verify_token import verify_token
from models.http.create_dialog_request import CreateDialogRequest
from models.http.npc_dialog import GetNPCDialogRequest, GetGameStoryParamsResponse, NPCInfo, ChapterInfo, Milestone, GameStoryModel
from typing import List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import logging
from services.chat_history_service import ChatHistoryService
from services.vector_db_service import VectorDBService

from services.dialog_chain_service import DialogChainService, DialogChainState

dialog_chain_service = DialogChainService()
chat_history_service = ChatHistoryService()

router = APIRouter()
logger = logging.getLogger("franjojo_backend")
active_vector_dbs: List[VectorDBService] = []

@router.post("/v1/addGameStory")
def add_game_story(story: GameStoryModel):
    """
    Expects a JSON body matching GameStoryModel (no 'response' field).
    """
    story_dict = story.dict()
    # Ensure all characters have an image field (for backward compatibility)
    for character in story_dict.get("characters", []):
        if "image" not in character:
            character["image"] = ""
    story_id = story_dict.get("storyId")
    if not story_id:
        raise HTTPException(status_code=400, detail="Missing storyId in request body.")
    doc_ref = db.collection("game_stories").document(story_id)
    story_dict["timestamp"] = datetime.utcnow().isoformat()
    doc_ref.set(story_dict)
    return {"message": f"Story '{story_id}' added/updated.", "timestamp": story_dict["timestamp"]}

# Ensure Firebase is initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

@router.get("/v1/getGameStorieParams/{storyName}")
def get_game_story_params(storyName: str):
    # Fetch story parameters from Firestore
    doc_ref = db.collection("game_stories").document(storyName)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"Story '{storyName}' not found.")
    response = doc.to_dict()
    # Ensure all characters have an image field
    if "characters" in response:
        for character in response["characters"]:
            if "image" not in character:
                character["image"] = ""
    return GetGameStoryParamsResponse(
        endpoint=f"v1/getGameStorieParams/{storyName}",
        method="GET",
        response=response,
        timestamp=datetime.utcnow()
    )

@router.get("/v1/getAllStories")
def get_all_stories():
    stories = []
    for doc in db.collection("game_stories").stream():
        story = doc.to_dict()
        # Ensure all characters have an image field
        if "characters" in story:
            for character in story["characters"]:
                if "image" not in character:
                    character["image"] = ""
        stories.append(story)
    return {"stories": stories, "count": len(stories)}

@router.post("/v1/getDialog/{storyId}/{npcId}")
def create_dialog(storyId: int, npcId: int, body: CreateDialogRequest, user_data=Depends(verify_token)):

    instance_id = user_data['user_id'] + "/" + str(storyId)

    story = __feth_story(str(storyId))

    lore = story['lore']
    relevant_npc = next(x for x in story['characters'] if x['id'] == npcId)

    vector_db_service = ___get_vector_db_service(instance_id)

    npc_dialog_state = __get_dialog_state(lore, relevant_npc)
    retriever = vector_db_service.get_retriever()

    chat_history = chat_history_service.get_chat_history(instance_id)

    resp = dialog_chain_service.create_prompt(body.playerQuestion, npc_dialog_state, chat_history, [], retriever)

    chat_history_service.save_chat(instance_id, body.playerQuestion, resp.content, relevant_npc['name'])
    
    return {'response': {
        "dialogResponse": resp.content
    }}

def __feth_story(storyId: str):
    doc_ref = db.collection("game_stories").document(storyId)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"Story '{storyId}' not found.")
    
    response = doc.to_dict()
    return response

def __get_dialog_state(lore: str, npc):
    return DialogChainState(
        lore=lore,
        name=npc['name'],
        background=npc['description']
    )

def ___get_vector_db_service(instance_id):
    
    vector_db_service = next((x for x in active_vector_dbs if x.instance_id == instance_id), None)

    if not vector_db_service:
        vector_db_service = VectorDBService(instance_id)
        active_vector_dbs.append(vector_db_service)
    
    return vector_db_service

