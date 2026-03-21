import chromadb
import numpy as np
import logging
import os
from typing import List
from .config import Config

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, chroma_path: str = Config.CHROMA_PATH, collection_name: str = Config.COLLECTION_NAME):
        """
        Initializes the VectorStore using ChromaDB.
        """
        self.chroma_path = chroma_path
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=self.chroma_path)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def build_index(self, chunks: List[str], embeddings: np.ndarray):
        """
        Stores text chunks and their embeddings in ChromaDB.
        Clears the collection before adding new data to ensure a clean state.
        """
        try:
            # Clear existing data in the collection first
            count = self.collection.count()
            if count > 0:
                logger.info(f"Clearing {count} existing items from ChromaDB collection for a clean rebuild.")
                self.client.delete_collection(name=self.collection_name)
                self.collection = self.client.create_collection(name=self.collection_name)

            logger.info(f"Adding {len(chunks)} items to ChromaDB collection: {self.collection_name}")
            
            # Chroma expects IDs for each document
            ids = [f"id_{i}" for i in range(len(chunks))]
            
            # Convert numpy array to list for Chroma
            embeddings_list = embeddings.tolist()
            
            self.collection.add(
                embeddings=embeddings_list,
                documents=chunks,
                ids=ids
            )
            logger.info(f"Successfully added data to ChromaDB at {self.chroma_path}")
        except Exception as e:
            logger.error(f"Error building ChromaDB index: {e}")

    def load(self) -> bool:
        """
        Checks if the collection exists and has data.
        """
        try:
            count = self.collection.count()
            if count > 0:
                logger.info(f"Loaded ChromaDB collection with {count} items.")
                return True
            else:
                logger.warning("ChromaDB collection is empty.")
                return False
        except Exception as e:
            logger.error(f"Error loading ChromaDB: {e}")
            return False

    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[str]:
        """
        Searches ChromaDB for the top k most similar chunks.
        """
        try:
            # Convert query embedding to list
            query_list = query_embedding.tolist()
            
            results = self.collection.query(
                query_embeddings=query_list,
                n_results=k
            )
            
            # results['documents'] is a list of lists
            return results['documents'][0]
        except Exception as e:
            logger.error(f"Error searching ChromaDB: {e}")
            return []

if __name__ == "__main__":
    from .data_loader import load_data, create_drug_documents
    from .text_preprocessor import split_into_chunks
    from .embedding_generator import EmbeddingGenerator
    
    logging.basicConfig(level=logging.INFO)
    
    # Example usage for testing
    inds, sides, bilingual, api = load_data()
    docs = create_drug_documents(inds, sides, bilingual, api)
    chunks = split_into_chunks(docs[:10]) # Use small sample
    
    generator = EmbeddingGenerator()
    embeddings = generator.get_embeddings(chunks)
    
    vs = VectorStore()
    vs.build_index(chunks, embeddings)
    
    # Test search
    test_query_emb = generator.get_embeddings(["What is Paracetamol?"])
    results = vs.search(test_query_emb)
    logger.info(f"Search results: {results}")
