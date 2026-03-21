
# 💊 Pharmaceutical Multilingual RAG System
### نظام استرجاع المعلومات الصيدلانية المدعم بالتوليد (ثنائي اللغة)

A professional, production-ready **Retrieval-Augmented Generation (RAG)** system designed to provide accurate pharmaceutical drug information in both **Arabic and English**. The system integrates official **openFDA data**, uses **ChromaDB** for vector storage, and supports both local (**Ollama**) and cloud-based (**OpenAI GPT-4o**) models.

---

## 🚀 الميزات الرئيسية (Key Features)

- **Multilingual Support (دعم ثنائي اللغة):** Full processing of queries and data in both Arabic and English.
- **Official Data Integration:** Automatically fetches the latest drug labels from the **openFDA API**.
- **Hybrid AI Power:** Switch seamlessly between local models (Ollama) and high-performance cloud models (OpenAI GPT-4o).
- **Advanced Arabic NLP:** Specialized normalization and cleaning for Arabic text using `PyArabic` to ensure high retrieval accuracy.
- **ChromaDB Vector Store:** Industry-standard vector database for fast, persistent, and reliable semantic search.
- **Production-Ready:** Centralized configuration, comprehensive logging, and automated database rebuilding.

---

## 🛠️ هيكلية المشروع (Project Structure)

- `data/`: Local bilingual datasets and drug information.
- `src/config.py`: Centralized system configuration.
- `src/data_loader.py`: Handles FDA API fetching and local data merging.
- `src/text_preprocessor.py`: Text cleaning and semantic chunking.
- `src/embedding_generator.py`: Generates vectors via Ollama or OpenAI.
- `src/vector_store.py`: Manages the **ChromaDB** collection.
- `src/llm_integration.py`: Connects to LLMs (GPT-4o / Llama3).
- `src/qa_pipeline.py`: Orchestrates the RAG flow (Retrieve -> Generate).
- `app.py`: Professional Command-Line Interface (CLI).

---

## 💻 التشغيل السريع (Quick Start)

### 1. Prerequisites (المتطلبات)
- Install **Ollama** and pull models (for local use):
  ```bash
  ollama pull nomic-embed-text
  ollama pull llama3
  ```
- Obtain an **OpenAI API Key** (for cloud use).

### 2. Installation (التثبيت)
```bash
git clone https://github.com/RanaKamalDaneh/Pharmaceutical-Drug-Information-Assistant-using-Retrieval-Augmented-Generation-RAG-.git
cd Pharmaceutical-Drug-Information-Assistant-using-Retrieval-Augmented-Generation-RAG-
pip install -r requirements.txt
```

### 3. Configuration (الإعدادات)
Create a `.env` file in the root directory:
```env
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your_key_here
DRUG_API_URL=https://api.fda.gov/drug/label.json?limit=100
```

### 4. Running the System (التشغيل)
Build the database for the first time:
```bash
python app.py --rebuild
```
Start chatting:
```bash
python app.py
```

---

## 📖 Technical Documentation
For a deep dive into the architecture and workflow diagrams, please refer to **[PROJECT_DETAILS.md](PROJECT_DETAILS.md)**.
