
import logging
import time
from typing import Tuple
from .config import Config
from .data_loader import load_data, create_drug_documents
from .text_preprocessor import split_into_chunks, preprocess_text
from .embedding_generator import EmbeddingGenerator
from .vector_store import VectorStore
from .llm_integration import LLMInterface

logger = logging.getLogger(__name__)

class PharmaceuticalRAG:
    def __init__(self, rebuild_index: bool = False):
        """
        Initializes the Pharmaceutical RAG system.
        """
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()
        self.llm = LLMInterface()

        if rebuild_index or not self.vector_store.load():
            logger.info("Building vector store from scratch...")
            self._build_initial_index()
        else:
            logger.info("System initialized with existing index.")

    def _build_initial_index(self):
        """
        Builds the initial FAISS index from all data sources.
        """
        inds, sides, bilingual, api = load_data()
        docs = create_drug_documents(inds, sides, bilingual, api)
        chunks = split_into_chunks(docs)
        
        # Generate embeddings for all chunks
        embeddings = self.embedder.get_embeddings(chunks)
        self.vector_store.build_index(chunks, embeddings)

    def ask(self, query: str) -> Tuple[str, list]:
        """
        The main QA flow: Retrieve and Generate.
        """
        start_time = time.time()
        logger.info(f"Received query: {query}")

        # 1. Preprocess and embed query
        # Cleaned query helps in matching if using keyword-based, but for semantic, we might want original or lightly cleaned.
        # We'll use the embedder directly on the query.
        query_embedding = self.embedder.get_embeddings([query])

        # 2. Retrieve relevant chunks
        # Increased K for more context and better synthesis
        relevant_chunks = self.vector_store.search(query_embedding, k=20)
        
        # 3. Generate answer
        answer = self.llm.generate_answer(query, relevant_chunks)
        
        end_time = time.time()
        logger.info(f"QA process took {end_time - start_time:.2f} seconds.")
        
        return answer, relevant_chunks

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Initialize system (might take time for first run)
    rag = PharmaceuticalRAG(rebuild_index=False)
    
    # Test English
    ans, docs = rag.ask("What are the side effects of Ibuprofen?")
    print(f"\nEN Answer: {ans}\n")
    
    # Test Arabic
    ans_ar, docs_ar = rag.ask("ما هي الآثار الجانبية للأيبوبروفين؟")
    print(f"\nAR Answer: {ans_ar}\n")
