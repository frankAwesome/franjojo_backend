import faiss
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from langchain.docstore.in_memory import InMemoryDocstore

class VectorDBService:

    def __init__(self, user_id, project_id: int):
        self.user_id = user_id
        self.project_id = project_id
        self.persist_path = f"vectorstores/{user_id}/{project_id}"
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

        os.makedirs(self.persist_path, exist_ok=True)

        if os.path.exists(os.path.join(self.persist_path, "index.faiss")):
            # Load existing index
            self.vectorstore = FAISS.load_local(
                self.persist_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # Create an empty FAISS index properly
            embedding_size = len(self.embeddings.embed_query("test"))
            index = faiss.IndexFlatL2(embedding_size)
            self.vectorstore = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )

    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        self.persist_path = f"vectorstores/{instance_id}"
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None

        os.makedirs(self.persist_path, exist_ok=True)

        if os.path.exists(os.path.join(self.persist_path, "index.faiss")):
            # Load existing index
            self.vectorstore = FAISS.load_local(
                self.persist_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # Create an empty FAISS index properly
            embedding_size = len(self.embeddings.embed_query("test"))
            index = faiss.IndexFlatL2(embedding_size)
            self.vectorstore = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )

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

    def rebase(self, new_docs: list[str] = None):
        """
        Rebuild the FAISS index from original documents or a new set.
        If new_docs is provided, it will replace the current documents.
        """
        if new_docs is not None:
            self.original_docs = new_docs

        # Rebuild index from scratch
        self.vectorstore = FAISS.from_texts(self.original_docs, self.embeddings)
        self.save()