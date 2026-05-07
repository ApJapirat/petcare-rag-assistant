# 🐾 PetCare RAG Chatbot

ระบบตอบคำถามสายพันธุ์สัตว์เลี้ยง (แมวและสุนัข) โดยใช้ **RAG (Retrieval-Augmented Generation)**

ข้อมูลจากเว็บไซต์ [Purina Thailand](https://www.purina.co.th)

---

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a local `.env` file from the example:
```bash
copy .env.example .env
```

On macOS/Linux:
```bash
cp .env.example .env
```

3. Open `.env` and set your Gemini key:
```env
GEMINI_API_KEY=your_real_gemini_api_key_here
```

Do not commit `.env`. It is ignored by `.gitignore`.

4. Build the vector index if needed:
```bash
python rag/build_index.py
```

5. Run the FastAPI app:
```bash
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000` in your browser.

## Render Setup

In Render, add this environment variable in the service settings:

```env
GEMINI_API_KEY=your_real_gemini_api_key_here
```

Use this Render start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Render will read `GEMINI_API_KEY` from its environment variables, so do not upload a `.env` file.

---

## 📋 การแบ่งงาน

| คนที่ | หน้าที่ | ไฟล์หลัก |
|-------|---------|----------|
| 1. Data + NLP (แพท) | เก็บข้อมูลจาก Purina, Clean text, สร้าง CSV | `scraper.py`, `data/pet_breeds.csv` |
| 2. Model / AI Logic (ซซีาร์) | สร้าง Vector Index, Semantic Search, RAG | `rag/build_index.py`, `rag/search.py`, `rag/answer.py` |
| 3. Backend / UI (เต้) | สร้าง FastAPI backend และหน้าเว็บ HTML/CSS/JS | `backend/`, `frontend/static/` |

---

## 🚀 วิธีรัน (Quick Start)

### 1. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 2. สร้าง Vector Index (ครั้งแรกเท่านั้น)
```bash
python rag/build_index.py
```

### 3. เปิดเว็บ Chatbot
```bash
uvicorn backend.main:app --reload
```

เปิดเบราว์เซอร์ไปที่ **http://127.0.0.1:8000**

---

## 🗂️ โครงสร้างโปรเจค

```
PetCare_RAG/
├── scraper.py                 ← ดึงข้อมูลจาก Purina (คนที่ 1)
├── requirements.txt           ← Dependencies
├── README.md                  ← คู่มือนี้
├── .env.example               ← ตัวอย่าง Environment Variable
├── backend/
│   ├── main.py                ← FastAPI app + static file server
│   ├── api/
│   │   └── routes.py          ← API endpoint POST /ask
│   ├── core/
│   │   └── config.py          ← Path/config สำหรับ backend
│   ├── schemas/
│   │   └── ask.py             ← Request/response models
│   └── services/
│       └── rag_service.py     ← โหลด RAG และเรียก rag.answer()
├── frontend/
│   └── static/
│       ├── index.html         ← หน้าเว็บหลัก
│       ├── style.css          ← Cute cat-themed UI
│       └── script.js          ← เรียก API /ask
├── docs/
│   └── README_RAG.md          ← คู่มือ RAG ละเอียด (คนที่ 2)
├── logs/
│   ├── streamlit-ui.log
│   └── streamlit-ui.err.log
├── tests/
│   └── test_rag.py            ← สคริปต์ทดสอบ RAG
├── legacy/
│   └── app_streamlit.py       ← Streamlit เวอร์ชันเก่า (ไม่ใช้ deploy)
│
├── data/
│   ├── pet_breeds.csv         ← Dataset 53 สายพันธุ์
│   └── pet_breedsRaw.csv      ← Raw data
│
└── rag/
    ├── __init__.py
    ├── build_index.py         ← สร้าง Vector Index (คนที่ 2)
    ├── search.py              ← Semantic Search (คนที่ 2)
    ├── answer.py              ← RAG + LLM (คนที่ 2)
    └── index/
        ├── faiss_index.index  ← FAISS index (สร้างอัตโนมัติ)
        └── chunks.pkl         ← Chunk metadata
```

---

## 🔧 ส่วนที่ 1: Data + NLP (คนที่ 1)

### หน้าที่
- ดึงข้อมูลสายพันธุ์แมวและสุนัขจาก Purina
- Clean text และจัดรูปแบบ
- สร้าง dataset CSV

### วิธีรัน
```bash
python scraper.py
```

### Output
- `data/pet_breeds.csv` — 53 สายพันธุ์ (แมว 22 + สุนัข 31)
- Columns: `type, breed_name, full_text, source_url`

---

## 🧠 ส่วนที่ 2: Model / AI Logic (คนที่ 2)

### หน้าที่
- อ่าน CSV → สร้าง Document → Split Chunk → Embedding → FAISS
- Semantic Search ค้นหาคำตอบที่เกี่ยวข้อง
- RAG: ส่ง context ให้ LLM ตอบคำถาม

### วิธีรัน
```bash
# สร้าง index
python rag/build_index.py

# ทดสอบ search
python rag/search.py

# ทดสอบ RAG
python rag/answer.py
```

### Pipeline
```
CSV → Document → Chunk → Embedding (Sentence-BERT) → FAISS Index
                                                          ↓
User Query → Query Embedding → FAISS Search → Top-K Chunks → RAG Prompt → LLM → Answer
```

### LLM ที่รองรับ
| Provider | ต้องติดตั้ง | API Key |
|----------|-----------|---------|
| Gemini | `pip install google-genai` | Google AI Studio |
| OpenAI | `pip install openai` | OpenAI |
| Typhoon | `pip install openai` | OpenTyphoon |
| Ollama | ติดตั้ง Ollama | ไม่ต้อง (local) |

---

## 🖥️ ส่วนที่ 3: Backend / UI (คนที่ 3)

### หน้าที่
- สร้าง FastAPI backend สำหรับ API endpoint `POST /ask`
- เสิร์ฟหน้าเว็บ static HTML/CSS/JavaScript จาก FastAPI
- ช่องให้ user พิมพ์คำถาม แล้ว frontend เรียก backend API
- แสดงผลลัพธ์: คำตอบ AI, Source, สายพันธุ์ที่เกี่ยวข้อง

### วิธีรัน
```bash
uvicorn backend.main:app --reload
```

### หน้าเว็บมี
- **Title:** PetCare RAG Assistant
- **Input:** ช่องถามคำถาม
- **Ask Button:** กดแล้วเรียก API `/ask`
- **Output:**
  - 💬 คำตอบ AI
  - 📚 Source ที่ระบบใช้ตอบ (ชื่อสายพันธุ์, ประเภท, ลิงก์, คะแนนความเกี่ยวข้อง)
  - 🏷️ สายพันธุ์ที่เกี่ยวข้อง (tag)
- **Info panel:**
  - ข้อมูลเกี่ยวกับระบบ
  - ตัวอย่างคำถาม (กดได้เลย)
  - Tech stack

---

## 🧪 คำถามทดสอบ

| คำถาม | ประเภทที่คาดหวัง |
|--------|------------------|
| แมวพันธุ์ไหนเหมาะกับคนอยู่คนเดียว | cat |
| สุนัขพันธุ์ไหนขนสั้นดูแลง่าย | dog |
| Persian มีนิสัยยังไง | cat |
| แมวขนยาวต้องดูแลอะไรบ้าง | cat |

---

## 📦 Dependencies

```
pandas
numpy
beautifulsoup4
selenium
sentence-transformers
faiss-cpu
transformers
google-genai
google-generativeai
fastapi
uvicorn
python-dotenv
requests
```

---

## 🎤 Presentation Tips

### สไลด์นำเสนอ
1. **ภาพรวม** — ระบบถาม-ตอบสายพันธุ์สัตว์เลี้ยง ใช้ RAG
2. **Data Pipeline** — Scrape → Clean → CSV → Embed → FAISS
3. **RAG Architecture** — Query → Search → Context → LLM → Answer
4. **Demo** — เปิด FastAPI website แล้วถามคำถามสด

### Demo Script
1. เปิด Terminal → `uvicorn backend.main:app --reload`
2. พิมพ์ "แมวพันธุ์ไหนเหมาะกับคนอยู่คนเดียว" → กด Ask
3. ชี้คำตอบ + Sources + คะแนนความเกี่ยวข้อง
4. ลองคำถามอื่น: "สุนัขพันธุ์ไหนขนสั้นดูแลง่าย"
5. กดปุ่มตัวอย่างคำถามในแผงด้านซ้าย
