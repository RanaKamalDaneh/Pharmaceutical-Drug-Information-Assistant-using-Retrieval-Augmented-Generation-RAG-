
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import logging
from src.qa_pipeline import PharmaceuticalRAG
from src.config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Web_App")

app = Flask(__name__)
CORS(app)

# Initialize RAG system
# We don't rebuild the index by default to save time
logger.info("Initializing Pharmaceutical RAG system for Web...")
rag = PharmaceuticalRAG(rebuild_index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({"success": False, "error": "Empty query"}), 400
            
        logger.info(f"Processing web query: {query}")
        answer, sources = rag.ask(query)
        
        return jsonify({
            "success": True, 
            "answer": answer,
            "sources_count": len(sources)
        })
        
    except Exception as e:
        logger.error(f"Error in web API: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Get port from env or default to 5000
    port = int(os.environ.get("PORT", 5000))
    print(f"\nPharmaAssist Web Server started at http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
