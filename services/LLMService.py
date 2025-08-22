import os

from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-5-mini", api_key=os.environ.get('OPENAI_API_KEY'))

class LLMService:
    def send_prompt(self, messages):
        return llm.invoke(messages)
