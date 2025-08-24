import asyncio
import faiss
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.in_memory import InMemoryDocstore
import os
import logging
import uuid

logger = logging.getLogger("franjojo_backend")

class VectorDBService:

    def __init__(self, instance_id: str):
        self.instance_id = instance_id
        self.persist_path = f"vectorstores/{instance_id}"
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        self.deleted_ids = set()   # soft-delete set

        os.makedirs(self.persist_path, exist_ok=True)

        if os.path.exists(os.path.join(self.persist_path, "index.faiss")):
            self.vectorstore = FAISS.load_local(
                self.persist_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            embedding_size = len(self.embeddings.embed_query("test"))
            index = faiss.IndexFlatL2(embedding_size)
            self.vectorstore = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={}
            )

    def add_documents(self, docs: list[str], ids: list[str] = None):
        """
        Add documents with optional IDs. Preserves IDs across rebases.
        Returns a list of dicts with 'id' and 'content'.
        """
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in docs]
        if len(ids) != len(docs):
            raise ValueError("Length of ids must match length of docs")

        added_docs = []
        for doc, doc_id in zip(docs, ids):
            self.vectorstore.add_texts([doc], ids=[doc_id])
            self.deleted_ids.discard(doc_id)  # in case it was deleted before
            added_docs.append({"id": doc_id, "content": doc})

        self.vectorstore.save_local(self.persist_path)
        return added_docs

    def remove_document(self, doc_id: str, rebase: bool = False):
        """
        Soft delete a document by ID. Actual removal happens on rebase.
        """
        if doc_id in self.vectorstore.index_to_docstore_id.values():
            self.deleted_ids.add(doc_id)
            logger.info(f"Document {doc_id} marked for deletion.")
        else:
            logger.warning(f"Document ID {doc_id} not found.")
        
        if rebase:
            self.rebase()

    def rebase(self):
        """
        Remove all soft-deleted documents while preserving doc IDs for remaining docs.
        """
        # Collect remaining documents with their original IDs
        remaining_docs = [
            (doc_id, self.vectorstore.docstore.search(doc_id).page_content)
            for doc_id in self.vectorstore.index_to_docstore_id.values()
            if doc_id not in self.deleted_ids
        ]

        # Rebuild FAISS index from remaining docs
        embedding_size = len(self.embeddings.embed_query("test"))
        index = faiss.IndexFlatL2(embedding_size)
        new_vectorstore = FAISS(
            embedding_function=self.embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )

        if remaining_docs:
            doc_texts, doc_ids = zip(*remaining_docs)
            new_vectorstore.add_texts(doc_texts, ids=list(doc_ids))

        self.vectorstore = new_vectorstore
        self.deleted_ids.clear()
        self.vectorstore.save_local(self.persist_path)
        logger.info("Index rebased: deleted documents removed.")

    def get_all_documents(self):
        """Return all documents that are not deleted, with their IDs."""
        return [
            {"id": doc_id, "content": self.vectorstore.docstore.search(doc_id).page_content}
            for doc_id in self.vectorstore.index_to_docstore_id.values()
            if doc_id not in self.deleted_ids
        ]

    def query(self, query: str, k: int = 3):
        results = self.vectorstore.similarity_search(query, k=k)
        return [r.page_content for r in results]

    def save(self):
        self.vectorstore.save_local(self.persist_path)

    def get_retriever(self, k: int = 3):
        logger.info("Getting retriever")
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})

        if not hasattr(retriever, "aget_relevant_documents"):
            class AsyncRetrieverWrapper:
                def __init__(self, retriever):
                    self._retriever = retriever

                async def aget_relevant_documents(self, query: str):
                    return await asyncio.to_thread(
                        self._retriever.get_relevant_documents, query
                    )

            retriever = AsyncRetrieverWrapper(retriever)

        logger.info("Done getting retriever")
        return retriever
