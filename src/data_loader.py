
import pandas as pd
import json
import os
import logging
import requests
from .config import Config

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_data_from_api():
    """
    Fetches drug data from the API specified in the settings (e.g., openFDA).
    """
    url = Config.DRUG_API_URL
    api_key = Config.DRUG_API_KEY
    
    try:
        logger.info(f"Fetching data from API: {url}...")
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        processed_data = []
        for item in data.get('results', []):
            processed_data.append({
                "name_en": item.get("openfda", {}).get("brand_name", ["Not available"])[0],
                "dosage_en": item.get("dosage_and_administration", ["Not available"])[0],
                "warnings_en": item.get("warnings", ["Not available"])[0],
                "side_effects_en": item.get("adverse_reactions", ["Not available"])[0],
                "indications_en": item.get("indications_and_usage", ["Not available"])[0]
            })
        logger.info(f"Fetched {len(processed_data)} records from API.")
        return processed_data
    except Exception as e:
        logger.error(f"Error while fetching data from API: {e}")
        return []

def load_data():
    """
    Loads SIDER data, bilingual drug data, and OpenFDA API data.
    """
    try:
        # Load SIDER data
        indications = pd.read_csv(Config.SIDER_INDICATIONS, sep="\t")
        side_effects = pd.read_csv(Config.SIDER_SIDE_EFFECTS, sep="\t")
        logger.info(f"Loaded {len(indications)} indications and {len(side_effects)} side effects from SIDER.")
        
        # Load Bilingual data
        with open(Config.BILINGUAL_DATA, "r", encoding='utf-8') as f:
            bilingual_data = json.load(f)
        logger.info(f"Loaded {len(bilingual_data)} bilingual drug entries.")
        
        # Fetch API data
        api_data = fetch_data_from_api()
        
        return indications, side_effects, bilingual_data, api_data
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return None, None, None, []

def create_drug_documents(indications, side_effects, bilingual_data, api_data=[]):
    """
    Creates a list of documents for each drug, prioritizing official API data.
    Unified format based on openFDA structure.
    """
    documents = []

    # 1. Process Official API Data (Primary Source)
    for entry in api_data:
        doc_api = (
            f"Source: Official FDA Record\n"
            f"Drug Name: {entry.get('name_en', 'N/A')}\n"
            f"Indications & Usage: {entry.get('indications_en', 'N/A')}\n"
            f"Dosage & Administration: {entry.get('dosage_en', 'N/A')}\n"
            f"Side Effects (Adverse Reactions): {entry.get('side_effects_en', 'N/A')}\n"
            f"Warnings & Precautions: {entry.get('warnings_en', 'N/A')}"
        )
        documents.append(doc_api)

    # 2. Process Bilingual Local Data (Secondary/Fallback)
    if bilingual_data:
        for entry in bilingual_data:
            # English version
            doc_en = (
                f"Source: Local Bilingual Database\n"
                f"Drug Name: {entry.get('name_en', 'N/A')}\n"
                f"Indications & Usage: {entry.get('indications_en', 'N/A')}\n"
                f"Side Effects (Adverse Reactions): {entry.get('side_effects_en', 'N/A')}\n"
                f"Warnings & Precautions: {entry.get('warnings_en', 'N/A')}"
            )
            documents.append(doc_en)
            
            # Arabic version (Keep as it's useful for Arabic queries)
            doc_ar = (
                f"المصدر: قاعدة بيانات محلية ثنائية اللغة\n"
                f"اسم الدواء: {entry.get('name_ar', 'N/A')}\n"
                f"دواعي الاستعمال: {entry.get('indications_ar', 'N/A')}\n"
                f"الآثار الجانبية: {entry.get('side_effects_ar', 'N/A')}\n"
                f"التحذيرات: {entry.get('warnings_ar', 'N/A')}"
            )
            documents.append(doc_ar)

    # 3. Process SIDER data (Only if no other data available or for broad coverage)
    # We will skip SIDER for now as per user's concern about reliability/consistency
    # unless you want to keep it as a broad fallback.
    
    logger.info(f"Total documents generated: {len(documents)} (API: {len(api_data)}, Local: {len(bilingual_data)*2 if bilingual_data else 0})")
    return documents

if __name__ == "__main__":
    inds, sides, bilingual, api = load_data()
    docs = create_drug_documents(inds, sides, bilingual, api)
    if docs:
        print(f"Sample API Document:\n{docs[-1]}\n")
