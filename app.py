
import argparse
import logging
import sys
from src.qa_pipeline import PharmaceuticalRAG
from src.config import Config

# Setup production logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("rag_system.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("CLI_App")

def main():
    parser = argparse.ArgumentParser(description="Production-Level Pharmaceutical Multilingual RAG System")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild the vector store index from scratch.")
    parser.add_argument("--llm", type=str, choices=["openai", "ollama"], default=Config.LLM_PROVIDER, help="The LLM provider to use.")
    args = parser.parse_args()

    # Update config with CLI arguments
    Config.LLM_PROVIDER = args.llm

    print("\n" + "="*50)
    print("PHARMACEUTICAL RAG SYSTEM (MULTILINGUAL)")
    print("="*50)
    print(f"Provider: {args.llm}")
    print(f"Embeddings: {Config.EMBEDDING_MODEL}")
    print(f"Rebuild Index: {args.rebuild}")
    print("="*50 + "\n")

    try:
        # Initialize the RAG system
        rag = PharmaceuticalRAG(rebuild_index=args.rebuild)
    except Exception as e:
        logger.error(f"Failed to initialize the system: {e}")
        sys.exit(1)

    print("\nSystem ready! You can now ask questions in English or Arabic.")
    print("Type 'exit' or 'quit' to close the application.\n")

    while True:
        try:
            # Multi-line query support can be added if needed, but for now simple input
            query = input("User Question: ").strip()
            
            if query.lower() in ["exit", "quit"]:
                print("\nGoodbye!")
                break
            
            if not query:
                continue

            print("\nSearching and generating answer...")
            answer, sources = rag.ask(query)
            
            print("\n" + "-"*30)
            print("ANSWER:")
            print(answer)
            print("-"*30 + "\n")
            
            # Optional: show sources for production transparency
            # print("Sources retrieved:", len(sources))
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"An error occurred during query processing: {e}")
            print("\nAn error occurred. Please try again.")

if __name__ == "__main__":
    main()
