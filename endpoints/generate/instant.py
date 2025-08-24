import json
from typing import Annotated, List

from fastapi import Depends
from fastapi import APIRouter
from common.verify_token import verify_token
from models.dialog_tree.dialog_tree import DialogTree
from models.dialog_tree.dialog_tree_node import DialogTreeNode
from models.http.GenerateInstantRequest import GenerateInstantRequest
from models.http.GenerateInstantResponse import GenerateInstantResponse
from models.http.post_generate_dialog_tree import GenerateDialogTree
from services.DialogAgentService import DialogAgentService
from services.InstantDialogService import InstantDialogService
from services.LLMService import LLMService
from langchain_openai import OpenAIEmbeddings
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from services.chat_history_service import ChatHistoryService
from services.dialog_chain_service import DialogChainService, DialogChainState
from services.dialog_tree_service import DialogTreeService
from services.project_service import ProjectService
from langchain.vectorstores import FAISS

import logging
logger = logging.getLogger("franjojo_backend")

from services.vector_db_service import VectorDBService

router = APIRouter()
dialog_agent_service = DialogAgentService()
instant_dialog_service = InstantDialogService()
llm_service = LLMService()
embeddings = OpenAIEmbeddings()
dialog_tree_service = DialogTreeService()
dialog_chain_service = DialogChainService()
project_service = ProjectService()
chat_history_service = ChatHistoryService()
# vector_db_service = VectorDBService()

npc_conversations = { }
active_vector_dbs: List[VectorDBService] = []

embeddings = OpenAIEmbeddings()
docs = [
    "The big bad wolf has been spotted nearby."
]
# Create FAISS index
vectorstore = FAISS.from_texts(docs, embeddings)
# Later you can save/load
vectorstore.save_local("world_index")


@router.get("/generate/instant")
async def get_instant_dialog_response(params: Annotated[GenerateInstantRequest, Depends()], user_data=Depends(verify_token)):

    # Load the relevant Dialog Agents (e.g. npc) to get their lore and personality
    from_dialog_agent = dialog_agent_service.get_dialog_agent(params.fromId)
    to_dialog_agent = dialog_agent_service.get_dialog_agent(params.toId)

    # Infer action from what was asked

    # Generate langchain prompt based off all info gathered
    messages = instant_dialog_service.generate_prompt_messages(
        from_dialog_agent=from_dialog_agent,
        from_dialog_agent_input=params.fromInput,
        to_dialog_agent=to_dialog_agent
    )

    # Get generated llm response
    response = llm_service.send_prompt(messages)

    return GenerateInstantResponse(response=response.content)

