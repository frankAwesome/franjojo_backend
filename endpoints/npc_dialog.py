
from fastapi import APIRouter, HTTPException
from models.http.npc_dialog import GetNPCDialogRequest, GetGameStoryParamsResponse, NPCInfo, ChapterInfo, Milestone, GameStoryModel
from typing import List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

router = APIRouter()

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

@router.post("/v1/getNPCDialog")
def get_npc_dialog(request: GetNPCDialogRequest):
    # Example: log dialog to Firestore
    doc_ref = db.collection("npc_dialogs").document()
    data = request.dict()
    data["timestamp"] = datetime.utcnow().isoformat()
    doc_ref.set(data)
    # For demo, just echo back
    return {"npcResponse": f"NPC ({request.npcId}) heard: {request.dialogText}", "timestamp": data["timestamp"]}

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
