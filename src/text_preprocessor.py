
import re
import logging
from typing import List
from pyarabic.araby import strip_tashkeel, normalize_alef, normalize_teh
from .config import Config

logger = logging.getLogger(__name__)

def clean_arabic_text(text: str) -> str:
    """
    Cleans and normalizes Arabic text.
    """
    # Remove tashkeel (diacritics)
    text = strip_tashkeel(text)
    # Normalize alef, teh marbuta, and alef maksura
    text = normalize_alef(text)
    text = normalize_teh(text)
    # Remove special characters but keep Arabic letters and numbers
    text = re.sub(r'[^\u0600-\u06FF0-9\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_english_text(text: str) -> str:
    """
    Cleans and normalizes English text.
    """
    text = text.lower()
    # Remove special characters but keep letters and numbers
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text: str) -> str:
    """
    Detects language and applies appropriate cleaning.
    """
    # Simple detection based on character ranges
    if re.search(r'[\u0600-\u06FF]', text):
        return clean_arabic_text(text)
    else:
        return clean_english_text(text)

def split_into_chunks(documents: List[str], chunk_size: int = Config.CHUNK_SIZE, overlap: int = Config.CHUNK_OVERLAP) -> List[str]:
    """
    Splits documents into semantic chunks with overlap.
    """
    chunks = []
    for doc in documents:
        # Simple word-based splitting as a proxy for tokens
        words = doc.split()
        if not words:
            continue
            
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            # Preprocess each chunk
            # cleaned_chunk = preprocess_text(chunk) # We might want to keep some structure for LLM
            chunks.append(chunk)
            
    logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    from .data_loader import load_data, create_drug_documents
    
    logging.basicConfig(level=logging.INFO)
    
    inds, sides, bilingual, api = load_data()
    docs = create_drug_documents(inds, sides, bilingual, api)
    
    # Test cleaning
    ar_test = "الحُمَّى، الآلام الخفيفة إلى المتوسطة"
    logger.info(f"Original Arabic: {ar_test}")
    logger.info(f"Cleaned Arabic: {clean_arabic_text(ar_test)}")
    
    # Test chunking
    chunks = split_into_chunks(docs)
    if chunks:
        logger.info(f"First chunk: {chunks[0][:100]}...")