@router.post("/generate/dialog/tree")
async def create_dialog_tree(body: GenerateDialogTree, user_data=Depends(verify_token)):
    logger.info('Building tree')
    current_dialog_tree_node: DialogTreeNode = dialog_tree_service.get_dialog_tree_node(body.currentDialogTreeNodeId)

    pointers = [current_dialog_tree_node]
    generated_dialog_tree_node_ids = []

    # retrieve lore + chapter info
    project = project_service.get_project(body.projectId)
    lore = project.lore

    # retrieve profiles for involved agents
    # from_dialog_agent = dialog_agent_service.get_dialog_agent(body.fromId)
    to_dialog_agent = dialog_agent_service.get_dialog_agent(body.toDialogAgentId)

    vectorstore = FAISS.load_local("world_index", embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    dialog_state = DialogChainState(
        lore=lore,
        dialog_agent=to_dialog_agent
    )
    chain = dialog_chain_service.create_dialog_agent_rag_chain(dialog_state, retriever)

    while pointers:
        pointer = pointers.pop(0)

        if pointer.generate_response:
            question = "I ask this: " + pointer.match_dialog + "\n answer my question with this as the response, but spruce it up based on your character: " + pointer.respond_dialog
            dialog_state.answer_with = pointer.respond_dialog
            pointer.generated_response = chain({
                "question": question
            })['answer']
        else:
            # TODO : figure out how to inject this into convo history if use
            pointer.generated_response = pointer.respond_dialog
        
        generated_dialog_tree_node_ids.append(pointer.dialog_tree_node_id)
        
        if pointer.next_dialog_tree_node_id and pointer.next_dialog_tree_node_id not in generated_dialog_tree_node_ids:
            pointers.append(dialog_tree_service.get_dialog_tree_node(pointer.next_dialog_tree_node_id))
    
    # return {'response': dialog_tree_service.get_dialog_tree(1, body.dialogTreeId)}
    return {'response': dialog_tree_service.get_dialog_tree_nodes()}

@router.post("/generate/dialog")
async def create_dialog(params: GenerateInstantRequest, user_data=Depends(verify_token)):
    parsed_user_data = json.loads(json.dumps(user_data))
    logger.info('Loading VDB')
    vector_db_service = next((x for x in active_vector_dbs if x.user_id == parsed_user_data['user_id']), None)

    if not vector_db_service:
        vector_db_service = VectorDBService(user_id=parsed_user_data['user_id'], project_id=params.projectId)
        active_vector_dbs.append(vector_db_service)

    logger.info('Finished Loading VDB')

    context = []

    # retrieve lore + chapter info
    project = project_service.get_project(params.projectId)
    lore = project.lore

    for chapter_id in params.completed_chapter_ids:
        chapter = next(x for x in project.chapters if x.chapter_id == chapter_id)
        context.append(chapter.completed_lore)
    
    current_chapter = next(x for x in project.chapters if x.chapter_id == params.current_chapter_id)
    context.append(current_chapter.active_lore)

    # retrieve profiles for involved agents
    from_dialog_agent = dialog_agent_service.get_dialog_agent(params.fromId)
    to_dialog_agent = dialog_agent_service.get_dialog_agent(params.toId)

    dialog_state = DialogChainState(
        lore=lore,
        dialog_agent=to_dialog_agent
    )

    logger.info("context: ")
    logger.info(context)
    vector_db_service.rebase(context)
    retriever = vector_db_service.get_retriever()

    #get conversation history
    if to_dialog_agent.dialog_agent_id not in npc_conversations:
        npc_conversations[to_dialog_agent.dialog_agent_id] = dialog_chain_service.create_dialog_agent_rag_chain(dialog_state, retriever)
    
    chain = npc_conversations[to_dialog_agent.dialog_agent_id]

    # infer what is being asked - (match current state of dialog tree | random chatter)
    dialog_options = dialog_tree_service.get_dialog_tree_nodes()

    inferred_dialog, _ = __match_dialog_option(params.fromInput, dialog_options)

    if inferred_dialog and inferred_dialog.generated_response:
        # fetch pre-built dialog, else generate
        resp = inferred_dialog.generated_response
    else:
        # generate quick response
        # resp = chain({"question": from_dialog_agent.name + ": " + params.fromInput})
        chat_history = chat_history_service.get_chat_history(parsed_user_data['user_id'] + "/" + str(to_dialog_agent.dialog_agent_id))
        resp = dialog_chain_service.create_prompt(params.fromInput, dialog_state, chat_history, retriever)

    chat_history_service.save_chat(parsed_user_data['user_id'] + "/" + str(to_dialog_agent.dialog_agent_id), resp.content)

    return {'response': resp}

def __match_dialog_option(input: str, options: list[DialogTreeNode], threshold: float = 0.75):
    input_vec = embeddings.embed_query(input)
    option_vecs = [embeddings.embed_query(opt.match_dialog) for opt in options]

    sims = cosine_similarity([input_vec], option_vecs)[0]
    best_idx = int(np.argmax(sims))
    best_score = sims[best_idx]

    if best_score >= threshold:
        return options[best_idx], best_score
    return None, best_score
