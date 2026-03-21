
# 💊 Pharmaceutical Drug Information Assistant using Retrieval-Augmented Generation (RAG)
### نظام استرجاع المعلومات الصيدلانية المدعم بالتوليد (ثنائي اللغة)

نظام متطور يعتمد على تقنية **RAG (Retrieval-Augmented Generation)** للإجابة على الاستفسارات المتعلقة بالأدوية باللغتين **العربية والإنجليزية**. يستخدم النظام نماذج لغوية محلية عبر **Ollama** لضمان الخصوصية والسرعة.

---

## 🚀 الميزات الرئيسية (Key Features)

- **دعم ثنائي اللغة (Multilingual Support):** معالجة الاستفسارات والبيانات باللغتين العربية والإنجليزية بشكل متكامل.
- **تضمينات Ollama المحلية (Local Embeddings):** استخدام نموذج `nomic-embed-text` لتوليد متجهات نصية عالية الدقة.
- **معالجة متقدمة للنص العربي (Arabic NLP):** تنظيف وتوحيد النصوص العربية لضمان دقة البحث.
- **قاعدة بيانات FAISS:** محرك بحث شعاعي فائق السرعة للبحث عن المعلومات ذات الصلة.
- **هيكلية جاهزة للإنتاج (Production Ready):** نظام إعدادات مركزي، تسجيل أحداث (Logging)، ومعالجة أخطاء شاملة.

---

## 🛠️ هيكلية المشروع (Project Structure)

- `data/`: قاعدة بيانات الأدوية (SIDER + Bilingual JSON).
- `src/config.py`: الإعدادات المركزية للنظام.
- `src/data_loader.py`: محرك تحميل ودمج البيانات.
- `src/text_preprocessor.py`: معالج النصوص (تنظيف وتجزئة).
- `src/embedding_generator.py`: مولد المتجهات عبر Ollama.
- `src/vector_store.py`: مدير قاعدة البيانات الشعاعية FAISS.
- `src/llm_integration.py`: واجهة الربط مع النماذج اللغوية (Ollama/OpenAI).
- `src/qa_pipeline.py`: المحرك الرئيسي لعملية السؤال والجواب.
- `app.py`: واجهة المستخدم الرسومية البسيطة (CLI).

---

## 💻 التشغيل السريع (Quick Start)

### 1. المتطلبات (Prerequisites)
- تثبيت برنامج **Ollama** وتحميل النماذج التالية:
  ```bash
  ollama pull nomic-embed-text
  ollama pull llama3
  ```

### 2. التثبيت (Installation)
```bash
pip install -r requirements.txt
```

### 3. التشغيل (Run)
لأول مرة (لبناء قاعدة البيانات):
```bash
python app.py --rebuild
```
للاستخدام العادي:
```bash
python app.py
```

---

## 📖 للمزيد من التفاصيل
يرجى مراجعة ملف **[PROJECT_DETAILS.md](PROJECT_DETAILS.md)** للحصول على شرح تقني مفصل ورسم بياني لآلية العمل.
