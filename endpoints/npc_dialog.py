
import asyncio
from fastapi import APIRouter, Depends, HTTPException, Query
import numpy as np
from common.verify_token import verify_token
from models.http.chapter_milestone import ChapterMilestone
from models.http.create_dialog_request import CreateDialogRequest
from models.http.create_story_context_documents_req import StoryContextDocumentReq
from models.http.npc_dialog import GetNPCDialogRequest, GetGameStoryParamsResponse, NPCInfo, ChapterInfo, Milestone, GameStoryModel
from typing import List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import logging
from services.chat_history_service import ChatHistoryService
from services.firestore_db_service import FirestoreDbService
from services.vector_db_service import VectorDBService
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

from services.dialog_chain_service import DialogChainService, DialogChainState
embeddings = OpenAIEmbeddings()

dialog_chain_service = DialogChainService()
chat_history_service = ChatHistoryService()
firestore_db_service = FirestoreDbService()

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
    doc_ref = db.collection("game_stories").document(str(story_id))
    story_dict["timestamp"] = datetime.utcnow().isoformat()
    doc_ref.set(story_dict)
    return {"message": f"Story '{story_id}' added/updated.", "timestamp": story_dict["timestamp"]}

# Ensure Firebase is initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()


@router.get("/v1/getGameStorieParams/{storyId}")
def get_game_story_params(storyId: int):
    # Fetch story parameters from Firestore by storyId
    doc_ref = db.collection("game_stories").document(str(storyId))
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"Story with id '{storyId}' not found.")
    response = doc.to_dict()
    # Ensure all characters have an image field
    if "characters" in response:
        for character in response["characters"]:
            if "image" not in character:
                character["image"] = ""
    return GetGameStoryParamsResponse(
        endpoint=f"v1/getGameStorieParams/{storyId}",
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

@router.get("/v1/storyContexts/{storyId}")
def get_story_context(storyId: str, user_data=Depends(verify_token)):
    instance_id = user_data['user_id'] + "/" + str(storyId)
    vector_db_service = ___get_vector_db_service(instance_id)

    return { 
        "documents": vector_db_service.get_all_documents()
    }

@router.post("/v1/storyContexts/{storyId}")
def create_story_context_document(storyId: int, body: StoryContextDocumentReq, user_data=Depends(verify_token)):
    instance_id = user_data['user_id'] + "/" + str(storyId)
    vector_db_service = ___get_vector_db_service(instance_id)

    result = vector_db_service.add_documents(body.documents)

    return { 
        "documents": result
    }

@router.delete("/v1/storyContexts/{storyId}/{documentId}")
def delete_story_context_document(storyId: str, documentId: str, rebase: bool = Query(False, description="Whether to rebase the index after deletion"), user_data=Depends(verify_token)):
    instance_id = user_data['user_id'] + "/" + str(storyId)
    vector_db_service = ___get_vector_db_service(instance_id)

    vector_db_service.remove_document(documentId, rebase)

    return { }

@router.post("/v1/getDialog/{storyId}/{npcId}")
async def create_dialog(storyId: int, npcId: int, body: CreateDialogRequest, user_data=Depends(verify_token)):

    logger.info(f"[/v1/getDialog/{storyId}/{npcId}] Started")

    resp, matched_milestone = await asyncio.gather(get_dialog_response(storyId, npcId, body, user_data), get_milestone_matching(body))
    
    return {'response': {
        "dialogResponse": resp.content,
        "matchedMilestone": matched_milestone.milestoneId if matched_milestone else None
    }}

async def get_milestone_matching(body):
    return __match_dialog_option(body.playerQuestion, [milestone for milestone in body.milestones if not milestone.completed])

async def get_dialog_response(storyId: int, npcId: int, body: CreateDialogRequest, user_data):
    instance_id = user_data['user_id'] + "/" + str(storyId)

    story = await firestore_db_service.get_game_story_by_story_id(str(storyId))

    lore = story['lore']
    chapters = story['chapters']

    active_chapter = next(c for c in chapters if c['id'] == body.activeChapterId)
    completed_chapters = [c for c in chapters if c['id'] in body.completedChapterIds]

    additional_context = ''
    
    for c in completed_chapters:
        additional_context += c['description'] + ', '
    
    additional_context += active_chapter['description']

    relevant_npc = next(x for x in story['characters'] if x['id'] == npcId)

    vector_db_service = ___get_vector_db_service(instance_id)

    npc_dialog_state = __get_dialog_state(lore, relevant_npc)
    retriever = vector_db_service.get_retriever()

    chat_history = chat_history_service.get_chat_history(instance_id)

    resp = await dialog_chain_service.create_prompt(body.playerQuestion, npc_dialog_state, chat_history, additional_context, retriever)

    chat_history_service.save_chat(instance_id, body.playerQuestion, resp.content, relevant_npc['name'])

    return resp

    logger.info(f"Fetching storyId {storyId}")

    doc_ref = db.collection("game_stories").document(storyId)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"Story '{storyId}' not found.")
    
    response = doc.to_dict()

    logger.info(f"Done fetching storyId {storyId}")
    return response

def __get_dialog_state(lore: str, npc):
    return DialogChainState(
        lore=lore,
        name=npc['name'],
        background=npc['description']
    )

def ___get_vector_db_service(instance_id):

    logger.info(f"[{instance_id}] Fetching vector DB service")
    
    vector_db_service = next((x for x in active_vector_dbs if x.instance_id == instance_id), None)

    if not vector_db_service:
        vector_db_service = VectorDBService(instance_id)
        active_vector_dbs.append(vector_db_service)

    logger.info(f"[{instance_id}] Done fetching vector DB service")
    
    return vector_db_service

def __match_dialog_option(input: str, options: list[ChapterMilestone], threshold: float = 0.85):
    logger.info("Starting dialog match")

    if not options:
        return None

    input_vec = embeddings.embed_query(input)

    best_match = None
    best_score = -1.0

    # loop through milestones
    for opt in options:
        # collect all possible match strings (name + matches)
        candidate_texts = [opt.name] + getattr(opt, "matches", [])

        # embed each
        option_vecs = [embeddings.embed_query(txt) for txt in candidate_texts]

        # compute similarity scores against input
        sims = cosine_similarity([input_vec], option_vecs)[0]

        # get best score for this milestone
        local_best = float(np.max(sims))
        if local_best > best_score:
            best_score = local_best
            best_match = opt

    logger.info(f"Done dialog match (best_score={best_score:.2f})")

    if best_score >= threshold:
        return best_match
    return None