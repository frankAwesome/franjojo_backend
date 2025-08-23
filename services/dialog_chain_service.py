from langchain_openai import ChatOpenAI
from models.dialog_templates.dialog_agent import DialogAgent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationalRetrievalChain


class DialogChainState:
    def __init__(self, lore, dialog_agent: DialogAgent):
        self.lore = lore
        self.name = dialog_agent.name
        self.personality = dialog_agent.personality
        self.background = dialog_agent.lore
        self.answer_with: str = 'Answer by replying to: '


class DialogChainService:
    def create_dialog_agent_rag_chain(self, dialogState: DialogChainState, retriever):
        system_template: str = f"""
        You are an npc in a game:
        {dialogState.lore}
        Your name is:
        {dialogState.name}
        Your personality is:
        {dialogState.personality}
        Your personal backstory/lore is:
        {dialogState.background}

        Always stay in character.
        Use the retrieved world/story facts if relevant.
        If facts conflict with your lore, defer to the world/story facts.
        You can only speak English

        The player/user speaking to you is the big bad wolf.

        Context: {{context}}
        Chat history: {{chat_history}}

        Respond to the player while staying in character, if context conflict, use the one lower in the list as higher order of precedence:
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
            combine_docs_chain_kwargs={"prompt": prompt}
        )

        return chain
