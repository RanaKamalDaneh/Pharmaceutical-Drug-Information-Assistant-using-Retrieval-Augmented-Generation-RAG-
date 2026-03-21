
import ollama
from openai import OpenAI
import numpy as np
import logging
from typing import List
from .config import Config
from tqdm import tqdm

logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    def __init__(self, provider: str = Config.EMBEDDING_PROVIDER, model_name: str = Config.EMBEDDING_MODEL):
        """
        Initializes the embedding generator (Ollama or OpenAI).
        """
        self.provider = provider
        self.model_name = model_name
        
        if self.provider == "openai":
            if not Config.OPENAI_API_KEY:
                logger.error("OpenAI API Key not found for embeddings.")
                raise ValueError("OPENAI_API_KEY is required for OpenAI embeddings.")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
            logger.info(f"Using OpenAI embedding model: {self.model_name}")
        else:
            self.host = Config.OLLAMA_HOST
            logger.info(f"Using Ollama embedding model: {self.model_name}")

    def get_embeddings(self, chunks: List[str]) -> np.ndarray:
        """
        Generates embeddings for a list of text chunks.
        """
        embeddings = []
        logger.info(f"Generating embeddings for {len(chunks)} chunks using {self.provider} ({self.model_name})...")
        
        if self.provider == "openai":
            # Process in batches for OpenAI
            batch_size = 100
            for i in tqdm(range(0, len(chunks), batch_size), desc="OpenAI Embeddings"):
                batch = chunks[i:i+batch_size]
                try:
                    response = self.client.embeddings.create(input=batch, model=self.model_name)
                    embeddings.extend([item.embedding for item in response.data])
                except Exception as e:
                    logger.error(f"Error generating OpenAI embeddings: {e}")
                    # Fallback for batch failure
                    embeddings.extend([[0] * 1536] * len(batch)) # Default for text-embedding-3-small
        else:
            # Process one by one for Ollama (current library limitation or for simplicity)
            for chunk in tqdm(chunks, desc="Ollama Embeddings"):
                try:
                    response = ollama.embeddings(model=self.model_name, prompt=chunk)
                    embeddings.append(response['embedding'])
                except Exception as e:
                    logger.error(f"Error generating Ollama embedding: {e}")
                    embeddings.append([0] * 768) # Default for nomic-embed-text
                
        return np.array(embeddings).astype('float32')

if __name__ == "__main__":
    from .data_loader import load_data, create_drug_documents
    from .text_preprocessor import split_into_chunks
    
    logging.basicConfig(level=logging.INFO)
    
    # Setup data
    inds, sides, bilingual, api = load_data()
    docs = create_drug_documents(inds, sides, bilingual, api)
    chunks = split_into_chunks(docs)
    
    # Test embeddings
    generator = EmbeddingGenerator()
    test_chunks = chunks[:5]
    embeddings = generator.get_embeddings(test_chunks)
    
    logger.info(f"Generated {len(embeddings)} embeddings.")
    logger.info(f"Embedding shape: {embeddings.shape}")
