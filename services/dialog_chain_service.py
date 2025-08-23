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
        You are a dialog agent in the following domain:
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

        Context: {{context}}
        Generate an answer for this: {{answer_with}} - To the question:
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
