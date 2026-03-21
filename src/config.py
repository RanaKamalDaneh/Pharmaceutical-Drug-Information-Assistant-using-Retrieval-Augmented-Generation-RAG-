
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    SRC_DIR = os.path.join(PROJECT_ROOT, "src")
    
    # Files
    SIDER_INDICATIONS = os.path.join(DATA_DIR, "indications.tsv")
    SIDER_SIDE_EFFECTS = os.path.join(DATA_DIR, "side-effects.tsv")
    BILINGUAL_DATA = os.path.join(DATA_DIR, "bilingual_drugs.json")
    
    # Vector Store
    CHROMA_PATH = os.path.join(PROJECT_ROOT, "chroma_db")
    COLLECTION_NAME = "pharmaceutical_drugs"
    
    # Embedding Model
    # Provider: 'ollama' or 'openai'
    EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # LLM (OpenAI or Ollama)
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

    # Data API
    DRUG_API_URL = os.getenv("DRUG_API_URL", "https://api.fda.gov/drug/label.json?limit=10")
    DRUG_API_KEY = os.getenv("DRUG_API_KEY", "")
    
    # Chunker
    CHUNK_SIZE = 500  # tokens
    CHUNK_OVERLAP = 50
