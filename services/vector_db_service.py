from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

class VectorDBService:
    def __init__(self, persist_path: str = "world_index"):
        self.persist_path = persist_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

        # Load if existing, else create new
        if os.path.exists(persist_path):
            self.vectorstore = FAISS.load_local(
                persist_path, 
                self.embeddings,
                allow_dangerous_deserialization=True  # required for loading in LangChain
            )
        else:
            self.vectorstore = FAISS.from_texts([], self.embeddings)

    def add_documents(self, docs: list[str]):
        """Add new docs and persist."""
        self.vectorstore.add_texts(docs)
        self.vectorstore.save_local(self.persist_path)

    def query(self, query: str, k: int = 3):
        """Retrieve top-k most similar docs."""
        results = self.vectorstore.similarity_search(query, k=k)
        return [r.page_content for r in results]

    def save(self):
        """Manually save the store."""
        self.vectorstore.save_local(self.persist_path)

    def get_retriever(self, k: int = 3):
        """Return a retriever for use in chains."""
        return self.vectorstore.as_retriever(search_kwargs={"k": k})