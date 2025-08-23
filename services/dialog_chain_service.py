from typing import List
from langchain_openai import ChatOpenAI
from models.dialog_templates.dialog_agent import DialogAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
import logging


logger = logging.getLogger("franjojo_backend")


class DialogChainState:
    def __init__(self, lore, dialog_agent: DialogAgent):
        self.lore = lore
        self.name = dialog_agent.name
        self.personality = dialog_agent.personality
        self.background = dialog_agent.lore
        self.answer_with: str = 'Answer by replying to: '

    def __init__(self, lore, name: str, background: str):
        self.lore = lore
        self.name = name
        self.background = background
        self.personality = ''

class DialogChainService:
    def create_dialog_agent_rag_chain(self, dialogState: DialogChainState, retriever):
        system_template: str = f"""
        You are an npc in a game set in this world:
        {dialogState.lore}
        Your name is:
        {dialogState.name}
        Your personality traits are:
        {dialogState.personality}
        Your personal backstory/lore is:
        {dialogState.background}

        Always stay in character.
        Use the retrieved world/story facts if relevant.
        If facts conflict with your lore, defer to the world/story facts.
        You can only speak English

        Context: {{context}}

        Generate a response to the player while staying in character:
        """

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("human", "{question}")
        ])

        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=memory,
            combine_docs_chain_kwargs={"prompt": prompt})

        return chain
    
    

    def create_prompt(self, question, dialogState: DialogChainState, chat_history, manual_context: List[str], retriever):

        better_manual_context = ''

        for x in manual_context:
            better_manual_context += x + ','
        
        better_chat_history = ''

        for x in chat_history:
            better_chat_history += x + '\n'

        logger.info('chat_hist:')
        logger.info(better_chat_history)

        prompt = PromptTemplate.from_template(f"""
        You are an npc in a game set in this world:
        {dialogState.lore}
        Your name is:
        {dialogState.name}
        Your personality traits are:
        {dialogState.personality}
        Your personal backstory/lore is:
        {dialogState.background}

        Always stay in character.
        Use the retrieved world/story facts if relevant.
        If facts conflict with your lore, defer to the world/story facts.
        You can only speak English.
        Respond with 2 sentences max.

        Context: 
        {better_manual_context}
        {{retriever_context}}
        Chat history:
        {better_chat_history}

        Generate a response to the players question while staying in character:
        Player: {question}
        """)

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9)
        chain = {
            "retriever_context": retriever,       # will pass query into retriever
        } | prompt | llm

        # 5. Run
        result = chain.invoke(question)
        return result
