
import os
import requests
import logging
from typing import List
from openai import OpenAI
import ollama
from .config import Config

logger = logging.getLogger(__name__)

class LLMInterface:
    def __init__(self, provider: str = Config.LLM_PROVIDER):
        """
        Initializes the LLM interface based on the provider.
        """
        self.provider = provider
        if self.provider == "openai":
            if not Config.OPENAI_API_KEY:
                logger.error("OpenAI API Key not found.")
                raise ValueError("OPENAI_API_KEY environment variable is required.")
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == "ollama":
            self.model = Config.OLLAMA_MODEL
            logger.info(f"Using Ollama LLM model: {self.model}")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate_answer(self, query: str, context: List[str]) -> str:
        """
        Generates a professional, detailed answer to the query using the provided context.
        Supports multilingual queries with enhanced medical instructions.
        """
        full_context = "\n---\n".join(context)
        
        system_prompt = (
            "You are a highly qualified Pharmaceutical Expert and Medical Consultant. "
            "Your task is to provide comprehensive, accurate, and scientifically grounded information based ONLY on the provided context. "
            "\n\nGUIDELINES:\n"
            "1. If the query is in Arabic, respond with professional, clear Arabic. If in English, use professional medical English.\n"
            "2. Structure your answer using bullet points and clear headings (e.g., Dosage, Side Effects, Warnings).\n"
            "3. If multiple sources are provided, synthesize the information into a single coherent response.\n"
            "4. ALWAYS include a medical disclaimer: 'This information is for educational purposes only. Always consult a healthcare professional before taking any medication.'\n"
            "5. If the specific answer (like dosage) is not explicitly in the context, but the drug is mentioned, summarize what IS available about the drug and suggest consulting a clinical guide for the missing specific details.\n"
            "6. If the drug is not mentioned at all in the context, politely state that you do not have official records for this specific drug in your current database.\n"
            "7. Maintain a serious, professional, and helpful tone."
        )
        
        user_prompt = f"### OFFICIAL MEDICAL CONTEXT:\n{full_context}\n\n### USER QUERY:\n{query}\n\n### EXPERT RESPONSE:"

        try:
            if self.provider == "openai":
                # Using configured model for OpenAI
                model_to_use = Config.OPENAI_MODEL
                response = self.client.chat.completions.create(
                    model=model_to_use,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.choices[0].message.content
            
            elif self.provider == "ollama":
                response = ollama.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response['message']['content']
                
        except Exception as e:
            logger.error(f"Error generating answer from {self.provider}: {e}")
            return "Sorry, I encountered an error while processing your request."

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    llm = LLMInterface()
    
    # Test English
    en_query = "What is Acetaminophen used for?"
    en_context = ["Acetaminophen is used for fever and mild to moderate pain."]
    logger.info(f"EN Query: {en_query}")
    logger.info(f"EN Answer: {llm.generate_answer(en_query, en_context)}")
    
    # Test Arabic
    ar_query = "ما هي استخدامات الباراسيتامول؟"
    ar_context = ["يستخدم الباراسيتامول للحمى والآلام الخفيفة إلى المتوسطة."]
    logger.info(f"AR Query: {ar_query}")
    logger.info(f"AR Answer: {llm.generate_answer(ar_query, ar_context)}")
