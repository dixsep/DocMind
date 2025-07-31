from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from basic import GEMINI_API_KEY1
import logging

logger = logging.getLogger(__name__)

class RetrieverBuilder:
    def __init__(self):
        """Initialize the retriever builder with embeddings."""
        self.embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001", google_api_key = GEMINI_API_KEY1)

    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever using BM25 and vector-based retrieval."""
        try:

            if not docs:
                raise ValueError("No documents were provided to build the retriever.")
            # Create Chroma vector store
            vector_store = Chroma.from_documents(
                documents = docs,
                embedding = self.embeddings,
                persist_directory = "./chroma_db"
            )

            logger.info("Vector store created successfully.")

            # Create BM25 retriever
            bm25 = BM25Retriever.from_documents(docs)
            logger.info("BM25 retriever created successfully.")

            # Create vector-based retriever
            vector_retriever = vector_store.as_retriever(search_kwargs = {"k": 10})
            logger.info("Vector retriever created successfully.")

            # Combine retrievers into a hybrid retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers = [bm25, vector_retriever],
                weights = [0,3, 0.7]
            )
            logger.info("Hybrid retriever created successfully.")
            return hybrid_retriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            raise