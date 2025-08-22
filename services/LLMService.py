import os

from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


llm = ChatOpenAI(model="gpt-5-mini", api_key=os.environ.get('OPENAI_API_KEY'))

class LLMService:
    def send_prompt(self, messages):
        return llm.invoke(messages)
